# core/lenses.py
"""
Observer lenses: project substrates into summaries.

Includes:
- Lens base class
- IdentityLens
- StatsLens (vectorized)
- AggregationLens (min/max/mean/var)
"""

from __future__ import annotations
from typing import Generic, TypeVar, Tuple, Dict, Any, Optional
import numpy as np
from .substrates import Substrate, One

Projection = TypeVar("Projection")


class Lens(Generic[Projection]):
    """
    Base lens interface. Implementations should override project().
    """
    def project(self, sub: Substrate) -> Projection:
        raise NotImplementedError


class IdentityLens(Lens[Tuple[One, ...]]):
    """
    Return the observed One set unchanged.
    """
    def project(self, sub: Substrate) -> Tuple[One, ...]:
        return sub.ones


class StatsLens(Lens[Dict[str, Any]]):
    """
    Compute simple statistics: count, centroid, bounds.

    Uses NumPy vectorized operations when possible.
    """
    def __init__(self, chunk_size: Optional[int] = None):
        self.chunk_size = chunk_size

    def project(self, sub: Substrate) -> Dict[str, Any]:
        if not sub.ones:
            return {"count": 0, "centroid": (), "bounds": ()}
        coords = np.asarray([o.coord for o in sub.ones], dtype=float)
        mins = coords.min(axis=0)
        maxs = coords.max(axis=0)
        centroid = coords.mean(axis=0)
        return {
            "count": int(coords.shape[0]),
            "centroid": tuple(float(x) for x in centroid),
            "bounds": tuple((float(mins[i]), float(maxs[i])) for i in range(coords.shape[1])),
        }


class AggregationLens(Lens[Dict[str, Any]]):
    """
    Compute min, max, mean, and variance per dimension.
    """
    def __init__(self, chunk_size: Optional[int] = None):
        self.chunk_size = chunk_size

    def project(self, sub: Substrate) -> Dict[str, Any]:
        if not sub.ones:
            return {"count": 0, "min": (), "max": (), "mean": (), "var": ()}
        coords = np.asarray([o.coord for o in sub.ones], dtype=float)
        mins = coords.min(axis=0)
        maxs = coords.max(axis=0)
        means = coords.mean(axis=0)
        diffs = coords - means
        vars_ = (diffs * diffs).mean(axis=0)
        return {
            "count": int(coords.shape[0]),
            "min": tuple(float(x) for x in mins),
            "max": tuple(float(x) for x in maxs),
            "mean": tuple(float(x) for x in means),
            "var": tuple(float(x) for x in vars_),
        }
