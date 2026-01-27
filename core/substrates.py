"""Substrate-of-substrates: a pure generative kernel.

This module defines minimal primitives for describing manifolds, collapsing them
into observable substrates, and treating every generated "one" as a
first-class dimensional unit. No hard-coded shapes; only equations and
observation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

Scalar = float
Vec = List[Scalar]


# ---------------------------------------------------------------------------
# Equation definitions
# ---------------------------------------------------------------------------

ImplicitFn = Callable[[Vec], Scalar]
ParametricFn = Callable[[Vec], Vec]


@dataclass(frozen=True)
class Equation:
    """Union-like structure describing either an implicit or parametric form."""

    kind: str
    f: Optional[ImplicitFn] = None
    g: Optional[ParametricFn] = None

    @staticmethod
    def implicit(f: ImplicitFn) -> "Equation":
        return Equation(kind="implicit", f=f)

    @staticmethod
    def parametric(g: ParametricFn) -> "Equation":
        return Equation(kind="parametric", g=g)


# ---------------------------------------------------------------------------
# Core primitives
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SubstrateDefinition:
    """Pure math describing a manifold. Not the manifold itself."""

    dim: int
    equation: Equation


@dataclass(frozen=True)
class One:
    """A single observed point on a manifold."""

    coord: Tuple[Scalar, ...]
    attrs: Optional[Dict[str, Scalar | str]] = None


@dataclass(frozen=True)
class Substrate:
    """A realized manifold: definition + observed ones."""

    defn: SubstrateDefinition
    ones: Tuple[One, ...]

    # Alias aligning with the TypeScript spec nomenclature
    @property
    def def_(self) -> SubstrateDefinition:  # pragma: no cover - trivial alias
        return self.defn


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def approx_eq(a: Scalar, b: Scalar, eps: Scalar = 1e-6) -> bool:
    """Approximate equality helper."""

    return abs(a - b) < eps


def _is_one(defn: SubstrateDefinition, p: Vec) -> bool:
    if defn.equation.kind == "implicit":
        if defn.equation.f is None:
            raise ValueError("Implicit equation missing function 'f'.")
        return approx_eq(defn.equation.f(p), 0)
    if defn.equation.kind == "parametric":
        return True  # parametric images are accepted as-is
    raise ValueError(f"Unknown equation kind: {defn.equation.kind}")


# ---------------------------------------------------------------------------
# Substrate generator
# ---------------------------------------------------------------------------


def spawn_substrate(
    defn: SubstrateDefinition, bounds: Sequence[Tuple[Scalar, Scalar]], step: Scalar
) -> Substrate:
    """Collapse a definition into a concrete substrate by sampling.

    Args:
        defn: Manifold definition (implicit or parametric).
        bounds: Sequence of [min, max] pairs, one per dimension/parameter.
        step: Sampling increment for each dimension.
    """

    if defn.dim != len(bounds):
        raise ValueError(
            f"Dimension mismatch: defn.dim={defn.dim} but bounds has {len(bounds)} elements."
        )

    ones: List[One] = []

    def recurse(params: List[Scalar], dim_index: int) -> None:
        if dim_index == defn.dim:
            if defn.equation.kind == "implicit":
                coord = tuple(params)
                if _is_one(defn, list(coord)):
                    ones.append(One(coord=coord))
            else:
                if defn.equation.g is None:
                    raise ValueError("Parametric equation missing function 'g'.")
                coord_vec = defn.equation.g(list(params))
                ones.append(One(coord=tuple(coord_vec)))
            return

        min_val, max_val = bounds[dim_index]
        v = min_val
        while v <= max_val + 1e-12:  # guard against float step drift
            recurse([*params, v], dim_index + 1)
            v += step

    recurse([], 0)

    return Substrate(defn=defn, ones=tuple(ones))


# ---------------------------------------------------------------------------
# Dimensional recursion engine
# ---------------------------------------------------------------------------


PHI: Scalar = (1 + sqrt(5)) / 2


@dataclass(frozen=True)
class DimensionalState:
    """Represents a φ-recursion state for scaling and spawning."""

    index: int  # 1..33 plus collapse stage
    scale: Scalar
    substrate: SubstrateDefinition


def phi_scale(n: int) -> Scalar:
    return PHI**n


def generate_cycle(base_substrate: SubstrateDefinition) -> Tuple[DimensionalState, ...]:
    states: List[DimensionalState] = []
    for i in range(1, 34):
        states.append(DimensionalState(index=i, scale=phi_scale(i), substrate=base_substrate))
    # collapse back to 1
    states.append(DimensionalState(index=34, scale=1, substrate=base_substrate))
    return tuple(states)


def spawn_at_state(
    state: DimensionalState, bounds: Sequence[Tuple[Scalar, Scalar]], step: Scalar
) -> Substrate:
    scaled_bounds = [(mn * state.scale, mx * state.scale) for mn, mx in bounds]
    return spawn_substrate(state.substrate, scaled_bounds, step)


__all__ = [
    "Scalar",
    "Vec",
    "Equation",
    "SubstrateDefinition",
    "One",
    "Substrate",
    "spawn_substrate",
    "approx_eq",
    "PHI",
    "DimensionalState",
    "phi_scale",
    "generate_cycle",
    "spawn_at_state",
]