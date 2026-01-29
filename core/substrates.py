# core/substrates.py
"""
Substrate data models.

Defines Equation (implicit/parametric), SubstrateDefinition, One, Substrate,
and DimensionalState. Parametric functions are expected to accept NumPy
arrays of shape (N, D_in) and return (N, D_out).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional, Sequence, Tuple
import numpy as np

Scalar = float
Vec = Sequence[Scalar]

# Type aliases for clarity
ImplicitFn = Callable[[Vec], Scalar]          # f([x,y,...]) -> scalar
ParametricFn = Callable[[np.ndarray], np.ndarray]  # g(array (N,D)) -> array (N,D_out)


@dataclass(frozen=True)
class Equation:
    """
    Union-like container for either an implicit or parametric equation.

    - kind: "implicit" or "parametric"
    - f: implicit function (if kind == "implicit")
    - g: parametric function (if kind == "parametric")
    """
    kind: str
    f: Optional[ImplicitFn] = None
    g: Optional[ParametricFn] = None

    @staticmethod
    def implicit(f: ImplicitFn) -> "Equation":
        return Equation(kind="implicit", f=f)

    @staticmethod
    def parametric(g: ParametricFn) -> "Equation":
        return Equation(kind="parametric", g=g)


@dataclass(frozen=True)
class SubstrateDefinition:
    """
    Pure mathematical description of a manifold.

    - dim: number of parameters (for parametric) or ambient dimension (for implicit)
    - equation: Equation instance
    """
    dim: int
    equation: Equation


@dataclass(frozen=True)
class One:
    """
    A single observed point on a manifold.

    - coord: tuple of scalar coordinates
    - attrs: optional attribute dictionary
    """
    coord: Tuple[Scalar, ...]
    attrs: Optional[dict] = None


@dataclass(frozen=True)
class Substrate:
    """
    A realized substrate: definition + observed ones.

    - defn: SubstrateDefinition
    - ones: tuple of One objects
    """
    defn: SubstrateDefinition
    ones: Tuple[One, ...]


@dataclass(frozen=True)
class DimensionalState:
    """
    Represents a φ-recursion state for scaling and spawning.

    - index: ordinal index in the cycle
    - fib_value: Fibonacci-like value assigned to this level (domain semantic)
    - scale: numeric scale factor used when spawning
    - label: optional human label
    """
    index: int
    fib_value: int
    scale: float
    label: str = ""
