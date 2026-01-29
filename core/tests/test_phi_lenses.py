# tests/test_phi_lenses.py
"""
Unit tests for core/phi_lenses.py

These tests use degenerate bounds (single point) so spawn_substrate_vectorized
produces a single, deterministic point for each phi state.
"""

from core.phi_lenses import PhiCycleLens, PhiStepLens
from core.transform import z_xy2_parametric
from core.lenses import StatsLens


def test_phi_step_lens_single_point():
    defn = z_xy2_parametric()
    # degenerate bounds produce a single parameter vector (0,0)
    bounds = [(0.0, 0.0), (0.0, 0.0)]
    step = 1.0
    projector = StatsLens()
    step_lens = PhiStepLens(step_index=1, projector=projector, bounds=bounds, step=step)
    out = step_lens.project(defn)
    assert out["step"] == 1
    assert "projection" in out
    assert out["projection"]["count"] == 1


def test_phi_cycle_lens_length_and_projection():
    defn = z_xy2_parametric()
    bounds = [(0.0, 0.0), (0.0, 0.0)]
    projector = StatsLens()
    cycle_lens = PhiCycleLens(projector=projector, bounds=bounds, step=1.0, include_collapse=True)
    results = cycle_lens.project(defn)
    # default custom sequence length is 10
    assert len(results) == 10
    # each projection should be present and count==1
    for r in results:
        assert "projection" in r
        assert r["projection"]["count"] == 1
