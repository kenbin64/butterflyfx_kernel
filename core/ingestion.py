# core/ingestion.py
"""
Directional substrate ingestor with strategy selection.

Provides a small class that chooses HORIZONTAL, VERTICAL, or SPIRAL
strategies based on estimated point counts. The actual ingestion uses
spawn_substrate_vectorized and returns the Substrate.
"""

from __future__ import annotations
from typing import Sequence, Tuple, Any
from .transform import spawn_substrate_vectorized
from .substrates import SubstrateDefinition


class DirectionalSubstrateIngestor:
    """
    Ingest a substrate definition using a directional strategy.

    - strategy: "AUTO", "HORIZONTAL", "VERTICAL", or "SPIRAL"
    """
    def __init__(self, strategy: str = "AUTO"):
        self.strategy = strategy

    def ingest(self, defn: SubstrateDefinition, bounds: Sequence[Tuple[float, float]], step: float, **kwargs) -> Any:
        """
        Ingest by selecting a strategy and calling spawn_substrate_vectorized.

        kwargs are forwarded to spawn_substrate_vectorized (chunk_size, max_points).
        """
        # Strategy selection (AUTO uses simple heuristic)
        if self.strategy == "AUTO":
            est = kwargs.get("estimate_count")
            if est is None:
                # estimate_count not provided: compute rough estimate
                from .sampling import estimate_grid_count
                est = estimate_grid_count(bounds, step)
            if est > 1000:
                chosen = "HORIZONTAL"
            elif est < 100:
                chosen = "VERTICAL"
            else:
                chosen = "SPIRAL"
        else:
            chosen = self.strategy

        # For now, ingestion behavior is the same; strategy influences orchestration
        # (e.g., parallelism) in higher-level systems. Here we simply spawn.
        return spawn_substrate_vectorized(defn, bounds, step, **kwargs)

    def auto_strategy(self, n_points: int) -> str:
        """
        Heuristic mapping from point count to strategy.
        """
        if n_points > 1000:
            return "HORIZONTAL"
        if n_points < 100:
            return "VERTICAL"
        return "SPIRAL"
