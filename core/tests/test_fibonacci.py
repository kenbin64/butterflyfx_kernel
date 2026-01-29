# tests/test_fibonacci.py
"""
Unit tests for core/fibonacci.py
"""

from core.fibonacci import build_custom_fib_cycle, fibonacci_squares, PHI
import math


def test_build_custom_fib_cycle_domain_mode():
    seq = [0, 1, 1, 2, 3]
    cycle = build_custom_fib_cycle(seq, mode="domain")
    assert len(cycle) == len(seq)
    # check scales equal fib values (with 0 mapped to 1.0)
    assert cycle[0].scale == 1.0
    assert cycle[1].scale == 1.0
    assert cycle[4].scale == 3.0


def test_build_custom_fib_cycle_phi_modes():
    seq = [0, 1, 1]
    c_index = build_custom_fib_cycle(seq, mode="phi_index")
    c_fib = build_custom_fib_cycle(seq, mode="phi_fib")
    # phi_index: scale = PHI ** index
    assert math.isclose(c_index[0].scale, PHI ** 1)
    # phi_fib: scale = PHI ** fib_value (fib_value 1 -> PHI)
    assert math.isclose(c_fib[1].scale, PHI ** 1)


def test_fibonacci_squares_small():
    sq = fibonacci_squares(5)
    assert sq == [1, 1, 2, 3, 5]
