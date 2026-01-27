"""Decision tree helpers for selecting substrate definitions.

Provides explicit helpers for common dimensional substrates (z=xy, z=x/y,
z=xy^2, m=xyz) and a lightweight decision function to pick implicit or
parametric forms. Also exposes a simple decision-tree-as-substrate
representation using z = x*y as the branching manifold.
"""

from __future__ import annotations

from typing import Literal

from core.substrates import Equation, SubstrateDefinition

SubstrateKind = Literal["z_xy", "z_x_over_y", "z_xy2", "m_xyz"]
FormKind = Literal["implicit", "parametric"]


def def_z_xy(form: FormKind = "parametric") -> SubstrateDefinition:
    if form == "parametric":
        return SubstrateDefinition(dim=2, equation=Equation.parametric(lambda u: [u[0], u[1], u[0] * u[1]]))
    return SubstrateDefinition(dim=3, equation=Equation.implicit(lambda p: p[2] - p[0] * p[1]))


def def_z_x_over_y(form: FormKind = "parametric") -> SubstrateDefinition:
    if form == "parametric":
        return SubstrateDefinition(dim=2, equation=Equation.parametric(lambda u: [u[0], u[1], u[0] / u[1] if u[1] != 0 else 0]))
    return SubstrateDefinition(dim=3, equation=Equation.implicit(lambda p: p[2] - (p[0] / p[1] if p[1] != 0 else 0)))


def def_z_xy2(form: FormKind = "parametric") -> SubstrateDefinition:
    if form == "parametric":
        return SubstrateDefinition(dim=2, equation=Equation.parametric(lambda u: [u[0], u[1], u[0] * (u[1] ** 2)]))
    return SubstrateDefinition(dim=3, equation=Equation.implicit(lambda p: p[2] - p[0] * (p[1] ** 2)))


def def_m_xyz(form: FormKind = "parametric") -> SubstrateDefinition:
    if form == "parametric":
        return SubstrateDefinition(dim=3, equation=Equation.parametric(lambda u: [u[0], u[1], u[2], u[0] * u[1] * u[2]]))
    return SubstrateDefinition(dim=4, equation=Equation.implicit(lambda p: p[3] - p[0] * p[1] * p[2]))


def choose_definition(kind: SubstrateKind, prefer_parametric: bool = True) -> SubstrateDefinition:
    form: FormKind = "parametric" if prefer_parametric else "implicit"
    if kind == "z_xy":
        return def_z_xy(form)
    if kind == "z_x_over_y":
        return def_z_x_over_y(form)
    if kind == "z_xy2":
        return def_z_xy2(form)
    if kind == "m_xyz":
        return def_m_xyz(form)
    raise ValueError(f"Unknown substrate kind: {kind}")


def decision_tree_substrate(score: float = 1.0, prefer_parametric: bool = True) -> SubstrateDefinition:
    """Represent a decision tree as a z = x*y manifold where x=choice, y=score."""
    form: FormKind = "parametric" if prefer_parametric else "implicit"
    if form == "parametric":
        return SubstrateDefinition(dim=2, equation=Equation.parametric(lambda u: [u[0], u[1] * score, u[0] * u[1] * score]))
    return SubstrateDefinition(dim=3, equation=Equation.implicit(lambda p: p[2] - p[0] * (p[1] / score if score != 0 else 0)))


__all__ = [
    "SubstrateKind",
    "FormKind",
    "def_z_xy",
    "def_z_x_over_y",
    "def_z_xy2",
    "def_m_xyz",
    "choose_definition",
    "decision_tree_substrate",
]
