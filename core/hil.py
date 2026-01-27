"""Human Interface Layer wrappers for the generative kernel.

Provides human-friendly naming and labeling around substrates, lenses,
and dimensional states without changing underlying math semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.lenses import Lens
from core.substrates import DimensionalState, SubstrateDefinition


@dataclass(frozen=True)
class NamedSubstrate:
    """Human-friendly wrapper around a substrate definition."""

    name: str
    description: str
    defn: SubstrateDefinition

    @property
    def def_(self) -> SubstrateDefinition:  # compatibility accessor
        return self.defn

    def as_dict(self) -> dict:
        return {"name": self.name, "description": self.description, "def": self.defn}


@dataclass(frozen=True)
class HumanDimensionalState:
    """Labeled dimensional state for easier human comprehension."""

    label: str
    index: int
    scale: float

    def as_dict(self) -> dict:
        return {"label": self.label, "index": self.index, "scale": self.scale}


@dataclass(frozen=True)
class NamedLens:
    """Human-friendly description of a lens observer."""

    name: str
    description: str
    lens: Lens[Any]

    def as_dict(self) -> dict:
        return {"name": self.name, "description": self.description, "lens": self.lens}


def humanize_state(state: DimensionalState) -> HumanDimensionalState:
    """Wrap a DimensionalState with a human-readable label."""

    if state.index == 1:
        label = "First Spark"
    elif state.index == 34:
        label = "Collapse / Renewal"
    else:
        label = f"Expansion φ^{state.index}"

    return HumanDimensionalState(label=label, index=state.index, scale=state.scale)


def name_substrate(name: str, description: str, defn: SubstrateDefinition) -> NamedSubstrate:
    """Attach human-friendly metadata to a substrate definition."""

    return NamedSubstrate(name=name, description=description, defn=defn)


def name_lens(name: str, description: str, lens: Lens[Any]) -> NamedLens:
    """Attach human-friendly metadata to a lens implementation."""

    return NamedLens(name=name, description=description, lens=lens)


__all__ = [
    "NamedSubstrate",
    "HumanDimensionalState",
    "NamedLens",
    "humanize_state",
    "name_substrate",
    "name_lens",
]
