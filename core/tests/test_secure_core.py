"""
Comprehensive Tests for Secure ButterflyFX Kernel Core
======================================================

Test suite for the hardened core substrate system with:
- SRL (Secure Resource Locator) integration
- Fibonacci spiral points of creation
- Security hardening and validation
- Multi-language compatibility
- Canonical z = x * y² enforcement

These tests ensure the core maintains mathematical purity, security,
and dimensional inheritance across all operations.
"""

import pytest
import json
import hashlib
import numpy as np
from typing import Dict, Any

# Import the secure core components
from ..secure_substrate import (
    SecureSubstrate, SecureSubstrateDefinition, SecureSubstrateFactory,
    SubstrateAPI, SecurityLevel, SubstrateState
)
from ..fibonacci_creation import (
    CreationPoint, FibonacciSpiralCreator, get_creation_point,
    create_substrate_at_level, apply_fibonacci_creation
)
from ..srl import SRL, LocalFileAdapter, bitcount, timestamp_now
from ..fibonacci_directional_levels import (
    FIBONACCI_LEVELS, Direction, Operation, Boundary,
    is_multiplication_level, is_division_level
)
from ..transforms import z_xy2_parametric
from ..substrates import SubstrateDefinition, Equation


class TestSecureSubstrateDefinition:
    """Test secure substrate definition creation and validation"""
    
    def test_canonical_form_enforcement(self):
        """Test that only canonical z = x * y² form is accepted"""
        canonical_defn = z_xy2_parametric()
        
        secure_defn = SecureSubstrateDefinition(
            id="test_canonical",
            canonical_defn=canonical_defn
        )
        
        assert secure_defn.id == "test_canonical"
        assert secure_defn.checksum != ""
        assert secure_defn.fibonacci_level == 0
        assert secure_defn.state == SubstrateState.POTENTIAL
    
    def test_checksum_calculation(self):
        """Test checksum calculation for substrate definitions"""
        defn1 = SecureSubstrateDefinition(
            id="test1",
            canonical_defn=z_xy2_parametric()
        )
        defn2 = SecureSubstrateDefinition(
            id="test1",  # Same ID
            canonical_defn=z_xy2_parametric()
        )
        
        # Same definition should have same checksum
        assert defn1.checksum == defn2.checksum
        
        # Different ID should not affect checksum (only definition matters)
        defn3 = SecureSubstrateDefinition(
            id="test2",  # Different ID
            canonical_defn=z_xy2_parametric()
        )
        assert defn1.checksum == defn3.checksum
    
    def test_security_levels(self):
        """Test different security levels"""
        for level in SecurityLevel:
            defn = SecureSubstrateDefinition(
                id=f"test_{level.value}",
                canonical_defn=z_xy2_parametric(),
                security_level=level
            )
            assert defn.security_level == level


