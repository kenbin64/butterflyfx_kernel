# core/fibonacci.py
"""
Fibonacci staircase and cycle utilities.

Provides:
- build_custom_fib_cycle(seq, mode): build DimensionalState list from a custom sequence.
- fibonacci_squares(n): helper to produce Fibonacci square sizes.
- fibonacci_spiral_coords(n): simple placement helper (optional).
"""

from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
from typing import List, Tuple

PHI = (1 + sqrt(5)) / 2


@dataclass(frozen=True)
class DimensionalState:
    """
    Represents a level in the Fibonacci staircase.

    - index: ordinal position (1..N)
    - fib_value: the Fibonacci-like number assigned to this level
    - scale: numeric scale used when spawning
    - label: human-readable label
    """
    index: int
    fib_value: int
    scale: float
    label: str = ""


def build_custom_fib_cycle(seq: List[int], mode: str = "domain") -> List[DimensionalState]:
    """
    Build a cycle of DimensionalState objects from a custom sequence.

    seq: e.g. [0,1,1,2,3,5,8,13,21,33]
    mode:
      - "domain": scale = fib_value (domain semantic)
      - "phi_index": scale = PHI ** index
      - "phi_fib": scale = PHI ** fib_value
    """
    states: List[DimensionalState] = []
    for i, fv in enumerate(seq, start=1):
        if mode == "domain":
            scale = float(fv) if fv != 0 else 1.0
        elif mode == "phi_index":
            scale = PHI ** i
        elif mode == "phi_fib":
            scale = PHI ** fv if fv != 0 else 1.0
        else:
            raise ValueError("unknown mode for build_custom_fib_cycle")
        label = f"Level {i} (F={fv})"
        states.append(DimensionalState(index=i, fib_value=fv, scale=scale, label=label))
    return states


def fibonacci_squares(n: int) -> List[int]:
    """
    Return the first n Fibonacci numbers (starting from 1,1,...).

    Useful for geometric tiling sizes.
    """
    if n <= 0:
        return []
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


def fibonacci_spiral_coords(n: int) -> List[Tuple[int, int, int, int]]:
    """
    Simple placement algorithm for n Fibonacci squares.

    Returns a list of tuples (x, y, size, orientation_index).
    This is a helper for visualization and tiling; not used in core math.
    """
    sizes = fibonacci_squares(n)
    x = y = 0
    coords = []
    dir_idx = 0
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for s in sizes:
        dx, dy = dirs[dir_idx % 4]
        coords.append((x, y, s, dir_idx % 4))
        x += dx * s
        y += dy * s
        dir_idx += 1
    return coords
