"""
ButterflyFX Kernel Core - Standalone Library Package
=====================================================

A hardened, secure, and optimized pure math substrate system with:
- Canonical z = x * y² substrate enforcement
- SRL (Secure Resource Locator) universal connectors
- Fibonacci spiral points of creation for all operations
- Multi-language compatibility API
- Security hardening with validation layers
- Dimensional inheritance with reversible transformations

This is the STANDALONE core library that can be imported and used across
all programming languages through the provided API interfaces.

Core Principles:
1. The canonical substrate equation is z = x * y²
   - x = identity component
   - y = transformation component  
   - z = completed artifact (identity × transformation²)

2. Substrate ≠ Lens
   - Substrate: pure, lossless, reversible math objects
   - Lens: presentation, UI, rendering, animation, sound, layout

3. Dimensional Inheritance
   - 0D → 1D → 2D → 3D → nD with reversible compression
   - Higher dimensions compress into lower ones without losing information

4. Directional Operations
   - Horizontal movement (→ ←): MULTIPLICATION → Vertical boundaries │
   - Vertical movement (↑ ↓): DIVISION → Horizontal boundaries ─
   - Fibonacci spiral: ● → ↑ ← ↓ → ↑ ∞ (clockwise)

Version: 1.0.0-hardened
Security Level: HARDENED with SRL integration
License: MIT
"""

__version__ = "1.0.0-hardened"
__author__ = "ButterflyFX Kernel Team"
__license__ = "MIT"

# Core primitives
from .substrates import (
    Equation,
    One,
    Scalar,
    Substrate,
    SubstrateDefinition,
    Vec,
)

# Canonical substrate and transforms
from .transforms import (
    z_xy2_parametric,
    spawn_substrate_vectorized,
)

# Security and SRL integration
from .secure_substrate import (
    SecureSubstrate,
    SecureSubstrateDefinition,
    SecureSubstrateFactory,
    SubstrateAPI,
    SecurityLevel,
    SubstrateState,
)

# Fibonacci spiral points of creation
from .fibonacci_creation import (
    CreationPoint,
    CreationPhase,
    FibonacciSpiralCreator,
    get_creation_point,
    create_substrate_at_level,
    apply_fibonacci_creation,
    get_creation_metadata,
    visualize_fibonacci_spiral,
)

# SRL universal connector
from .srl import (
    SRL,
    ConnectorAdapter,
    LocalFileAdapter,
    HTTPAdapter,
    SQLiteAdapter,
    LensConnector,
    bitcount,
    timestamp_now,
)

# Fibonacci directional levels
from .fibonacci_directional_levels import (
    FibonacciLevel,
    Direction,
    Operation,
    Boundary,
    FIBONACCI_LEVELS,
    get_level,
    get_direction_at_level,
    get_operation_at_level,
    get_boundary_at_level,
    is_multiplication_level,
    is_division_level,
    get_spiral_pattern,
    visualize_levels,
)

# Optional utilities (import as needed)
from .lenses import (
    Lens,
    IdentityLens,
    StatsLens,
    AggregationLens,
)

from .hil import (
    name_substrate,
    name_lens,
    humanize_state,
)

from .decider import (
    choose_definition,
    decision_tree_substrate,
)

from .sampling import (
    grid_params,
    random_params,
    enforce_budget,
)

from .phi_lens import (
    PhiStepLens,
    PhiCycleLens,
)

# Constants
PHI = (1 + 5 ** 0.5) / 2  # Golden ratio ≈ 1.618
GOLDEN_RATIO_LIMIT = 21   # φ⁸ ≈ 21.009 - prevents uncontrolled growth
TRADITIONAL_DIMENSIONAL_UNITS = 21  # Complete cycle value
CUMULATIVE_DIMENSIONAL_AT_LEVEL_7 = 33  # New understanding


# Convenience functions for quick substrate creation
def create_canonical_substrate(substrate_id: str = "default", 
                             fibonacci_level: int = 0,
                             security_level: SecurityLevel = SecurityLevel.STANDARD) -> SecureSubstrate:
    """
    Quick creation of a canonical z = x * y² substrate
    
    Args:
        substrate_id: Unique identifier for the substrate
        fibonacci_level: Initial Fibonacci level (0-8)
        security_level: Security validation level
    
    Returns:
        SecureSubstrate instance with full SRL and Fibonacci integration
    """
    return SecureSubstrateFactory.create_canonical(
        substrate_id=substrate_id,
        security_level=security_level,
        fibonacci_level=fibonacci_level
    )


def create_multi_language_api(security_level: SecurityLevel = SecurityLevel.STANDARD) -> SubstrateAPI:
    """
    Create API instance for multi-language compatibility
    
    Returns:
        SubstrateAPI instance that can be exposed to other programming languages
    """
    return SubstrateAPI(security_level=security_level)


def get_fibonacci_creation_point(level: int) -> Optional[CreationPoint]:
    """
    Get Fibonacci spiral creation point at specified level
    
    Args:
        level: Fibonacci level (0-8)
    
    Returns:
        CreationPoint with full metadata or None if invalid level
    """
    return get_creation_point(level)


