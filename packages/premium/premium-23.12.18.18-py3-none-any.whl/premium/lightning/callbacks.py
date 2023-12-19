from abc import ABC, abstractmethod

import codefast as cf
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
import torch 

def configure_optimizers(self):
    self.hparams.lr = 1e-5
    self.hparams.warm_up_step = 500
    optimizer = torch.optim.Adam(self.parameters(), lr=self.hparams.lr)

    def lr_foo(epoch):
        if epoch < self.hparams.warm_up_step:
            # warm up lr
            lr_scale = 0.1 ** (self.hparams.warm_up_step - epoch)
        else:
            lr_scale = 0.95 ** epoch

        return lr_scale

    scheduler = torch.optim.lr_scheduler.LambdaLR(
        optimizer,
        lr_lambda=lr_foo
    )

    return [optimizer], [scheduler]



class ModelMetrics(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.pos = 4 if 'pos' not in kwargs else kwargs['pos']

    def __str__(self):
        ignore_keys = ['pos']
        iter_keys = ['epoch']
        class_name = self.__class__.__name__

        def _repr_metric():
            for k, v in self.kwargs.items():
                if k not in ignore_keys:
                    # check if v is a tensor, if so convert to float
                    vv = v.item() if hasattr(v, 'item') else v
                    if k in iter_keys:
                        yield f'{k}={vv}'
                    else:
                        yield f'{k}={round(vv, self.pos)}'

        return f'{class_name}({", ".join([_ for _ in _repr_metric()])})\n'


# Abstract class for callbacks
class ModelMetricsCallback(pl.Callback, ABC):

    def __init__(self):
        self.metrics = []

    @abstractmethod
    def on_validation_epoch_end(self, trainer, pl_module):
        ...

    def on_train_end(self, trainer, pl_module):
        if self.metrics:
            print(self.metrics[-1])


class PretrainedSaveCallback(pl.Callback):
    """ save best model 
    """

    def __init__(self, save_path: str):
        self.save_path = save_path
        self.best_loss = float('inf')

    def on_validation_epoch_end(self, trainer, pl_module):
        metrics = trainer.callback_metrics
        if 'val_loss' in metrics.keys():
            val_loss = metrics['val_loss'].item()
            if val_loss < self.best_loss:
                self.best_loss = val_loss
                trainer.model.pretrained.save_pretrained(self.save_path)


class AccLossCallback(ModelMetricsCallback):

    def on_validation_epoch_end(self, trainer, pl_module):
        """
        usage: 
        def validation_step(self, batch, batch_idx):
            ...
            metric = {'val_loss': loss, 'val_acc': accuracy}
            self.log_dict(metric)
        """
        metrics = ModelMetrics(epoch=trainer.current_epoch, )
        import torch
        for k, v in trainer.callback_metrics.items():
            _v = v.cpu()
            if isinstance(_v, torch.Tensor):
                _v = _v.item()
            metrics.kwargs[k] = _v
        try:
            from rich import print
        except ImportError:
            pass
        print(metrics)
        self.metrics.append(metrics)


class f1Callback(ModelMetricsCallback):

    def on_validation_epoch_end(self, trainer, pl_module):
        """
        usage: 
        def validation_step(self, batch, batch_idx):
            ...
            metric = {'val_loss': loss, 'val_acc': accuracy}
            self.log_dict(metric)
        """
        output = {'epoch': trainer.current_epoch}


def create_rich_progress_bar():
    # refer `https://lightning.ai/docs/pytorch/stable/common/progress_bar.html` for more details.
    from pytorch_lightning.callbacks import RichProgressBar
    from pytorch_lightning.callbacks.progress.rich_progress import \
        RichProgressBarTheme

    return RichProgressBar(theme=RichProgressBarTheme(
        description="green_yellow",
        progress_bar="green1",
        progress_bar_finished="green1",
        progress_bar_pulse="#6206E0",
        batch_progress="green_yellow",
        time="grey82",
        processing_speed="grey82",
        metrics="grey82",
    ))


def build_checkpoint(monitor: str,
                     dirpath: str,
                     prefix: str = None,
                     model: str = None) -> ModelCheckpoint:
    filename = ''
    for x in [prefix, model]:
        if x:
            filename += x + '_'

    if monitor == 'val_f1':
        filename += f'_{{epoch:02d}}_{{val_f1:.4f}}'
    elif monitor == 'val_loss':
        filename += f'_{{epoch:02d}}_{{val_loss:.4f}}'
    elif monitor == 'val_recall':
        filename += f'_{{epoch:02d}}_{{val_recall:.4f}}'
    elif monitor == 'val_precision':
        filename += f'_{{epoch:02d}}_{{val_precision:.4f}}'
    mode = 'min' if 'loss' in monitor else 'max'

    return ModelCheckpoint(monitor=monitor,
                           dirpath=dirpath,
                           filename=filename,
                           save_top_k=1,
                           mode=mode,
                           save_weights_only=True)




