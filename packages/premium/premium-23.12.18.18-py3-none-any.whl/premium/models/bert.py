#!/usr/bin/env python3
from enum import Enum


class BERTChineseModels(str, Enum):
    tiny = 'ckiplab/bert-tiny-chinese'
    base = 'bert-base-chinese'
    # https://huggingface.co/hfl/chinese-macbert-base
    macbert = 'hfl/chinese-macbert-base'
    macbert_large = 'hfl/chinese-macbert-large'
    xlnet_base = 'hfl/chinese-xlnet-base'
    roberta = 'hfl/chinese-roberta-wwm-ext'
    roberta_large = 'hfl/chinese-roberta-wwm-ext-large'
    lert_small = 'hfl/chinese-lert-small'
    lert_base = 'hfl/chinese-lert-base' 
    lert_large = 'hfl/chinese-lert-large' 
    distilbert_multi = 'distilbert-base-multilingual-cased'
    ernie = 'nGhuyong/ernie-3.0-base-Zh' # Layer:12, Heads:12, Hidden:768
    ernie_mini = 'nGhuyong/ernie-3.0-mini-Zh' # Layer:6, Heads:12, Hidden:384
    ernie_micro = 'nghuyong/ernie-3.0-micro-zh' # Layer:4, Heads:12, Hidden:384
    ernie_nano = 'nghuyong/ernie-3.0-nano-zh' # Layer:4, Heads:12, Hidden:312


class BERTEnglishModels(str, Enum):
    base = 'bert-base-uncased'
    base_cased = 'bert-base-cased'
    large = 'bert-large-uncased'
    large_cased = 'bert-large-cased'
    xlnet_base = 'xlnet-base-cased'
    xlnet_large = 'xlnet-large-cased'
    tiny = 'prajjwal1/bert-tiny'
    albert_base = 'albert-base-v2'
    albert_large = 'albert-large-v2'
    albert_xlarge = 'albert-xlarge-v2'
    distil = 'distilbert-base-uncased'
    roberta = 'roberta-base'
    roberta_large = 'roberta-large'
    deberta = 'microsoft/deberta-v3-base'
    xlm_roberta = 'xlm-roberta-base' # 100 languages
    base_multilingual_cased='bert-base-multilingual-cased'
    base_multilingual_uncased='bert-base-multilingual-uncased'
    snli = 'symanto/xlm-roberta-base-snli-mnli-anli-xnli' # A strong base model for snli


if __name__ == '__main__':
    print(BERTChineseModels.tiny.value)
