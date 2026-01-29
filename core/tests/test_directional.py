# tests/test_directional.py
"""
Unit tests for core/directional.py
"""

import numpy as np
from core.directional import traverse_horizontal, traverse_vertical


def test_traverse_horizontal_and_vertical_scalar():
    # horizontal multiply
    assert traverse_horizontal(2, 3) == 6.0
    # vertical divide with nonzero denominator
    assert traverse_vertical(6, 3) == 2.0
    # vertical divide by zero returns 0.0 (safe_div default)
    assert traverse_vertical(1.0, 0.0) == 0.0


def test_traverse_with_arrays():
    a = np.array([1.0, 2.0])
    b = np.array([3.0, 4.0])
    h = traverse_horizontal(a, b)
    v = traverse_vertical(a, b)
    assert np.allclose(h, np.array([3.0, 8.0]))
    assert np.allclose(v, np.array([1.0 / 3.0, 2.0 / 4.0]))
