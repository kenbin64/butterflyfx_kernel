# core/atomic_lens_system.py
"""
High-level orchestration of lens arrays.

- DirectionalLensArray: apply many lenses in parallel (horizontal)
- HierarchicalLensLayer: apply layers of lenses sequentially (vertical)
"""

from __future__ import annotations
from typing import Iterable, Callable, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed


class DirectionalLensArray:
    """
    Apply a collection of lenses in parallel to a substrate.
    """
    def __init__(self, lenses: Iterable[Callable]):
        self.lenses = list(lenses)

    def apply_parallel(self, substrate, workers: int = 8) -> List[Any]:
        results = []
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = {ex.submit(l.project, substrate): l for l in self.lenses}
            for fut in as_completed(futures):
                results.append(fut.result())
        return results


class HierarchicalLensLayer:
    """
    Apply layers of lenses sequentially; each layer receives the output of the previous.
    """
    def __init__(self, layers: List[Iterable[Callable]]):
        self.layers = layers

    def apply(self, substrate):
        current = substrate
        results = []
        for layer in self.layers:
            layer_res = [l.project(current) for l in layer]
            results.append(layer_res)
        return results
