# tests/test_transform.py
"""
Unit tests for core/transform.py and the z = x * y^2 substrate.
"""

import numpy as np
from core.transform import z_xy2_parametric, spawn_substrate_vectorized
from core.substrates import SubstrateDefinition


def test_z_xy2_parametric_mapping():
    defn = z_xy2_parametric()
    # small batch of parameter vectors
    params = np.array([[2.0, 3.0], [1.0, -2.0]])
    out = defn.equation.g(params)
    # expected z values: x * y^2
    expected = np.array([[2.0, 3.0, 2.0 * 9.0], [1.0, -2.0, 1.0 * 4.0]])
    assert np.allclose(out, expected)


def test_spawn_substrate_vectorized_single_point():
    defn = z_xy2_parametric()
    # bounds that collapse to a single parameter vector (0,0)
    bounds = [(0.0, 0.0), (0.0, 0.0)]
    sub = spawn_substrate_vectorized(defn, bounds, step=1.0, chunk_size=10)
    # one One object with coord (0.0, 0.0, 0.0)
    assert len(sub.ones) == 1
    assert tuple(sub.ones[0].coord) == (0.0, 0.0, 0.0)