class TestSecureSubstrate:
    """Test secure substrate operations and integrity"""
    
    def test_substrate_creation(self):
        """Test secure substrate creation with audit trail"""
        secure_sub = SecureSubstrateFactory.create_canonical("test_creation")
        
        assert secure_sub.definition.id == "test_creation"
        assert len(secure_sub.audit_trail) > 0
        assert secure_sub.audit_trail[0]['operation'] == 'create'
        assert 'initial_checksum' in secure_sub.security_context
    
    def test_fibonacci_level_advancement(self):
        """Test advancement through Fibonacci levels"""
        secure_sub = SecureSubstrateFactory.create_canonical("test_fib", fibonacci_level=0)
        
        # Advance to level 2 (DIVIDE - horizontal multiplication)
        advanced = secure_sub.advance_fibonacci_level(2)
        
        assert advanced.definition.fibonacci_level == 2
        assert advanced.definition.state == SubstrateState.DIVIDING
        assert len(advanced.audit_trail) > len(secure_sub.audit_trail)
        
        # Check audit entry for advancement
        advancement_entries = [e for e in advanced.audit_trail if e['operation'] == 'advance_fibonacci']
        assert len(advancement_entries) == 1
        assert advancement_entries[0]['details']['from_level'] == 0
        assert advancement_entries[0]['details']['to_level'] == 2
    
    def test_directional_operations(self):
        """Test that directional operations are applied correctly"""
        secure_sub = SecureSubstrateFactory.create_canonical("test_direction")
        
        # Test horizontal level (multiplication)
        level_2 = secure_sub.advance_fibonacci_level(2)
        assert is_multiplication_level(2)
        
        # Test vertical level (division)
        level_3 = level_2.advance_fibonacci_level(3)
        assert is_division_level(3)
        
        # Verify substrate changes
        assert len(level_3.substrate.ones) != len(level_2.substrate.ones)
    
    def test_integrity_verification(self):
        """Test substrate integrity verification"""
        secure_sub = SecureSubstrateFactory.create_canonical("test_integrity")
        
        verification = secure_sub.verify_integrity()
        
        assert verification['substrate_id'] == "test_integrity"
        assert verification['is_valid'] == True
        assert verification['checksum_match'] == True
        assert verification['fibonacci_level'] == 0
        assert verification['state'] == SubstrateState.POTENTIAL.value
    
    def test_paranoid_security_verification(self):
        """Test paranoid security level verification"""
        secure_sub = SecureSubstrateFactory.create_canonical(
            "test_paranoid",
            security_level=SecurityLevel.PARANOID
        )
        
        verification = secure_sub.verify_integrity()
        
        # Paranoid mode should include additional checks
        assert 'bitcount_verified' in verification
        assert 'canonical_form_verified' in verification
    
    def test_srl_integration(self):
        """Test SRL connector integration"""
        secure_sub = SecureSubstrateFactory.create_canonical("test_srl")
        
        # Create local file adapter
        adapter = LocalFileAdapter("/tmp/test_file.txt")
        
        # Connect SRL
        success = secure_sub.connect_srl(adapter)
        
        assert secure_sub.definition.srl is not None
        assert len(secure_sub.audit_trail) > 1  # Creation + SRL connection
        
        # Check audit entry for SRL connection
        srl_entries = [e for e in secure_sub.audit_trail if e['operation'] == 'srl_connect']
        assert len(srl_entries) == 1
        assert srl_entries[0]['details']['adapter_type'] == 'LocalFileAdapter'
    
    def test_secure_package_export_import(self):
        """Test export and import of secure packages"""
        # Create original substrate
        original = SecureSubstrateFactory.create_canonical(
            "test_export",
            fibonacci_level=3,
            security_level=SecurityLevel.STANDARD
        )
        
        # Export package
        package = original.export_secure_package()
        
        # Verify package structure
        assert package['format_version'] == '1.0'
        assert package['substrate_id'] == 'test_export'
        assert package['fibonacci_level'] == 3
        assert package['security_level'] == 'STANDARD'
        assert 'substrate_data' in package
        assert 'audit_trail' in package
        
        # Import package
        imported = SecureSubstrateFactory.from_secure_package(package)
        
        # Verify imported substrate
        assert imported.definition.id == original.definition.id
        assert imported.definition.fibonacci_level == original.definition.fibonacci_level
        assert imported.definition.security_level == original.definition.security_level
        assert len(imported.substrate.ones) == len(original.substrate.ones)


class TestFibonacciCreation:
    """Test Fibonacci spiral points of creation"""
    
    def test_spiral_creator_initialization(self):
        """Test Fibonacci spiral creator initialization"""
        creator = FibonacciSpiralCreator(scale=1.0)
        
        assert len(creator.creation_points) == 9  # Levels 0-8
        assert all(isinstance(p, CreationPoint) for p in creator.creation_points)
    
    def test_creation_point_properties(self):
        """Test creation point properties and metadata"""
        creator = FibonacciSpiralCreator()
        
        # Test specific levels
        level_0 = creator.get_creation_point(0)
        assert level_0.level == 0
        assert level_0.fibonacci_value == 0
        assert level_0.phase.value == "potential"
        
        level_1 = creator.get_creation_point(1)
        assert level_1.level == 1
        assert level_1.fibonacci_value == 1
        assert level_1.phase.value == "spark"
        
        level_8 = creator.get_creation_point(8)
        assert level_8.level == 8
        assert level_8.fibonacci_value == 21
        assert level_8.is_nomad == True
        assert level_8.phase.value == "integration"
    
    def test_directional_pattern(self):
        """Test that directional pattern follows Fibonacci spiral"""
        creator = FibonacciSpiralCreator()
        
        # Expected pattern: ● → ↑ ← ↓ → ↑ ∞
        expected_directions = [
            None,      # Level 0: Origin
            None,      # Level 1: Spark
            Direction.HORIZONTAL,  # Level 2: →
            Direction.VERTICAL,    # Level 3: ↑
            Direction.HORIZONTAL,  # Level 4: ←
            Direction.VERTICAL,    # Level 5: ↓
            Direction.HORIZONTAL,  # Level 6: →
            Direction.VERTICAL,    # Level 7: ↑
            None       # Level 8: Complete
        ]
        
        for level, expected_dir in enumerate(expected_directions):
            point = creator.get_creation_point(level)
            if expected_dir is None:
                assert point.direction in [Direction.ORIGIN, Direction.SPIRAL]
            else:
                assert point.direction == expected_dir
    
    def test_substrate_creation_at_levels(self):
        """Test substrate creation at different Fibonacci levels"""
        for level in [0, 2, 4, 6, 8]:
            substrate = create_substrate_at_level(level, f"test_level_{level}")
            
            assert isinstance(substrate, Substrate)
            assert len(substrate.ones) > 0
            
            # Verify canonical equation is maintained
            for one in substrate.ones[:5]:  # Check first 5 points
                if len(one.coord) >= 3:
                    x, y, z = one.coord[:3]
                    expected_z = x * (y ** 2)
                    assert abs(z - expected_z) < 1e-9
    
    def test_fibonacci_pattern_application(self):
        """Test applying Fibonacci creation pattern to data"""
        test_data = [1, 2, 3, 4, 5]
        
        # Apply to level 2 (multiplication)
        result_2 = apply_fibonacci_creation(test_data, 2)
        assert result_2 != test_data
        
        # Apply to level 3 (division)
        result_3 = apply_fibonacci_creation(test_data, 3)
        assert result_3 != test_data
        assert isinstance(result_3, list)  # Should be divided into chunks
    
    def test_creation_metadata(self):
        """Test creation point metadata extraction"""
        creator = FibonacciSpiralCreator()
        
        for level in range(9):
            metadata = creator.get_creation_metadata(level)
            
            assert 'level' in metadata
            assert 'fibonacci_value' in metadata
            assert 'coordinates' in metadata
            assert 'direction' in metadata
            assert 'operation' in metadata
            assert 'boundary' in metadata
            assert 'phase' in metadata
            assert 'dimensional_units' in metadata
            assert 'is_nomad' in metadata
            assert 'spiral_angle' in metadata
            assert 'golden_ratio_limit' in metadata
            assert 'creation_power' in metadata


