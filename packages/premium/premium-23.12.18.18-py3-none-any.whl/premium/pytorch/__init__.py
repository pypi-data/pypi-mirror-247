#!/usr/bin/env python3

from typing import List, Tuple

import torch
import torch.nn.functional as F


def pad_sequence(inputs: List[List[int]],
                 max_size: int,
                 value: int = 0,
                 return_first: bool = False) -> List[List[int]]:
    assert isinstance(inputs, list), "inputs must be a list"
    assert isinstance(inputs[0], list), "inputs must be a list of list"
    results = F.pad(torch.tensor(inputs), (0, max_size - len(inputs[0])),
                    'constant', value).tolist()
    if return_first:
        return results[0]
    return results


class BatchCollector(object):

    def __init__(self, device: torch.device = None) -> None:
        self.device = device if device else torch.device("cpu")
        self.text = None
        self.label = None
        self.offsets = None

    def __call__(self, inputs) -> Tuple[torch.Tensor, torch.Tensor]:
        batch = {}
        tokens, labels, offsets = [], [], [0]
        for b in inputs:
            tokens.append(b['text'])
            labels.append(b['label'])
            offsets.append(b['text'].size(0))
        batch['text'] = torch.cat(tokens)
        batch['label'] = torch.tensor(labels)
        batch["offset"] = torch.tensor(offsets[:-1]).cumsum(dim=0)
        self.batch = batch
        return self

    def __getitem__(self, key: str):
        return self.batch[key].to(self.device)
