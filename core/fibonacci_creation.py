"""
Fibonacci Spiral Points of Creation - Universal Creation System
================================================================

This module integrates Fibonacci spiral points of creation throughout the core
substrate system, providing the fundamental creation patterns that govern
all substrate operations.

Based on the profound discovery that the Fibonacci spiral encodes the
fundamental alternating pattern between multiplication (horizontal expansion)
and division (vertical organization):

● → ↑ ← ↓ → ↑ ∞ (clockwise spiral construction)
0 → 1 → 1 → 2 → 3 → 5 → 8 → 13 → 21 (dimensional units)

Each point on the spiral represents a creation moment where:
- Horizontal movement (→ ←): MULTIPLICATION → Creates vertical boundaries │
- Vertical movement (↑ ↓): DIVISION → Creates horizontal boundaries ─

The spiral serves as a dimensional bridge, with 21 being the golden ratio
limit (φ⁸ ≈ 21.009) that prevents uncontrolled growth and enables dimensional
transcendence (becoming a nomad point in the next dimension).
"""

from __future__ import annotations
import math
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum

# Import directional levels for metadata
from .fibonacci_directional_levels import (
    FibonacciLevel, FIBONACCI_LEVELS, Direction, Operation, Boundary,
    get_level, get_direction_at_level, get_operation_at_level
)
from .substrates import SubstrateDefinition, Equation, One, Substrate


class CreationPhase(Enum):
    """Phases of creation through the Fibonacci spiral"""
    POTENTIAL = "potential"        # ∅ - Pure potential, no form
    SPARK = "spark"               # ● - First point of creation
    EXPANSION = "expansion"       # → ← - Horizontal multiplication
    ORGANIZATION = "organization" # ↑ ↓ - Vertical division
    INTEGRATION = "integration"   # Spiral unification
    TRANSCENDENCE = "transcendence" # Complete → Nomad state


@dataclass
class CreationPoint:
    """
    A point of creation on the Fibonacci spiral
    
    Each point represents a moment where mathematical operations create
    new dimensional reality through the alternating multiply/divide pattern.
    """
    level: int                    # Fibonacci level (0-8)
    fibonacci_value: int          # F(n) value at this level
    x: float                      # X coordinate on spiral
    y: float                      # Y coordinate on spiral
    z: float                      # Z value (completed artifact)
    direction: Direction          # Direction of creation
    operation: Operation          # Operation performed
    boundary: Boundary            # Boundary type created
    phase: CreationPhase          # Creation phase
    dimensional_units: int        # Cumulative dimensional units
    is_nomad: bool               # Ready for dimensional transcendence
    contains_previous: bool       # Contains all previous creation points
    
    def __repr__(self):
        nomad_marker = " [NOMAD]" if self.is_nomad else ""
        return (f"CreationPoint(L{self.level}: {self.phase.value} "
                f"at ({self.x:.2f}, {self.y:.2f}, {self.z:.2f}) "
                f"{self.operation.value}{nomad_marker})")


