# core/transform.py
"""
Canonical substrate: z = x * y^2 and vectorized spawn logic.

- z_xy2_parametric() returns a SubstrateDefinition with a parametric g.
- spawn_substrate_vectorized() evaluates g over a grid in chunks and returns
  a Substrate (materializing One objects only at the end).
"""

from __future__ import annotations
from typing import Sequence, Tuple, Optional
import numpy as np
from .substrates import SubstrateDefinition, Equation, Substrate, One
from .sampling import grid_params_generator, chunked

def z_xy2_parametric() -> SubstrateDefinition:
    """
    Parametric definition for z = x * y^2.

    The returned g accepts a NumPy array of shape (N,2) and returns (N,3).
    """
    def g(u: np.ndarray) -> np.ndarray:
        # u[:,0] = x, u[:,1] = y
        x = u[:, 0]
        y = u[:, 1]
        z = x * (y ** 2)
        return np.stack([x, y, z], axis=-1)
    return SubstrateDefinition(dim=2, equation=Equation.parametric(g))


def spawn_substrate_vectorized(defn: SubstrateDefinition,
                               bounds: Sequence[Tuple[float, float]],
                               step: float,
                               chunk_size: int = 100_000,
                               max_points: Optional[int] = 5_000_000) -> Substrate:
    """
    Evaluate a parametric or implicit substrate over a grid.

    - defn: SubstrateDefinition (parametric preferred)
    - bounds: sequence of (min, max) pairs, one per parameter
    - step: sampling increment
    - chunk_size: number of parameter vectors evaluated per batch
    - max_points: safety guard to avoid runaway memory usage

    Returns a Substrate with One objects for each sampled coordinate.
    """
    coords_parts = []
    total = 0
    gen = grid_params_generator(bounds, step)

    # Evaluate in batches to limit memory
    for batch in chunked(gen, chunk_size):
        arr = np.asarray(batch, dtype=float)  # shape (M, dim)
        if defn.equation.kind == "parametric":
            # Vectorized parametric mapping
            g = defn.equation.g
            mapped = g(arr)  # expected shape (M, D_out)
            coords_parts.append(mapped)
            total += mapped.shape[0]
            if max_points and total > max_points:
                raise MemoryError("Exceeded max_points budget in spawn_substrate_vectorized")
        else:
            # Implicit: evaluate f per parameter vector and select zeros
            f = defn.equation.f
            vals = np.array([f(row.tolist()) for row in arr])
            mask = np.abs(vals) < 1e-9
            coords_parts.append(arr[mask])
            total += int(mask.sum())
            if max_points and total > max_points:
                raise MemoryError("Exceeded max_points budget in spawn_substrate_vectorized")

    # Concatenate results and materialize One objects
    if coords_parts:
        coords = np.vstack(coords_parts)
    else:
        coords = np.empty((0, defn.dim + 1))

    # Convert rows to One objects (tuple coords)
    ones = tuple(One(coord=tuple(row)) for row in coords)
    return Substrate(defn=defn, ones=ones)