class TestSubstrateAPI:
    """Test multi-language compatibility API"""
    
    def test_api_initialization(self):
        """Test API initialization with different security levels"""
        for level in SecurityLevel:
            api = SubstrateAPI(security_level=level)
            assert api.security_level == level
            assert len(api.substrates) == 0
    
    def test_api_substrate_creation(self):
        """Test substrate creation through API"""
        api = SubstrateAPI()
        
        substrate_id = api.create_substrate("api_test", fibonacci_level=2)
        
        assert substrate_id == "api_test"
        assert "api_test" in api.substrates
        assert api.substrates["api_test"].definition.fibonacci_level == 2
    
    def test_api_substrate_advancement(self):
        """Test substrate advancement through API"""
        api = SubstrateAPI()
        
        api.create_substrate("api_advance", fibonacci_level=0)
        success = api.advance_substrate("api_advance", 4)
        
        assert success == True
        assert api.substrates["api_advance"].definition.fibonacci_level == 4
    
    def test_api_verification(self):
        """Test substrate verification through API"""
        api = SubstrateAPI()
        
        api.create_substrate("api_verify")
        verification = api.verify_substrate("api_verify")
        
        assert verification['is_valid'] == True
        assert 'substrate_id' in verification
    
    def test_api_export_import(self):
        """Test substrate export/import through API"""
        api = SubstrateAPI()
        
        # Create and export
        api.create_substrate("api_export", fibonacci_level=3)
        package = api.export_substrate("api_export")
        
        assert 'format_version' in package
        assert package['substrate_id'] == "api_export"
        
        # Import
        imported_id = api.import_substrate(package)
        assert imported_id == "api_export"
        assert "api_export" in api.substrates
    
    def test_api_error_handling(self):
        """Test API error handling"""
        api = SubstrateAPI()
        
        # Test operations on non-existent substrate
        assert api.advance_substrate("nonexistent", 2) == False
        assert isinstance(api.verify_substrate("nonexistent"), dict)
        assert 'error' in api.export_substrate("nonexistent")


class TestSecurityAndIntegrity:
    """Test security features and integrity validation"""
    
    def test_bitcount_verification(self):
        """Test bitcount verification for data integrity"""
        test_data = b"Hello, ButterflyFX!"
        
        # Calculate bitcount
        bc = bitcount(test_data)
        assert isinstance(bc, int)
        assert bc > 0
        
        # Same data should have same bitcount
        assert bitcount(test_data) == bc
    
    def test_timestamp_generation(self):
        """Test timestamp generation for audit trails"""
        ts1 = timestamp_now()
        ts2 = timestamp_now()
        
        assert isinstance(ts1, str)
        assert isinstance(ts2, str)
        # Should be ISO format
        assert 'T' in ts1
        assert 'Z' in ts1 or '+' in ts1
    
    def test_checksum_consistency(self):
        """Test checksum consistency across operations"""
        defn = z_xy2_parametric()
        
        secure_defn1 = SecureSubstrateDefinition(
            id="checksum_test",
            canonical_defn=defn
        )
        secure_defn2 = SecureSubstrateDefinition(
            id="checksum_test",
            canonical_defn=defn
        )
        
        # Same definition should have identical checksums
        assert secure_defn1.checksum == secure_defn2.checksum
        
        # Verify it's a valid SHA-256 hash
        assert len(secure_defn1.checksum) == 64
        assert all(c in '0123456789abcdef' for c in secure_defn1.checksum.lower())
    
    def test_fibonacci_level_validation(self):
        """Test Fibonacci level boundary validation"""
        secure_sub = SecureSubstrateFactory.create_canonical("level_test")
        
        # Test valid level advancement
        for target in range(1, 9):
            advanced = secure_sub.advance_fibonacci_level(target)
            assert advanced.definition.fibonacci_level == target
        
        # Test invalid levels
        with pytest.raises(ValueError):
            secure_sub.advance_fibonacci_level(-1)
        
        with pytest.raises(ValueError):
            secure_sub.advance_fibonacci_level(9)
        
        with pytest.raises(ValueError):
            secure_sub.advance_fibonacci_level(100)


