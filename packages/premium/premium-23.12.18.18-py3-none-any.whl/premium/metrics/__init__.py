def f1_loss(y_true, y_pred):
    # lazy import
    import tensorflow as tf
    from tensorflow.keras import backend as K
    tp = K.sum(K.cast(y_true * y_pred, 'float'), axis=0)
    tn = K.sum(K.cast((1 - y_true) * (1 - y_pred), 'float'), axis=0)
    fp = K.sum(K.cast((1 - y_true) * y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true * (1 - y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())
    print(p, r)

    f1 = 2 * p * r / (p + r + K.epsilon())
    # f1 = tf.where(tf.is_nan(f1), tf.zeros_like(f1), f1)
    return 1 - K.mean(f1)


def custom_f1(y_true, y_pred):
    return f1_loss(y_true, y_pred)


def calculate_metrics(ytruth, ypred, average, prefix=None):
    from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                                 recall_score)
    ms = {
        'f1':
        f1_score(ytruth, ypred, zero_division=0, average=average),
        'precision':
        precision_score(ytruth, ypred, zero_division=0, average=average),
        'recall':
        recall_score(ytruth, ypred, zero_division=0, average=average),
        'accuracy':
        accuracy_score(ytruth, ypred, normalize=True)
    }
    if prefix:
        ms = {prefix + '_' + k: v for k, v in ms.items()}
    return ms


def qa_em(pred):
    # qa exact match
    labels = pred.label_ids
    preds = pred.predictions
    start_pos = preds[0].argmax(-1)
    end_post = preds[1].argmax(-1)
    exact_match = 0
    for s, e, l in zip(start_pos, end_post, labels):
        if s == l[0] and e == l[1]:
            exact_match += 1
    return {'em': exact_match / len(labels)}


