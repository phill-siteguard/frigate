"""Minimal transformers stub for tests."""

import os

import numpy as np

__all__ = ["AutoFeatureExtractor", "AutoTokenizer"]


class _BaseTokenizer:
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir

    @classmethod
    def from_pretrained(cls, model_name, cache_dir=None, **kwargs):
        os.makedirs(cache_dir or "./tokenizer", exist_ok=True)
        return cls(cache_dir=cache_dir)

    def save_pretrained(self, path):
        os.makedirs(path, exist_ok=True)

    def encode(self, text):
        return [0]

    def __call__(
        self,
        text,
        padding=None,
        truncation=None,
        max_length=None,
        return_tensors=None,
        **kwargs,
    ):
        length = max_length or max(len(text), 1)
        data = np.zeros((1, length), dtype=np.int64)
        return {"input_ids": data, "attention_mask": data}


class AutoTokenizer(_BaseTokenizer):
    pass


class AutoFeatureExtractor:
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir

    @classmethod
    def from_pretrained(cls, cache_dir, **kwargs):
        os.makedirs(cache_dir, exist_ok=True)
        return cls(cache_dir=cache_dir)

    def __call__(self, images, return_tensors=None, **kwargs):
        return {
            "pixel_values": np.zeros((1, 3, 224, 224), dtype=np.float32),
        }

