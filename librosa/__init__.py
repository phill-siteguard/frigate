"""Minimal stub of librosa for unit tests."""

import numpy as np


def load(fname, sr=22050, dtype=np.float32, *args, **kwargs):  # pragma: no cover
    """Return silence with the requested dtype and sample rate."""

    duration = sr  # 1 second of audio by default
    return np.zeros(duration, dtype=dtype), sr

