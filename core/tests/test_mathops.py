# tests/test_mathops.py
"""
Unit tests for core/mathops.py
"""

import numpy as np
from core import mathops


def test_safe_mul_scalar_and_array():
    # scalar * scalar
    assert float(mathops.safe_mul(2, 3)) == 6.0
    # array * scalar
    res = mathops.safe_mul([1, 2, 3], 2)
    assert np.allclose(res, np.array([2.0, 4.0, 6.0]))


def test_safe_div_zero_handling():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([1.0, 0.0, 2.0])
    res = mathops.safe_div(a, b, fill=-1.0)
    assert np.allclose(res, np.array([1.0, -1.0, 1.5]))


def test_pair_sum_diff_and_inverse_roundtrip():
    a = np.array([5, 7, 9])
    b = np.array([2, 3, 4])
    s, d = mathops.pair_sum_diff(a, b)
    a2, b2 = mathops.pair_sum_diff_inverse(s, d)
    # inverse uses integer-style floor division; check that values are integers and consistent
    assert np.all((a2 == (s + d) // 2))
    assert np.all((b2 == (s - d) // 2))
