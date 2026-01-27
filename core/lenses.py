"""Lenses: observers that collapse potential into meaning."""

from __future__ import annotations

from typing import Generic, Iterable, List, Optional, Tuple, TypeVar

from core.substrates import One, Substrate

Projection = TypeVar("Projection")


class Lens(Generic[Projection]):
    """Base observer interface."""

    def project(self, sub: Substrate) -> Projection:  # pragma: no cover - interface
        raise NotImplementedError


class IdentityLens(Lens[Tuple[One, ...]]):
    """Returns the observed 1-set unchanged."""

    def project(self, sub: Substrate) -> Tuple[One, ...]:
        return sub.ones


class StatsLens(Lens[dict]):
    """Reduces a substrate to simple statistics (count, centroid, bounds)."""

    def project(self, sub: Substrate) -> dict:
        if not sub.ones:
            return {"count": 0, "centroid": (), "bounds": ()}

        dims = len(sub.ones[0].coord)
        coords = [one.coord for one in sub.ones]
        mins = [min(c[i] for c in coords) for i in range(dims)]
        maxs = [max(c[i] for c in coords) for i in range(dims)]
        centroid = [sum(c[i] for c in coords) / len(coords) for i in range(dims)]

        return {
            "count": len(sub.ones),
            "centroid": tuple(centroid),
            "bounds": tuple(zip(mins, maxs)),
        }


class AggregationLens(Lens[dict]):
    """Computes min, max, mean, and variance per dimension."""

    def project(self, sub: Substrate) -> dict:
        if not sub.ones:
            return {"count": 0, "min": (), "max": (), "mean": (), "var": ()}

        dims = len(sub.ones[0].coord)
        coords = [one.coord for one in sub.ones]
        mins = [min(c[i] for c in coords) for i in range(dims)]
        maxs = [max(c[i] for c in coords) for i in range(dims)]
        means = [sum(c[i] for c in coords) / len(coords) for i in range(dims)]

        variances = []
        for i in range(dims):
            mean_i = means[i]
            variances.append(sum((c[i] - mean_i) ** 2 for c in coords) / len(coords))

        return {
            "count": len(coords),
            "min": tuple(mins),
            "max": tuple(maxs),
            "mean": tuple(means),
            "var": tuple(variances),
        }


__all__ = ["Lens", "IdentityLens", "StatsLens", "AggregationLens"]