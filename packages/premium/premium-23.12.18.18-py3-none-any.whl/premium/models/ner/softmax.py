# --------------------------------------------
import os

import codefast as cf
import pandas as pd
import torch
from rich import print
from torch.utils.data import DataLoader, Dataset, random_split
from transformers import (AutoModelForTokenClassification, AutoTokenizer,
                          BertForTokenClassification, BertModel, BertTokenizer,
                          EarlyStoppingCallback, Trainer, TrainingArguments)

import premium as pm
from premium.models.bert import BERTChineseModels

TOKENIZERS_PARALLELISM = False

base_model = BERTChineseModels.roberta.value
base_model = BERTChineseModels.ernie_mini.value
tokenizer = AutoTokenizer.from_pretrained(base_model)
softmax_model = AutoModelForTokenClassification.from_pretrained(base_model)
tag2idx = {'O': 0, 'B': 1, 'I': 2, 'S': 3}


class InputExample(Dataset):

    def __init__(self,
                 df: pd.DataFrame,
                 tokenizer: BertTokenizer,
                 max_len: int = 512,
                 for_train=True):
        self.df = df
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.for_train = for_train

    def __len__(self):
        return len(self.df)

    def padding(self, input_ids, masks, labels):
        input_ids = input_ids + [0] * (self.max_len - len(input_ids))
        masks = masks + [0] * (self.max_len - len(masks))
        labels = labels + [0] * (self.max_len - len(labels))
        return input_ids, masks, labels

    def __getitem__(self, idx):
        tokens = self.df['tokens'].iloc[idx]
        if self.for_train:
            tags = [tag2idx[t] for t in self.df['tags'].iloc[idx]]
        else:
            tags = [0] * len(tokens)
        tokens = tokens[:self.max_len - 2]
        tags = tags[:self.max_len - 2]
        input_ids, masks, labels = [101], [1], [0]
        for i, t in enumerate(tokens):
            ids = self.tokenizer.encode(t, add_special_tokens=False)
            if not ids:
                ids.append(101)
            for _id in ids:
                input_ids.append(_id)
                masks.append(1)
                labels.append(tags[i])

        input_ids.append(102)
        masks.append(1)
        labels.append(0)
        input_ids, masks, labels = self.padding(input_ids, masks, labels)

        if self.for_train:
            return {
                'input_ids': torch.tensor(input_ids),
                'attention_mask': torch.tensor(masks),
                'labels': torch.tensor(labels),
            }
        else:
            return {
                'input_ids': torch.tensor(input_ids),
                'attention_mask': torch.tensor(masks),
            }


class DataCollator:

    def __call__(self, epoch):
        input_ids = torch.stack([f['input_ids'] for f in epoch])
        attention_mask = torch.stack([f['attention_mask'] for f in epoch])
        labels = None
        if 'labels' in epoch[0]:
            labels = torch.stack([f['labels'] for f in epoch])
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels,
        }


def calculate_metrics(preds):
    from sklearn_crfsuite.metrics import flat_classification_report as fcr
    labels = preds.label_ids
    predictions = preds.predictions.argmax(-1)
    tags = [1, 2]
    for t in range(3, 10):
        if t in labels:
            tags.append(t)
    tags = list(set(tags))
    metrics = fcr(labels,
                  predictions,
                  labels=tags,
                  output_dict=True,
                  digits=4,
                  zero_division=0)
    return {
        'precision': metrics['weighted avg']['precision'],
        'recall': metrics['weighted avg']['recall'],
        'f1': metrics['weighted avg']['f1-score'],
        'support': metrics['weighted avg']['support'],
    }


def get_examples(tag_type: str, sentence_len_type: int = 5):
    df = None
    df.sort_values('conversation_id', inplace=True)
    X, Xv = pm.ttsplit_df(df, test_size=0.1, random_state=2023, shuffle=False)
    train_examples = InputExample(X, tokenizer)
    val_examples = InputExample(Xv, tokenizer)
    return train_examples, val_examples


def create_trainer(model, train_examples, val_examples, epochs=20):
    train_args = TrainingArguments(
        evaluation_strategy='epoch',
        output_dir='/data/tmp/logs',
        overwrite_output_dir=True,
        num_train_epochs=epochs,     # total number of training epochs
        per_device_train_batch_size=8,     # batch size per device during training
        per_device_eval_batch_size=8,     # batch size for evaluation
        warmup_steps=500,     # number of warmup steps for learning rate scheduler
        weight_decay=0.01,     # strength of weight decay
        report_to='none',
        save_total_limit=1,
        save_strategy='epoch',
        metric_for_best_model='f1',
        load_best_model_at_end=True,
        eval_steps=500,
        logging_steps=500,
        fp16=True,
     # no_cuda=True
    )

    return Trainer(
        model=model,
        args=train_args,
        train_dataset=train_examples,
        eval_dataset=val_examples,
        data_collator=DataCollator(),
        compute_metrics=calculate_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=7)],
    )


def do_train(tag_type: str, epochs: int = 10):
    train_examples, val_examples = get_examples(tag_type, sentence_len_type=7)
    model = AutoModelForTokenClassification.from_pretrained(base_model,
                                                            num_labels=3)
    export_path = '/data/tmp/softmax/{}'.format(tag_type)

    if os.path.exists(export_path):
        cf.info('skip training {}'.format(tag_type))
        return

    trainer = create_trainer(model, train_examples, val_examples, epochs=epochs)
    res = trainer.train()
    trainer.save_model(export_path)
    print(res)
    return trainer


def make_prediction(tag_type: str):
    cf.info('evaluate....')
    _, val_examples = get_examples(tag_type, sentence_len_type=7)
    model = AutoModelForTokenClassification.from_pretrained('/data/tmp/softmax',
                                                            num_labels=3)
    trainer = create_trainer(model, None, val_examples)
    metrics = trainer.evaluate()
    print(metrics)
    return metrics
