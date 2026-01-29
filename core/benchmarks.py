# core/benchmarks.py
"""
Small benchmarking helpers.

timeit returns the result and elapsed time for a callable.
"""

from __future__ import annotations
import time
from typing import Callable, Any, Dict


def timeit(func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """
    Execute func(*args, **kwargs) and return a dict with result and time in seconds.
    """
    t0 = time.perf_counter()
    res = func(*args, **kwargs)
    t1 = time.perf_counter()
    return {"result": res, "time_s": t1 - t0}
