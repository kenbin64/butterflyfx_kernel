"""Affine transform helpers for substrate definitions."""

from __future__ import annotations

from typing import Iterable, Sequence

from core.substrates import Equation, Scalar, SubstrateDefinition


def _normalize_factors(factors: Scalar | Sequence[Scalar], dim: int) -> list[Scalar]:
    if isinstance(factors, (int, float)):
        return [float(factors)] * dim
    if len(factors) < dim:
        raise ValueError("Not enough scale factors for dimensions")
    return [float(x) for x in factors[:dim]]


def translate_definition(defn: SubstrateDefinition, offsets: Sequence[Scalar]) -> SubstrateDefinition:
    offs = list(offsets)
    if len(offs) < defn.dim:
        raise ValueError("Offset length must match dimension")

    if defn.equation.kind == "parametric":
        if defn.equation.g is None:
            raise ValueError("Parametric equation missing g")
        return SubstrateDefinition(
            dim=defn.dim,
            equation=Equation.parametric(lambda u, g=defn.equation.g: [g(u)[i] + offs[i] for i in range(defn.dim)]),
        )

    if defn.equation.f is None:
        raise ValueError("Implicit equation missing f")
    return SubstrateDefinition(
        dim=defn.dim,
        equation=Equation.implicit(lambda p, f=defn.equation.f: f([p[i] - offs[i] for i in range(defn.dim)])),
    )


def scale_definition(defn: SubstrateDefinition, factors: Scalar | Sequence[Scalar]) -> SubstrateDefinition:
    facs = _normalize_factors(factors, defn.dim)

    if defn.equation.kind == "parametric":
        if defn.equation.g is None:
            raise ValueError("Parametric equation missing g")
        return SubstrateDefinition(
            dim=defn.dim,
            equation=Equation.parametric(lambda u, g=defn.equation.g: [g(u)[i] * facs[i] for i in range(defn.dim)]),
        )

    if defn.equation.f is None:
        raise ValueError("Implicit equation missing f")
    return SubstrateDefinition(
        dim=defn.dim,
        equation=Equation.implicit(lambda p, f=defn.equation.f: f([p[i] / facs[i] if facs[i] != 0 else 0 for i in range(defn.dim)])),
    )


__all__ = ["translate_definition", "scale_definition"]