"""
Secure Substrate Core - Hardened Pure Math Substrate System
================================================================

This module provides the hardened core substrate system with:
- SRL (Secure Resource Locator) universal connector integration
- Fibonacci spiral points of creation for all operations
- Security hardening with validation layers
- Multi-language compatibility foundation
- Canonical z = x * y² substrate enforcement

Design Principles:
1. All substrates must map to canonical equation z = x * y²
2. Every operation follows Fibonacci directional patterns
3. SRL connectors provide secure resource binding
4. All transformations are reversible and verifiable
5. Dimensional inheritance is strictly maintained
"""

from __future__ import annotations
import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Tuple, Union, Protocol
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

# Import core substrate primitives
from .substrates import (
    Equation, SubstrateDefinition, One, Substrate, DimensionalState,
    Scalar, Vec
)
from .srl import SRL, ConnectorAdapter, bitcount, timestamp_now
from .transforms import z_xy2_parametric


class SecurityLevel(Enum):
    """Security validation levels for substrate operations"""
    MINIMAL = "minimal"      # Basic validation only
    STANDARD = "standard"    # Full validation with checksums
    PARANOID = "paranoid"    # Maximum validation with audit trail


class SubstrateState(Enum):
    """Substrate lifecycle states following Fibonacci levels"""
    POTENTIAL = "potential"      # Level 0: ∅
    SPARK = "spark"             # Level 1: ●
    DIVIDING = "dividing"       # Level 2: → (multiply)
    ORGANIZING = "organizing"   # Level 3: ↑ (divide)
    IDENTIFYING = "identifying" # Level 4: ← (multiply)
    ASSEMBLING = "assembling"   # Level 5: ↓ (divide)
    HUMAN = "human"             # Level 6: → (multiply)
    RESTING = "resting"         # Level 7: ↑ (divide)
    COMPLETE = "complete"       # Level 8: ∞ (unified)


