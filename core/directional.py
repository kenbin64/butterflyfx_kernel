# core/directional.py
"""
Directional algebra mapping edges to arithmetic operations.

- Horizontal traversal => multiplication (parallel semantics)
- Vertical traversal => division (hierarchical semantics)

These functions are intentionally small and composable.
"""

from __future__ import annotations
import numpy as np
from .mathops import safe_mul, safe_div


def traverse_horizontal(a, b):
    """
    Horizontal edge traversal: multiply a and b elementwise.

    Accepts scalars, lists, or numpy arrays.
    """
    return safe_mul(a, b)


def traverse_vertical(a, b):
    """
    Vertical edge traversal: divide a by b safely.

    Where b == 0, returns 0 by default.
    """
    return safe_div(a, b, fill=0.0)


def apply_edge_sequence(values, edges):
    """
    Apply a sequence of edge traversals to `values`.

    - values: initial numeric value or array
    - edges: iterable of 'H' (horizontal) or 'V' (vertical)
    """
    v = values
    for e in edges:
        if e == "H":
            v = traverse_horizontal(v, v)
        elif e == "V":
            v = traverse_vertical(v, v)
        else:
            raise ValueError("edge must be 'H' or 'V'")
    return v
