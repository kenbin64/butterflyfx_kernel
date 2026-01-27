"""Phi-cycle lenses for golden-ratio scaling across 1..33 (+collapse).

These lenses are optional add-ons: they delegate to another lens (e.g.,
IdentityLens, StatsLens, AggregationLens) after spawning/scaling at a given
phi step. They do not modify the core kernel.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List, Sequence, Tuple

from core.lenses import Lens, IdentityLens
from core.substrates import (
    DimensionalState,
    Substrate,
    SubstrateDefinition,
    generate_cycle,
    spawn_at_state,
)


@dataclass(frozen=True)
class PhiStepLens(Lens):
    step_index: int
    projector: Lens
    bounds: Sequence[Tuple[float, float]]
    step: float

    def project(self, sub_def_or_sub: Substrate | SubstrateDefinition) -> dict:
        if isinstance(sub_def_or_sub, Substrate):
            defn = sub_def_or_sub.defn
        else:
            defn = sub_def_or_sub

        cycle = generate_cycle(defn)
        if self.step_index < 1 or self.step_index > len(cycle):
            raise ValueError("step_index out of range for phi cycle")

        state = cycle[self.step_index - 1]
        sub = spawn_at_state(state, bounds=self.bounds, step=self.step)
        proj = self.projector.project(sub)
        return {"step": state.index, "scale": state.scale, "projection": proj}


@dataclass(frozen=True)
class PhiCycleLens(Lens):
    projector: Lens
    bounds: Sequence[Tuple[float, float]]
    step: float
    include_collapse: bool = True

    def project(self, sub_def_or_sub: Substrate | SubstrateDefinition) -> List[dict]:
        if isinstance(sub_def_or_sub, Substrate):
            defn = sub_def_or_sub.defn
        else:
            defn = sub_def_or_sub

        cycle = generate_cycle(defn)
        if not self.include_collapse:
            cycle = cycle[:-1]  # drop collapse stage

        results = []
        for state in cycle:
            sub = spawn_at_state(state, bounds=self.bounds, step=self.step)
            proj = self.projector.project(sub)
            results.append({"step": state.index, "scale": state.scale, "projection": proj})
        return results


__all__ = ["PhiStepLens", "PhiCycleLens"]