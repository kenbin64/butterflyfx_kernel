# core/connection_manager.py
"""
Directional connection manager.

Provides simple helpers to establish connections in horizontal (parallel),
vertical (hierarchical), or spiral (alternating) patterns. This module is
I/O-agnostic and expects a user-provided connect_fn that performs the actual
connection work.
"""

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Callable, Any, List


class DirectionalConnectionManager:
    """
    Manage connections using directional strategies.
    """
    def __init__(self):
        pass

    def connect_horizontal(self, endpoints: Iterable[str], connect_fn: Callable[[str], Any], workers: int = 8) -> List[Any]:
        """
        Establish connections in parallel (horizontal semantics).
        """
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = [ex.submit(connect_fn, e) for e in endpoints]
            return [f.result() for f in futures]

    def connect_vertical(self, layers: Iterable[Iterable[str]], connect_fn: Callable[[str], Any]) -> List[List[Any]]:
        """
        Establish connections layer-by-layer (vertical semantics).
        """
        results = []
        for layer in layers:
            layer_res = [connect_fn(e) for e in layer]
            results.append(layer_res)
        return results

    def connect_spiral(self, sequence: Iterable[str], connect_fn: Callable[[str], Any]) -> List[Any]:
        """
        Connect following a spiral sequence (alternating semantics).
        """
        return [connect_fn(s) for s in sequence]
