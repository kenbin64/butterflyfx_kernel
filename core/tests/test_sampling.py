# tests/test_sampling.py
"""
Unit tests for core/sampling.py
"""

import numpy as np
import pytest
from core import sampling


def test_estimate_grid_count_and_generator_small():
    bounds = [(0.0, 0.0), (0.0, 0.0)]
    # only one point expected
    cnt = sampling.estimate_grid_count(bounds, step=1.0)
    assert cnt == 1
    gen = sampling.grid_params_generator(bounds, step=1.0)
    pts = list(gen)
    assert pts == [[0.0, 0.0]]


def test_random_params_np_shape_and_range():
    bounds = [(0.0, 1.0), (-1.0, 1.0)]
    arr = sampling.random_params_np(bounds, count=100, seed=42)
    assert arr.shape == (100, 2)
    # values within bounds
    assert np.all(arr[:, 0] >= 0.0) and np.all(arr[:, 0] <= 1.0)
    assert np.all(arr[:, 1] >= -1.0) and np.all(arr[:, 1] <= 1.0)


def test_chunked_yields_chunks():
    it = iter(range(7))
    chunks = list(sampling.chunked(it, chunk_size=3))
    assert chunks == [[0, 1, 2], [3, 4, 5], [6]]
