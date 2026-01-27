"""Sampling utilities for substrate generation.

Provides simple grid and random samplers plus a budget guard to avoid
runaway sampling. These helpers are optional and do not alter the core
`spawn_substrate` API.
"""

from __future__ import annotations

import random
from typing import Callable, Iterable, List, Sequence, Tuple

from core.substrates import Scalar

Bounds = Sequence[Tuple[Scalar, Scalar]]


def grid_params(bounds: Bounds, step: Scalar) -> List[List[Scalar]]:
    """Generate grid-sampled parameter vectors within bounds."""

    params: List[List[Scalar]] = []

    def recurse(curr: List[Scalar], idx: int) -> None:
        if idx == len(bounds):
            params.append(list(curr))
            return
        mn, mx = bounds[idx]
        v = mn
        while v <= mx + 1e-12:
            recurse([*curr, v], idx + 1)
            v += step

    recurse([], 0)
    return params


def random_params(bounds: Bounds, count: int, rng: Callable[[], float] | None = None) -> List[List[Scalar]]:
    """Generate randomly sampled parameter vectors within bounds."""

    r = rng or random.random
    params: List[List[Scalar]] = []
    for _ in range(count):
        params.append([mn + (mx - mn) * r() for mn, mx in bounds])
    return params


def enforce_budget(items: Sequence, max_count: int | None) -> List:
    """Trim sequence to budget if provided."""

    if max_count is None:
        return list(items)
    return list(items[:max_count])


__all__ = ["grid_params", "random_params", "enforce_budget", "Bounds"]