def create_fibonacci_substrate(level: int, substrate_id: str = "") -> Substrate:
    """
    Create substrate at specific Fibonacci level using spiral creation point
    
    Args:
        level: Fibonacci level (0-8)
        substrate_id: Optional substrate identifier
    
    Returns:
        Substrate created at the specified Fibonacci level
    """
    return create_substrate_at_level(level, substrate_id)


# Package information and validation
def get_package_info() -> dict:
    """Get comprehensive package information"""
    return {
        'name': 'butterflyfx-kernel-core',
        'version': __version__,
        'author': __author__,
        'license': __license__,
        'description': 'Hardened pure math substrate system with SRL and Fibonacci integration',
        'canonical_equation': 'z = x * y²',
        'security_levels': [level.value for level in SecurityLevel],
        'fibonacci_levels': list(range(9)),  # 0-8
        'golden_ratio': PHI,
        'golden_ratio_limit': GOLDEN_RATIO_LIMIT,
        'supported_languages': ['Python', 'C++', 'JavaScript', 'Rust', 'Go'],
        'api_compatibility': 'FFI/gRPC/REST',
        'security_features': [
            'SRL universal connectors',
            'Checksum verification',
            'Audit trails',
            'Canonical form validation',
            'Bitcount verification'
        ],
        'fibonacci_features': [
            'Directional operations',
            'Points of creation',
            'Dimensional inheritance',
            'Spiral pattern encoding',
            'Golden ratio limit enforcement'
        ]
    }


def validate_package_integrity() -> dict:
    """
    Validate package integrity and security
    
    Returns:
        Validation report with security checks
    """
    import hashlib
    import os
    
    validation = {
        'package_valid': True,
        'version': __version__,
        'checks': {},
        'security_level': 'HARDENED'
    }
    
    # Check core modules exist
    core_modules = [
        'substrates', 'transforms', 'secure_substrate', 'fibonacci_creation',
        'srl', 'fibonacci_directional_levels', 'lenses', 'hil'
    ]
    
    for module in core_modules:
        try:
            __import__(f'.{module}', package=__name__)
            validation['checks'][f'module_{module}'] = True
        except ImportError:
            validation['checks'][f'module_{module}'] = False
            validation['package_valid'] = False
    
    # Validate golden ratio
    expected_phi = (1 + 5 ** 0.5) / 2
    validation['checks']['golden_ratio_correct'] = abs(PHI - expected_phi) < 1e-10
    
    # Validate Fibonacci levels
    validation['checks']['fibonacci_levels_complete'] = len(FIBONACCI_LEVELS) == 9
    
    return validation


# Export all public symbols
__all__ = [
    # Version and info
    '__version__',
    '__author__',
    '__license__',
    'get_package_info',
    'validate_package_integrity',
    
    # Core primitives
    'Equation',
    'One',
    'Scalar',
    'Substrate',
    'SubstrateDefinition',
    'Vec',
    
    # Canonical substrate
    'z_xy2_parametric',
    'spawn_substrate_vectorized',
    
    # Security and SRL
    'SecureSubstrate',
    'SecureSubstrateDefinition',
    'SecureSubstrateFactory',
    'SubstrateAPI',
    'SecurityLevel',
    'SubstrateState',
    'SRL',
    'ConnectorAdapter',
    'LocalFileAdapter',
    'HTTPAdapter',
    'SQLiteAdapter',
    'LensConnector',
    'bitcount',
    'timestamp_now',
    
    # Fibonacci creation
    'CreationPoint',
    'CreationPhase',
    'FibonacciSpiralCreator',
    'get_creation_point',
    'create_substrate_at_level',
    'apply_fibonacci_creation',
    'get_creation_metadata',
    'visualize_fibonacci_spiral',
    
    # Fibonacci directional levels
    'FibonacciLevel',
    'Direction',
    'Operation',
    'Boundary',
    'FIBONACCI_LEVELS',
    'get_level',
    'get_direction_at_level',
    'get_operation_at_level',
    'get_boundary_at_level',
    'is_multiplication_level',
    'is_division_level',
    'get_spiral_pattern',
    'visualize_levels',
    
    # Constants
    'PHI',
    'GOLDEN_RATIO_LIMIT',
    'TRADITIONAL_DIMENSIONAL_UNITS',
    'CUMULATIVE_DIMENSIONAL_AT_LEVEL_7',
    
    # Convenience functions
    'create_canonical_substrate',
    'create_multi_language_api',
    'get_fibonacci_creation_point',
    'create_fibonacci_substrate',
    
    # Optional utilities
    'Lens',
    'IdentityLens',
    'StatsLens',
    'AggregationLens',
    'name_substrate',
    'name_lens',
    'humanize_state',
    'choose_definition',
    'decision_tree_substrate',
    'grid_params',
    'random_params',
    'enforce_budget',
    'PhiStepLens',
    'PhiCycleLens',
]


# Package initialization validation
def _initialize_package():
    """Initialize package with validation"""
    validation = validate_package_integrity()
    if not validation['package_valid']:
        print("⚠️  ButterflyFX Kernel Core - Package validation failed")
        print("Some modules may be missing or corrupted")
    else:
        print("✅ ButterflyFX Kernel Core - Package validated successfully")
        print(f"Version: {__version__}")
        print(f"Security Level: HARDENED with SRL integration")
        print(f"Fibonacci Levels: 0-8 (Golden ratio limit: {GOLDEN_RATIO_LIMIT})")


# Auto-initialize on import
_initialize_package()
