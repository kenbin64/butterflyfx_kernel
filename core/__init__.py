"""
Core package for ButterflyFX Kernel.

A generative substrate-of-substrates kernel with φ-recursion, observer lenses,
and pure equation-driven manifolds.
"""

__version__ = "0.1.0"

# Core primitives
from core.substrates import (
    Equation,
    One,
    PHI,
    Scalar,
    Substrate,
    SubstrateDefinition,
    Vec,
    approx_eq,
    spawn_substrate,
)

# Optional utilities (import as needed to avoid overhead)
# from core.lenses import Lens, IdentityLens, StatsLens, AggregationLens
# from core.hil import humanize_state, name_substrate, name_lens
# from core.decider import choose_definition, decision_tree_substrate
# from core.sampling import grid_params, random_params, enforce_budget
# from core.transforms import translate_definition, scale_definition
# from core.phi_lens import PhiStepLens, PhiCycleLens

__all__ = [
    "__version__",
    "Equation",
    "One",
    "PHI",
    "Scalar",
    "Substrate",
    "SubstrateDefinition",
    "Vec",
    "approx_eq",
    "spawn_substrate",
]