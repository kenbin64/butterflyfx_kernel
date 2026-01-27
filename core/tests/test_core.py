import unittest

from core.fibonacci import (
    fibonacci_directional_attributes,
    fibonacci_directional_operations,
    fibonacci_sequence,
)
from core.hil import HumanDimensionalState, NamedLens, NamedSubstrate, humanize_state, name_lens, name_substrate
from core.lenses import IdentityLens, StatsLens
from core.substrates import (
    DimensionalState,
    Equation,
    SubstrateDefinition,
    approx_eq,
    generate_cycle,
    phi_scale,
    spawn_at_state,
    spawn_substrate,
)


class TestGenerativeKernel(unittest.TestCase):
    def test_spawn_substrate_implicit_plane(self):
        defn = SubstrateDefinition(
            dim=2, equation=Equation.implicit(lambda p: p[0] + p[1] - 1)
        )
        substrate = spawn_substrate(defn, bounds=[(0, 1), (0, 1)], step=0.5)

        coords = {one.coord for one in substrate.ones}
        expected = {(0.0, 1.0), (0.5, 0.5), (1.0, 0.0)}
        self.assertEqual(coords, expected)

    def test_spawn_substrate_parametric_parabola(self):
        defn = SubstrateDefinition(
            dim=1, equation=Equation.parametric(lambda u: [u[0], u[0] ** 2])
        )
        substrate = spawn_substrate(defn, bounds=[(0, 2)], step=1.0)
        coords = [one.coord for one in substrate.ones]
        self.assertEqual(coords, [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)])

    def test_identity_lens_returns_ones(self):
        defn = SubstrateDefinition(
            dim=1, equation=Equation.parametric(lambda u: [u[0], u[0]])
        )
        substrate = spawn_substrate(defn, bounds=[(0, 1)], step=0.5)
        lens = IdentityLens()
        self.assertEqual(lens.project(substrate), substrate.ones)

    def test_stats_lens_bounds_and_centroid(self):
        defn = SubstrateDefinition(
            dim=1, equation=Equation.parametric(lambda u: [u[0], u[0] ** 2])
        )
        substrate = spawn_substrate(defn, bounds=[(0, 2)], step=1.0)
        stats = StatsLens().project(substrate)

        self.assertEqual(stats["count"], 3)
        self.assertEqual(stats["bounds"], ((0.0, 2.0), (0.0, 4.0)))
        self.assertEqual(stats["centroid"], (1.0, 5 / 3))

    def test_phi_scale_and_generate_cycle(self):
        base = SubstrateDefinition(dim=1, equation=Equation.parametric(lambda u: [u[0]]))
        cycle = generate_cycle(base)
        self.assertEqual(len(cycle), 34)
        self.assertAlmostEqual(cycle[0].scale, phi_scale(1))
        self.assertAlmostEqual(cycle[-1].scale, 1)

    def test_spawn_at_state_scales_bounds(self):
        base = SubstrateDefinition(dim=1, equation=Equation.parametric(lambda u: [u[0]]))
        state = DimensionalState(index=2, scale=phi_scale(2), substrate=base)
        substrate = spawn_at_state(state, bounds=[(0, 1)], step=1.0)
        coords = [one.coord for one in substrate.ones]
        # scale phi^2 ≈ 2.618..., bounds become (0, ~2.618) sampled at step 1
        self.assertEqual(coords, [(0.0,), (1.0,), (2.0,)])

    def test_dimension_mismatch_raises(self):
        defn = SubstrateDefinition(dim=2, equation=Equation.implicit(lambda p: p[0]))
        with self.assertRaises(ValueError):
            spawn_substrate(defn, bounds=[(0, 1)], step=1)

    def test_approximate_equality(self):
        self.assertTrue(approx_eq(1.000001, 1.000002, eps=1e-5))
        self.assertFalse(approx_eq(1.0, 1.1, eps=1e-3))

    def test_fibonacci_sequence(self):
        self.assertEqual(fibonacci_sequence(7), [0, 1, 1, 2, 3, 5, 8])

    def test_fibonacci_directional_attributes_numeric(self):
        attrs = fibonacci_directional_attributes(8, 2)
        self.assertEqual(attrs, {"horizontal_movement": 16, "vertical_movement": 4.0})

    def test_fibonacci_directional_attributes_substrate(self):
        defn = SubstrateDefinition(
            dim=1, equation=Equation.parametric(lambda u: [u[0], u[0] + 1])
        )
        substrate = spawn_substrate(defn, bounds=[(2, 2)], step=1)
        attrs = fibonacci_directional_attributes(substrate)
        self.assertEqual(attrs, {"horizontal_movement": 6.0, "vertical_movement": 0.6666666666666666})

    def test_humanize_state_labels(self):
        base = SubstrateDefinition(dim=1, equation=Equation.parametric(lambda u: [u[0]]))
        first = humanize_state(DimensionalState(index=1, scale=phi_scale(1), substrate=base))
        mid = humanize_state(DimensionalState(index=5, scale=phi_scale(5), substrate=base))
        last = humanize_state(DimensionalState(index=34, scale=1, substrate=base))

        self.assertIsInstance(first, HumanDimensionalState)
        self.assertEqual(first.label, "First Spark")
        self.assertEqual(mid.label, "Expansion φ^5")
        self.assertEqual(last.label, "Collapse / Renewal")

    def test_named_wrappers(self):
        defn = SubstrateDefinition(dim=1, equation=Equation.parametric(lambda u: [u[0]]))
        named_sub = name_substrate("Line", "Unit line", defn)
        lens = IdentityLens()
        named_lens = name_lens("Identity", "Pass-through", lens)

        self.assertIsInstance(named_sub, NamedSubstrate)
        self.assertEqual(named_sub.name, "Line")
        self.assertEqual(named_sub.description, "Unit line")
        self.assertIs(named_sub.defn, defn)

        self.assertIsInstance(named_lens, NamedLens)
        self.assertEqual(named_lens.name, "Identity")
        self.assertEqual(named_lens.description, "Pass-through")
        self.assertIs(named_lens.lens, lens)


if __name__ == "__main__":
    unittest.main()