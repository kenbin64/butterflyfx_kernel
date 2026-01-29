# core/sampling.py
"""
Sampling utilities: deterministic grid generator, random vectorized sampler,
and chunking helpers.

Design goals:
- Avoid float accumulation drift by using integer counters.
- Provide generators for large grids to keep memory bounded.
- Provide a vectorized random sampler using NumPy.
"""

from __future__ import annotations
from typing import Sequence, Tuple, Iterator, List, Optional
import math
import numpy as np

Bounds = Sequence[Tuple[float, float]]


def estimate_grid_count(bounds: Bounds, step: float) -> int:
    """
    Estimate the number of grid points for given bounds and step.

    Raises ValueError for invalid inputs.
    """
    if step <= 0:
        raise ValueError("step must be positive")
    count = 1
    for mn, mx in bounds:
        if mx < mn:
            raise ValueError("each bound must have mn <= mx")
        n = int(math.floor((mx - mn) / step)) + 1
        count *= max(0, n)
    return count


def grid_params_generator(bounds: Bounds, step: float) -> Iterator[List[float]]:
    """
    Lazily generate parameter vectors on a regular grid.

    Uses integer-index odometer to avoid cumulative float drift.
    Yields lists of floats of length len(bounds).
    """
    if step <= 0:
        raise ValueError("step must be positive")

    dims = len(bounds)
    counts: List[int] = []
    mins: List[float] = []
    for mn, mx in bounds:
        cnt = int(math.floor((mx - mn) / step)) + 1
        counts.append(cnt)
        mins.append(float(mn))

    # Odometer indices
    indices = [0] * dims
    total = 1
    for c in counts:
        total *= c

    for _ in range(total):
        yield [mins[i] + indices[i] * step for i in range(dims)]
        # increment odometer
        for i in range(dims - 1, -1, -1):
            indices[i] += 1
            if indices[i] < counts[i]:
                break
            indices[i] = 0


def random_params_np(bounds: Bounds, count: int, seed: Optional[int] = None) -> np.ndarray:
    """
    Vectorized random sampling using NumPy.

    Returns an array of shape (count, len(bounds)).
    """
    if count < 0:
        raise ValueError("count must be non-negative")
    rng = np.random.default_rng(seed)
    lows = np.array([mn for mn, _ in bounds], dtype=float)
    highs = np.array([mx for _, mx in bounds], dtype=float)
    u = rng.random((count, len(bounds)), dtype=float)
    return lows + (highs - lows) * u


def chunked(iterable, chunk_size: int):
    """
    Yield successive chunks (lists) of up to chunk_size from iterable.

    Useful for batching grid evaluation.
    """
    it = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(chunk_size):
                chunk.append(next(it))
        except StopIteration:
            if chunk:
                yield chunk
            break
        yield chunk
