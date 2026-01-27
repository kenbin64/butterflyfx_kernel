"""Fibonacci utilities expressed in substrate-friendly terms."""

from __future__ import annotations

from typing import Sequence, Tuple


def fibonacci_sequence(n: int):
    """Generate the first *n* Fibonacci numbers."""

    if n <= 0:
        return []
    if n == 1:
        return [0]

    sequence = [0, 1]
    for _ in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


def _extract_xy(source, y=None) -> Tuple[float, float]:
    """Extract an (x, y) pair from numbers, sequences, or substrates."""

    # Numeric pair
    if isinstance(source, (int, float)):
        if y is None:
            raise TypeError("y must be provided when source is a scalar")
        return float(source), float(y)

    # Sequence-like
    if isinstance(source, Sequence) and not isinstance(source, (str, bytes)):
        if len(source) < 2:
            raise ValueError("Sequence must contain at least two elements")
        return float(source[0]), float(source[1])

    # Substrate (imported lazily to avoid cycles)
    try:
        from core.substrates import Substrate

        if isinstance(source, Substrate):
            if not source.ones:
                raise ValueError("Substrate must contain at least one observed point")
            coord = source.ones[0].coord
            if len(coord) < 2:
                raise ValueError("Observed coordinate must be at least 2D for directional attributes")
            return float(coord[0]), float(coord[1])
    except Exception:
        pass

    raise TypeError("Unsupported source type for extracting directional attributes")


def fibonacci_directional_operations(x, y):
    """Perform multiplicative/divisive directional operations."""

    return {
        "horizontal_movement": x * y,
        "vertical_movement": x / y if y != 0 else 0,
    }


def fibonacci_directional_attributes(source, y=None):
    """Convenience wrapper that accepts scalars, sequences, or substrates."""

    x_val, y_val = _extract_xy(source, y)
    return fibonacci_directional_operations(x_val, y_val)


__all__ = [
    "fibonacci_sequence",
    "fibonacci_directional_attributes",
    "fibonacci_directional_operations",
]