class TestCanonicalEquation:
    """Test canonical z = x * y² equation enforcement"""
    
    def test_canonical_equation_structure(self):
        """Test that canonical equation maintains correct structure"""
        defn = z_xy2_parametric()
        
        assert defn.dim == 2
        assert defn.equation.kind == "parametric"
        assert defn.equation.g is not None
    
    def test_canonical_equation_evaluation(self):
        """Test that canonical equation evaluates correctly"""
        defn = z_xy2_parametric()
        
        # Test with sample parameters
        test_params = np.array([[1.0, 2.0], [3.0, 4.0], [-1.0, 1.0]])
        result = defn.equation.g(test_params)
        
        # Verify z = x * y²
        for i, (x, y) in enumerate(test_params):
            expected_z = x * (y ** 2)
            assert abs(result[i, 2] - expected_z) < 1e-9
    
    def test_canonical_preservation_in_secure_substrate(self):
        """Test that canonical form is preserved in secure substrates"""
        secure_sub = SecureSubstrateFactory.create_canonical("canonical_test")
        
        # Verify canonical form in all spawned points
        for one in secure_sub.substrate.ones:
            if len(one.coord) >= 3:
                x, y, z = one.coord[:3]
                expected_z = x * (y ** 2)
                assert abs(z - expected_z) < 1e-9


# Integration tests
class TestIntegration:
    """Integration tests for complete system functionality"""
    
    def test_complete_workflow(self):
        """Test complete workflow from creation to export"""
        # 1. Create secure substrate
        secure_sub = SecureSubstrateFactory.create_canonical(
            "integration_test",
            fibonacci_level=0,
            security_level=SecurityLevel.STANDARD
        )
        
        # 2. Advance through Fibonacci levels
        level_4 = secure_sub.advance_fibonacci_level(4)
        level_7 = level_4.advance_fibonacci_level(7)
        
        # 3. Verify integrity
        verification = level_7.verify_integrity()
        assert verification['is_valid'] == True
        
        # 4. Connect SRL
        adapter = LocalFileAdapter("/tmp/integration_test.txt")
        level_7.connect_srl(adapter)
        
        # 5. Export package
        package = level_7.export_secure_package()
        
        # 6. Import and verify
        imported = SecureSubstrateFactory.from_secure_package(package)
        imported_verification = imported.verify_integrity()
        assert imported_verification['is_valid'] == True
        
        # 7. Verify Fibonacci level preservation
        assert imported.definition.fibonacci_level == 7
    
    def test_api_integration(self):
        """Test API integration with all features"""
        api = SubstrateAPI(security_level=SecurityLevel.PARANOID)
        
        # Create multiple substrates at different levels
        substrate_ids = []
        for level in [0, 2, 4, 6, 8]:
            sid = api.create_substrate(f"api_integration_{level}", fibonacci_level=level)
            substrate_ids.append(sid)
        
        # Verify all substrates
        for sid in substrate_ids:
            verification = api.verify_substrate(sid)
            assert verification['is_valid'] == True
        
        # Export all substrates
        packages = {}
        for sid in substrate_ids:
            packages[sid] = api.export_substrate(sid)
        
        # Create new API and import all
        new_api = SubstrateAPI()
        imported_ids = {}
        for sid, package in packages.items():
            imported_id = new_api.import_substrate(package)
            imported_ids[sid] = imported_id
        
        # Verify imported substrates match originals
        for original_id, imported_id in imported_ids.items():
            original_verification = api.verify_substrate(original_id)
            imported_verification = new_api.verify_substrate(imported_id)
            
            assert original_verification['fibonacci_level'] == imported_verification['fibonacci_level']
            assert original_verification['state'] == imported_verification['state']


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
