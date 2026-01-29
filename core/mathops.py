# core/mathops.py
"""
Pure numeric primitives and safe arithmetic helpers.

This module contains small, single-purpose functions used throughout the
core pipeline. All functions prefer NumPy arrays and are vectorized where
possible. Keep this file dependency-light and math-focused.
"""

from __future__ import annotations
from typing import Tuple
import numpy as np

Scalar = float

def safe_mul(a, b):
    """
    Elementwise multiplication with NumPy coercion.

    Accepts scalars, lists, or numpy arrays. Returns a numpy array.
    """
    a_arr = np.asarray(a, dtype=float)
    b_arr = np.asarray(b, dtype=float)
    return a_arr * b_arr


def safe_div(a, b, fill: float = 0.0):
    """
    Elementwise safe division.

    Where denominator is zero, returns `fill`. Works with broadcasting.
    """
    a_arr = np.asarray(a, dtype=float)
    b_arr = np.asarray(b, dtype=float)
    return np.where(b_arr != 0.0, a_arr / b_arr, fill)


def pair_sum_diff(a, b) -> Tuple[np.ndarray, np.ndarray]:
    """
    Reversible pair transform (vectorized).

    Returns (s, d) where s = a + b and d = a - b.
    """
    a_arr = np.asarray(a)
    b_arr = np.asarray(b)
    return a_arr + b_arr, a_arr - b_arr


def pair_sum_diff_inverse(s, d) -> Tuple[np.ndarray, np.ndarray]:
    """
    Inverse of pair_sum_diff using integer-style inversion.

    Uses floor division semantics for integer-like reversibility.
    """
    s_arr = np.asarray(s)
    d_arr = np.asarray(d)
    a = (s_arr + d_arr) // 2
    b = (s_arr - d_arr) // 2
    return a, b