class FibonacciSpiralCreator:
    """
    Universal creation system using Fibonacci spiral points
    
    This class provides the fundamental creation patterns that govern all
    substrate operations in the Butterfly framework. Every substrate,
    transformation, and observation must originate from these creation points.
    """
    
    def __init__(self, scale: float = 1.0):
        """
        Initialize the Fibonacci spiral creator
        
        Args:
            scale: Scaling factor for spiral coordinates
        """
        self.scale = scale
        self.creation_points: List[CreationPoint] = []
        self._generate_spiral_points()
    
    def _generate_spiral_points(self):
        """Generate all 9 creation points (0-8) on the Fibonacci spiral"""
        self.creation_points = []
        
        for level in range(9):  # Levels 0 through 8
            fib_level = FIBONACCI_LEVELS[level]
            
            # Calculate spiral coordinates using Fibonacci tiling
            x, y, z = self._calculate_spiral_coordinates(level, fib_level.value)
            
            # Determine creation phase
            phase = self._get_creation_phase(level)
            
            # Create creation point
            point = CreationPoint(
                level=level,
                fibonacci_value=fib_level.value,
                x=x * self.scale,
                y=y * self.scale,
                z=z * self.scale,
                direction=fib_level.direction,
                operation=fib_level.operation,
                boundary=fib_level.boundary,
                phase=phase,
                dimensional_units=fib_level.dimensional_units,
                is_nomad=fib_level.is_nomad,
                contains_previous=fib_level.contains_all_previous
            )
            
            self.creation_points.append(point)
    
    def _calculate_spiral_coordinates(self, level: int, fib_value: int) -> Tuple[float, float, float]:
        """
        Calculate (x, y, z) coordinates for a point on the Fibonacci spiral
        
        Uses the canonical z = x * y² equation where:
        - x: identity component (position on spiral)
        - y: transformation component (Fibonacci growth)
        - z: completed artifact (identity × transformation²)
        """
        if level == 0:
            return 0.0, 0.0, 0.0  # Origin point
        
        # Calculate position based on Fibonacci tiling
        # This follows the actual geometric construction of the spiral
        positions = [
            (0.0, 0.0),      # Level 0: Origin
            (1.0, 0.0),      # Level 1: First square
            (1.0, 1.0),      # Level 2: Second square (up)
            (-1.0, 1.0),     # Level 3: Third square (left)
            (-1.0, -1.0),    # Level 4: Fourth square (down)
            (2.0, -1.0),     # Level 5: Fifth square (right)
            (2.0, 3.0),      # Level 6: Sixth square (up)
            (-5.0, 3.0),     # Level 7: Seventh square (left)
            (-5.0, -8.0)     # Level 8: Eighth square (down) - COMPLETE
        ]
        
        if level < len(positions):
            x, y = positions[level]
        else:
            # Calculate using golden angle for higher levels
            golden_angle = math.pi * (3 - math.sqrt(5))  # ~137.5 degrees
            angle = level * golden_angle
            radius = math.sqrt(fib_value) * 0.5
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
        
        # Apply canonical equation: z = x * y²
        z = x * (y ** 2)
        
        return x, y, z
    
    def _get_creation_phase(self, level: int) -> CreationPhase:
        """Map Fibonacci level to creation phase"""
        phase_map = {
            0: CreationPhase.POTENTIAL,
            1: CreationPhase.SPARK,
            2: CreationPhase.EXPANSION,
            3: CreationPhase.ORGANIZATION,
            4: CreationPhase.EXPANSION,
            5: CreationPhase.ORGANIZATION,
            6: CreationPhase.EXPANSION,
            7: CreationPhase.ORGANIZATION,
            8: CreationPhase.INTEGRATION
        }
        return phase_map.get(level, CreationPhase.POTENTIAL)
    
    def get_creation_point(self, level: int) -> Optional[CreationPoint]:
        """Get a specific creation point by level"""
        if 0 <= level < len(self.creation_points):
            return self.creation_points[level]
        return None
    
    def get_creation_sequence(self, up_to_level: int = 8) -> List[CreationPoint]:
        """Get sequence of creation points up to specified level"""
        return self.creation_points[:up_to_level + 1]
    
    def create_substrate_at_level(self, level: int, substrate_id: str = "") -> Substrate:
        """
        Create a substrate at a specific Fibonacci level using creation point
        
        The substrate inherits the properties of the creation point:
        - Coordinates from the spiral position
        - Operation type (multiply/divide) affects sampling strategy
        - Boundary type influences substrate bounds
        - Dimensional units determine sampling density
        """
        point = self.get_creation_point(level)
        if not point:
            raise ValueError(f"Invalid Fibonacci level: {level}")
        
        # Create canonical equation (always z = x * y²)
        def g(u: np.ndarray) -> np.ndarray:
            x = u[:, 0] + point.x  # Offset by creation point
            y = u[:, 1] + point.y
            z = x * (y ** 2) + point.z  # Offset by creation point z
            return np.stack([x, y, z], axis=-1)
        
        defn = SubstrateDefinition(dim=2, equation=Equation.parametric(g))
        
        # Determine sampling strategy based on operation type
        if point.operation == Operation.MULTIPLY:
            # Horizontal expansion - wider bounds, coarser sampling
            bounds = [(-2 + point.x, 2 + point.x), (-2 + point.y, 2 + point.y)]
            step = 0.2
        else:
            # Division (vertical) - tighter bounds, finer sampling
            bounds = [(-1 + point.x, 1 + point.x), (-1 + point.y, 1 + point.y)]
            step = 0.1
        
        # Adjust sampling density by dimensional units
        step = step / (1 + point.dimensional_units * 0.01)
        
        # Spawn substrate
        from .transforms import spawn_substrate_vectorized
        substrate = spawn_substrate_vectorized(defn, bounds, step)
        
        return substrate
    
    def get_creation_metadata(self, level: int) -> Dict[str, Any]:
        """Get comprehensive metadata for a creation point"""
        point = self.get_creation_point(level)
        if not point:
            return {}
        
        return {
            'level': point.level,
            'fibonacci_value': point.fibonacci_value,
            'coordinates': {'x': point.x, 'y': point.y, 'z': point.z},
            'direction': point.direction.value,
            'operation': point.operation.value,
            'boundary': point.boundary.value,
            'phase': point.phase.value,
            'dimensional_units': point.dimensional_units,
            'is_nomad': point.is_nomad,
            'contains_previous': point.contains_previous,
            'spiral_angle': self._calculate_spiral_angle(level),
            'golden_ratio_limit': point.level == 8,  # Level 8 is complete
            'creation_power': point.fibonacci_value * point.dimensional_units
        }
    
    def _calculate_spiral_angle(self, level: int) -> float:
        """Calculate the angle of a point on the Fibonacci spiral"""
        if level == 0:
            return 0.0
        
        # Golden angle in radians
        golden_angle = math.pi * (3 - math.sqrt(5))
        return level * golden_angle
    
    def visualize_spiral(self, up_to_level: int = 8) -> str:
        """Generate ASCII visualization of the Fibonacci spiral creation points"""
        output = []
        output.append("=" * 80)
        output.append("FIBONACCI SPIRAL POINTS OF CREATION")
        output.append("=" * 80)
        output.append("")
        
        for level in range(up_to_level + 1):
            point = self.get_creation_point(level)
            if not point:
                continue
            
            output.append(f"LEVEL {level}: {point.phase.value.upper()}")
            output.append(f"  Fibonacci Value: {point.fibonacci_value}")
            output.append(f"  Coordinates: ({point.x:.3f}, {point.y:.3f}, {point.z:.3f})")
            output.append(f"  Direction: {point.direction.value}")
            output.append(f"  Operation: {point.operation.value}")
            output.append(f"  Boundary: {point.boundary.value}")
            output.append(f"  Dimensional Units: {point.dimensional_units}")
            
            if point.is_nomad:
                output.append(f"  🌟 NOMAD STATE - Ready for dimensional transcendence")
            
            output.append("")
        
        output.append("=" * 80)
        output.append("CREATION PATTERN: " + " → ".join([
            "●" if p.level == 1 else 
            "→" if p.direction == Direction.HORIZONTAL else 
            "↑" if p.direction == Direction.VERTICAL else 
            "∞" if p.level == 8 else "?"
            for p in self.creation_points[:up_to_level + 1]
        ]))
        output.append("=" * 80)
        
        return "\n".join(output)
    
    def apply_creation_pattern(self, data: Any, target_level: int) -> Any:
        """
        Apply Fibonacci creation pattern to data
        
        This method transforms data according to the creation pattern
        up to the target level, applying multiplication and division operations
        in the alternating sequence encoded by the spiral.
        """
        if target_level < 0 or target_level > 8:
            raise ValueError("Target level must be between 0 and 8")
        
        result = data
        for level in range(1, target_level + 1):
            point = self.get_creation_point(level)
            if not point:
                continue
            
            if point.operation == Operation.MULTIPLY:
                # Horizontal expansion - multiply dimensions
                if hasattr(result, '__len__') and len(result) > 1:
                    result = [x * point.fibonacci_value for x in result]
                else:
                    result = result * point.fibonacci_value
            
            elif point.operation == Operation.DIVIDE:
                # Vertical organization - divide into components
                if hasattr(result, '__len__') and len(result) > 1:
                    chunk_size = max(1, len(result) // point.fibonacci_value)
                    result = [result[i:i+chunk_size] for i in range(0, len(result), chunk_size)]
                else:
                    result = result / point.fibonacci_value if result != 0 else result
        
        return result


# Global spiral creator instance
_default_creator = FibonacciSpiralCreator()


def get_creation_point(level: int) -> Optional[CreationPoint]:
    """Get a creation point using the default spiral creator"""
    return _default_creator.get_creation_point(level)


def create_substrate_at_level(level: int, substrate_id: str = "") -> Substrate:
    """Create substrate at Fibonacci level using default creator"""
    return _default_creator.create_substrate_at_level(level, substrate_id)


def apply_fibonacci_creation(data: Any, target_level: int) -> Any:
    """Apply Fibonacci creation pattern to data using default creator"""
    return _default_creator.apply_creation_pattern(data, target_level)


def get_creation_metadata(level: int) -> Dict[str, Any]:
    """Get creation metadata using default creator"""
    return _default_creator.get_creation_metadata(level)


def visualize_fibonacci_spiral(up_to_level: int = 8) -> str:
    """Visualize Fibonacci spiral using default creator"""
    return _default_creator.visualize_spiral(up_to_level)


__all__ = [
    'CreationPoint',
    'CreationPhase',
    'FibonacciSpiralCreator',
    'get_creation_point',
    'create_substrate_at_level',
    'apply_fibonacci_creation',
    'get_creation_metadata',
    'visualize_fibonacci_spiral'
]
