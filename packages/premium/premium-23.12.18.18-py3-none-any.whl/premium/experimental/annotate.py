#!/usr/bin/env python3 
import codefast as cf 
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from xgboost import XGBClassifier

def train_classifier(train_df):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(train_df['text'] + ' ' + train_df['source'])
    y = train_df['label'] % 10 - 1
    cf.info({
        'X shape': X.shape,
        'y shape': y.shape,
    })
    # multi classifiation
    clf = XGBClassifier(objective='multi:softmax', num_class=5)
    clf.fit(X, y)
    cf.info("Training process completed")
    return clf, vectorizer


def annodate(clf, golden, samples, vectorizer):
    results = []
    for i, row in samples.iterrows():
        text = row['text'] + ' ' + row['source']
        X_test = vectorizer.transform([text])
        pred = clf.predict(X_test)[0] + 1
        print(f"Predicted label for '{text}': ")
        res = input("Is this correct? (y/n) ")
        if res.lower() == 'y':
            label = pred
        else:
            try:
                label = int(res)
            except ValueError:
                continue
        row['label'] = label
        results.append(row)

    df = pd.DataFrame(results)
    golden = pd.concat([golden, df])
    return golden
