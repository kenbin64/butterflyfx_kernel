# core/parallel.py
"""
Parallel orchestration helpers.

Provides simple wrappers to map chunked numeric work across processes
or threads. Designed to accept picklable callables for ProcessPoolExecutor.
"""

from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import Callable, Iterable, List, Any


def process_map(func: Callable[[Any], List[Any]], inputs: Iterable, workers: int = 4, chunk_size: int = 100_000) -> List[Any]:
    """
    Map `func` over chunked inputs in separate processes.

    - func: callable that accepts a chunk (list) and returns a list of results
    - inputs: iterable of items to chunk
    - workers: number of processes
    - chunk_size: size of each chunk passed to func
    """
    from .sampling import chunked
    results: List[Any] = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(func, chunk) for chunk in chunked(inputs, chunk_size)]
        for fut in as_completed(futures):
            results.extend(fut.result())
    return results


def thread_map(func: Callable[[Any], Any], inputs: Iterable, workers: int = 8) -> List[Any]:
    """
    Map `func` over inputs using threads (useful for I/O-bound tasks).
    """
    results: List[Any] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(func, item) for item in inputs]
        for fut in as_completed(futures):
            results.append(fut.result())
    return results
