# tests/test_lenses.py
"""
Unit tests for core/lenses.py
"""

from core.lenses import StatsLens, IdentityLens
from core.substrates import Substrate, SubstrateDefinition, One, Equation
import numpy as np


def make_simple_substrate():
    # create a tiny substrate with three 3D points
    defn = SubstrateDefinition(dim=2, equation=Equation.parametric(lambda u: u))  # dummy
    ones = (
        One(coord=(0.0, 0.0, 0.0)),
        One(coord=(1.0, 0.0, 0.0)),
        One(coord=(0.0, 1.0, 0.0)),
    )
    return Substrate(defn=defn, ones=ones)


def test_identity_lens_returns_ones():
    sub = make_simple_substrate()
    lens = IdentityLens()
    out = lens.project(sub)
    assert out == sub.ones


def test_stats_lens_centroid_and_bounds():
    sub = make_simple_substrate()
    lens = StatsLens()
    stats = lens.project(sub)
    assert stats["count"] == 3
    # centroid of the three points: (1/3, 1/3, 0)
    assert np.allclose(stats["centroid"], (1.0 / 3.0, 1.0 / 3.0, 0.0))
    # bounds should be ((0,1),(0,1),(0,0))
    assert stats["bounds"][0] == (0.0, 1.0)
    assert stats["bounds"][1] == (0.0, 1.0)
