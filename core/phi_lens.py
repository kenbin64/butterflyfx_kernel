# core/phi_lenses.py
"""
Phi-step and Phi-cycle lenses that spawn scaled substrates across the
custom Fibonacci cycle and apply a projector lens to each spawned substrate.

This module uses the domain sequence [0,1,1,2,3,5,8,13,21,33] by default.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, List, Dict, Any
from .fibonacci import build_custom_fib_cycle, DimensionalState
from .substrates import Substrate, SubstrateDefinition
from .transform import spawn_substrate_vectorized

# Default custom sequence (domain semantic)
DEFAULT_CUSTOM_SEQ = [0, 1, 1, 2, 3, 5, 8, 13, 21, 33]


@dataclass(frozen=True)
class PhiStepLens:
    """
    Spawn and project a single phi step.

    - step_index: 1-based index into the custom cycle
    - projector: a Lens instance
    - bounds, step: sampling parameters passed to spawn_substrate_vectorized
    """
    step_index: int
    projector: object
    bounds: Sequence[tuple]
    step: float

    def project(self, sub_def_or_sub: Substrate | SubstrateDefinition) -> Dict[str, Any]:
        # Resolve definition
        if isinstance(sub_def_or_sub, Substrate):
            defn = sub_def_or_sub.defn
        else:
            defn = sub_def_or_sub

        cycle = build_custom_fib_cycle(DEFAULT_CUSTOM_SEQ, mode="domain")
        if self.step_index < 1 or self.step_index > len(cycle):
            raise ValueError("step_index out of range for phi cycle")
        state = cycle[self.step_index - 1]

        # Spawn substrate at this state's scale (scale can be used to scale bounds)
        scaled_bounds = [(mn * state.scale, mx * state.scale) for mn, mx in self.bounds]
        sub = spawn_substrate_vectorized(defn, scaled_bounds, self.step)
        proj = self.projector.project(sub)
        return {"step": state.index, "scale": state.scale, "projection": proj}


@dataclass(frozen=True)
class PhiCycleLens:
    """
    Iterate the full custom cycle, spawn and project each state.

    - projector: Lens instance
    - bounds, step: sampling parameters
    - include_collapse: whether to include final collapse stage
    - workers: reserved for future parallelism (not used in this simple implementation)
    """
    projector: object
    bounds: Sequence[tuple]
    step: float
    include_collapse: bool = True
    workers: int = 1

    def project(self, sub_def_or_sub: Substrate | SubstrateDefinition) -> List[Dict[str, Any]]:
        if isinstance(sub_def_or_sub, Substrate):
            defn = sub_def_or_sub.defn
        else:
            defn = sub_def_or_sub

        cycle = build_custom_fib_cycle(DEFAULT_CUSTOM_SEQ, mode="domain")
        if not self.include_collapse:
            cycle = cycle[:-1]

        results: List[Dict[str, Any]] = []
        for state in cycle:
            scaled_bounds = [(mn * state.scale, mx * state.scale) for mn, mx in self.bounds]
            sub = spawn_substrate_vectorized(defn, scaled_bounds, self.step)
            proj = self.projector.project(sub)
            results.append({"step": state.index, "scale": state.scale, "projection": proj})
        return results