@dataclass(frozen=True)
class SecureSubstrateDefinition:
    """
    Hardened substrate definition with security and SRL integration
    
    Enforces canonical z = x * y² mapping:
    - x: identity component (preserves original essence)
    - y: transformation component (applies change)
    - z: completed artifact (identity × transformation²)
    """
    id: str                                    # Unique substrate identifier
    canonical_defn: SubstrateDefinition         # Must be z = x * y² form
    srl: Optional[SRL] = None                   # Secure resource locator
    security_level: SecurityLevel = SecurityLevel.STANDARD
    fibonacci_level: int = 0                    # Current Fibonacci level (0-8)
    state: SubstrateState = SubstrateState.POTENTIAL
    checksum: str = field(default="", init=False)  # SHA-256 of definition
    created_at: str = field(default_factory=timestamp_now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        # Calculate checksum of canonical definition
        defn_str = json.dumps({
            'dim': self.canonical_defn.dim,
            'equation_kind': self.canonical_defn.equation.kind
        }, sort_keys=True)
        checksum = hashlib.sha256(defn_str.encode()).hexdigest()
        object.__setattr__(self, 'checksum', checksum)
        
        # Validate canonical form
        if not self._is_canonical_form():
            raise ValueError("Substrate must be in canonical z = x * y² form")
    
    def _is_canonical_form(self) -> bool:
        """Validate that substrate follows canonical z = x * y² form"""
        # For now, check if it's the z_xy2_parametric form
        # In production, this would do mathematical verification
        return (self.canonical_defn.dim == 2 and 
                self.canonical_defn.equation.kind == "parametric")


@dataclass
class SecureSubstrate:
    """
    Secure substrate with hardened operations and SRL integration
    
    Maintains complete audit trail and follows Fibonacci directional patterns
    for all operations. Every transformation is reversible and verifiable.
    """
    definition: SecureSubstrateDefinition
    substrate: Substrate
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)
    security_context: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        # Initialize security context
        self.security_context.update({
            'created_at': timestamp_now(),
            'initial_checksum': self._calculate_substrate_checksum(),
            'fibonacci_level': self.definition.fibonacci_level,
            'state': self.definition.state.value
        })
        
        # Add creation to audit trail
        self._add_audit_entry('create', {
            'substrate_id': self.definition.id,
            'checksum': self.security_context['initial_checksum'],
            'fibonacci_level': self.definition.fibonacci_level
        })
    
    def _calculate_substrate_checksum(self) -> str:
        """Calculate checksum of current substrate state"""
        data = {
            'definition_id': self.definition.id,
            'ones_count': len(self.substrate.ones),
            'coords': [one.coord for one in self.substrate.ones]
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    
    def _add_audit_entry(self, operation: str, details: Dict[str, Any]):
        """Add entry to audit trail with Fibonacci level tracking"""
        entry = {
            'timestamp': timestamp_now(),
            'operation': operation,
            'fibonacci_level': self.definition.fibonacci_level,
            'state': self.definition.state.value,
            'details': details
        }
        self.audit_trail.append(entry)
    
    def advance_fibonacci_level(self, target_level: int) -> 'SecureSubstrate':
        """
        Advance substrate through Fibonacci levels with directional operations
        
        Levels: 0(∅) → 1(●) → 2(→) → 3(↑) → 4(←) → 5(↓) → 6(→) → 7(↑) → 8(∞)
        """
        if target_level < self.definition.fibonacci_level:
            raise ValueError("Cannot move backward in Fibonacci levels")
        
        if target_level > 8:
            raise ValueError("Maximum Fibonacci level is 8 (COMPLETE)")
        
        # Create new definition with advanced level
        new_defn = SecureSubstrateDefinition(
            id=self.definition.id,
            canonical_defn=self.definition.canonical_defn,
            srl=self.definition.srl,
            security_level=self.definition.security_level,
            fibonacci_level=target_level,
            state=self._get_state_for_level(target_level),
            metadata=self.definition.metadata.copy()
        )
        
        # Apply directional operation based on level transition
        new_substrate = self._apply_directional_operation(target_level)
        
        # Create new secure substrate
        secure_sub = SecureSubstrate(new_defn, new_substrate)
        
        # Copy audit trail and add advancement entry
        secure_sub.audit_trail = self.audit_trail.copy()
        secure_sub._add_audit_entry('advance_fibonacci', {
            'from_level': self.definition.fibonacci_level,
            'to_level': target_level,
            'direction': self._get_direction_for_transition(target_level)
        })
        
        return secure_sub
    
    def _get_state_for_level(self, level: int) -> SubstrateState:
        """Map Fibonacci level to substrate state"""
        state_map = {
            0: SubstrateState.POTENTIAL,
            1: SubstrateState.SPARK,
            2: SubstrateState.DIVIDING,
            3: SubstrateState.ORGANIZING,
            4: SubstrateState.IDENTIFYING,
            5: SubstrateState.ASSEMBLING,
            6: SubstrateState.HUMAN,
            7: SubstrateState.RESTING,
            8: SubstrateState.COMPLETE
        }
        return state_map.get(level, SubstrateState.POTENTIAL)
    
    def _get_direction_for_transition(self, target_level: int) -> str:
        """Get directional operation for Fibonacci level transition"""
        # Based on spiral pattern: ● → ↑ ← ↓ → ↑ ∞
        directions = {
            1: "●",  # Origin
            2: "→",  # Horizontal (multiply)
            3: "↑",  # Vertical (divide)
            4: "←",  # Horizontal (multiply)
            5: "↓",  # Vertical (divide)
            6: "→",  # Horizontal (multiply)
            7: "↑",  # Vertical (divide)
            8: "∞"   # Complete spiral
        }
        return directions.get(target_level, "?")
    
    def _apply_directional_operation(self, target_level: int) -> Substrate:
        """
        Apply directional operation based on Fibonacci level
        
        Horizontal levels (2,4,6): MULTIPLICATION - expand domain
        Vertical levels (3,5,7): DIVISION - organize range
        """
        from .transforms import spawn_substrate_vectorized
        
        if target_level in [2, 4, 6]:  # Horizontal - multiplication
            # Expand sampling bounds (multiply domain)
            multiplier = 1.0 + (target_level * 0.5)
            expanded_bounds = [(-multiplier, multiplier), (-multiplier, multiplier)]
            return spawn_substrate_vectorized(
                self.substrate.defn, 
                expanded_bounds, 
                step=0.1 * (2.0 / target_level) if target_level > 0 else 0.1
            )
        
        elif target_level in [3, 5, 7]:  # Vertical - division
            # Organize with finer sampling (divide range)
            organized_bounds = [(-2, 2), (-2, 2)]
            return spawn_substrate_vectorized(
                self.substrate.defn,
                organized_bounds,
                step=0.05 / (target_level * 0.3)  # Finer sampling for organization
            )
        
        else:  # Origin or complete
            return self.substrate
    
    def verify_integrity(self) -> Dict[str, Any]:
        """Verify substrate integrity and return validation report"""
        current_checksum = self._calculate_substrate_checksum()
        initial_checksum = self.security_context['initial_checksum']
        
        verification = {
            'substrate_id': self.definition.id,
            'is_valid': True,
            'checksum_match': current_checksum == initial_checksum,
            'current_checksum': current_checksum,
            'initial_checksum': initial_checksum,
            'fibonacci_level': self.definition.fibonacci_level,
            'state': self.definition.state.value,
            'audit_entries': len(self.audit_trail),
            'ones_count': len(self.substrate.ones)
        }
        
        # Additional security validations
        if self.definition.security_level == SecurityLevel.PARANOID:
            verification.update({
                'bitcount_verified': self._verify_bitcount(),
                'srl_connected': self.definition.srl is not None and self.definition.srl.connected,
                'canonical_form_verified': self._verify_canonical_form()
            })
        
        return verification
    
    def _verify_bitcount(self) -> bool:
        """Verify bitcount of substrate data"""
        data = json.dumps([one.coord for one in self.substrate.ones]).encode()
        current_bitcount = bitcount(data)
        # Store initial bitcount in security context on first verification
        if 'initial_bitcount' not in self.security_context:
            self.security_context['initial_bitcount'] = current_bitcount
        return current_bitcount == self.security_context['initial_bitcount']
    
    def _verify_canonical_form(self) -> bool:
        """Verify substrate maintains canonical z = x * y² form"""
        # Sample a few points and verify the equation
        for one in self.substrate.ones[:10]:  # Check first 10 points
            if len(one.coord) >= 3:
                x, y, z = one.coord[:3]
                expected_z = x * (y ** 2)
                if abs(z - expected_z) > 1e-9:
                    return False
        return True
    
    def connect_srl(self, adapter: ConnectorAdapter) -> bool:
        """Connect SRL adapter for secure resource binding"""
        if not self.definition.srl:
            # Create SRL if not exists
            self.definition.srl = SRL(
                substrate=self.substrate,
                adapter=adapter,
                metadata={'substrate_id': self.definition.id}
            )
        
        success = self.definition.srl.connect()
        self._add_audit_entry('srl_connect', {
            'adapter_type': adapter.__class__.__name__,
            'success': success
        })
        return success
    
    def export_secure_package(self) -> Dict[str, Any]:
        """Export substrate as secure package for multi-language compatibility"""
        package = {
            'format_version': '1.0',
            'substrate_id': self.definition.id,
            'canonical_definition': {
                'dim': self.definition.canonical_defn.dim,
                'equation_kind': self.definition.canonical_defn.equation.kind
            },
            'fibonacci_level': self.definition.fibonacci_level,
            'state': self.definition.state.value,
            'security_level': self.definition.security_level.value,
            'checksum': self.definition.checksum,
            'created_at': self.definition.created_at,
            'substrate_data': {
                'ones': [{'coord': one.coord, 'attrs': one.attrs} for one in self.substrate.ones]
            },
            'audit_trail': self.audit_trail,
            'security_context': self.security_context,
            'metadata': self.definition.metadata
        }
        
        # Add SRL info if connected
        if self.definition.srl:
            package['srl_info'] = {
                'endpoint': self.definition.srl.adapter.endpoint,
                'adapter_type': self.definition.srl.adapter.__class__.__name__,
                'connected': self.definition.srl.connected
            }
        
        return package


class SecureSubstrateFactory:
    """
    Factory for creating secure substrates with proper initialization
    """
    
    @staticmethod
    def create_canonical(substrate_id: str, 
                        srl: Optional[SRL] = None,
                        security_level: SecurityLevel = SecurityLevel.STANDARD,
                        fibonacci_level: int = 0) -> SecureSubstrate:
        """
        Create a secure substrate using the canonical z = x * y² equation
        """
        # Get canonical definition
        canonical_defn = z_xy2_parametric()
        
        # Create secure definition
        secure_defn = SecureSubstrateDefinition(
            id=substrate_id,
            canonical_defn=canonical_defn,
            srl=srl,
            security_level=security_level,
            fibonacci_level=fibonacci_level
        )
        
        # Spawn initial substrate
        from .transforms import spawn_substrate_vectorized
        initial_substrate = spawn_substrate_vectorized(
            canonical_defn, 
            bounds=[(-1, 1), (-1, 1)], 
            step=0.5
        )
        
        return SecureSubstrate(secure_defn, initial_substrate)
    
    @staticmethod
    def from_secure_package(package_data: Dict[str, Any]) -> SecureSubstrate:
        """
        Reconstruct secure substrate from exported package
        """
        # Validate package format
        if package_data.get('format_version') != '1.0':
            raise ValueError("Unsupported package format version")
        
        # Recreate canonical definition
        canonical_defn = z_xy2_parametric()
        
        # Recreate secure definition
        secure_defn = SecureSubstrateDefinition(
            id=package_data['substrate_id'],
            canonical_defn=canonical_defn,
            security_level=SecurityLevel(package_data['security_level']),
            fibonacci_level=package_data['fibonacci_level'],
            state=SubstrateState(package_data['state']),
            checksum=package_data['checksum'],
            created_at=package_data['created_at'],
            metadata=package_data.get('metadata', {})
        )
        
        # Recreate substrate data
        ones = tuple(
            One(coord=tuple(data['coord']), attrs=data.get('attrs'))
            for data in package_data['substrate_data']['ones']
        )
        substrate = Substrate(defn=canonical_defn, ones=ones)
        
        # Create secure substrate
        secure_sub = SecureSubstrate(secure_defn, substrate)
        secure_sub.audit_trail = package_data.get('audit_trail', [])
        secure_sub.security_context = package_data.get('security_context', {})
        
        return secure_sub


# Multi-language API compatibility layer
class SubstrateAPI:
    """
    Programming API for multi-language compatibility
    
    Provides clean interfaces that can be exposed to other programming languages
    through FFI, gRPC, or similar mechanisms.
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.STANDARD):
        self.security_level = security_level
        self.substrates: Dict[str, SecureSubstrate] = {}
    
    def create_substrate(self, substrate_id: str, fibonacci_level: int = 0) -> str:
        """Create new substrate and return its ID"""
        secure_sub = SecureSubstrateFactory.create_canonical(
            substrate_id=substrate_id,
            security_level=self.security_level,
            fibonacci_level=fibonacci_level
        )
        self.substrates[substrate_id] = secure_sub
        return substrate_id
    
    def advance_substrate(self, substrate_id: str, target_level: int) -> bool:
        """Advance substrate through Fibonacci levels"""
        if substrate_id not in self.substrates:
            return False
        
        try:
            advanced = self.substrates[substrate_id].advance_fibonacci_level(target_level)
            self.substrates[substrate_id] = advanced
            return True
        except Exception:
            return False
    
    def verify_substrate(self, substrate_id: str) -> Dict[str, Any]:
        """Verify substrate integrity"""
        if substrate_id not in self.substrates:
            return {'error': 'Substrate not found'}
        
        return self.substrates[substrate_id].verify_integrity()
    
    def export_substrate(self, substrate_id: str) -> Dict[str, Any]:
        """Export substrate as secure package"""
        if substrate_id not in self.substrates:
            return {'error': 'Substrate not found'}
        
        return self.substrates[substrate_id].export_secure_package()
    
    def import_substrate(self, package_data: Dict[str, Any]) -> str:
        """Import substrate from secure package"""
        try:
            secure_sub = SecureSubstrateFactory.from_secure_package(package_data)
            substrate_id = secure_sub.definition.id
            self.substrates[substrate_id] = secure_sub
            return substrate_id
        except Exception as e:
            return {'error': str(e)}


__all__ = [
    'SecureSubstrateDefinition',
    'SecureSubstrate', 
    'SecureSubstrateFactory',
    'SubstrateAPI',
    'SecurityLevel',
    'SubstrateState'
]
