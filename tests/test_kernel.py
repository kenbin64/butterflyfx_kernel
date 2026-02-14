"""
ButterflyFX Kernel - Basic Tests

Tests for the dimensional computing kernel.

Author: Kenneth Bingham <keneticsart@gmail.com>
License: CC BY 4.0
"""

import pytest


class TestHelixKernel:
    """Tests for the HelixKernel state machine."""
    
    def test_kernel_initialization(self):
        """Test that kernel initializes at spiral 0, level 0."""
        from butterflyfx import HelixKernel
        
        kernel = HelixKernel()
        assert kernel.spiral == 0
        assert kernel.level == 0
    
    def test_invoke_level(self):
        """Test direct level invocation."""
        from butterflyfx import HelixKernel
        
        kernel = HelixKernel()
        
        # Invoke level 4 directly (no iteration)
        kernel.invoke(level=4)
        assert kernel.level == 4
        assert kernel.spiral == 0
    
    def test_invoke_all_levels(self):
        """Test invoking all 7 levels."""
        from butterflyfx import HelixKernel
        
        kernel = HelixKernel()
        
        for level in range(7):
            kernel.invoke(level=level)
            assert kernel.level == level
    
    def test_spiral_up(self):
        """Test spiraling up from Whole to next Potential."""
        from butterflyfx import HelixKernel
        
        kernel = HelixKernel()
        kernel.invoke(level=6)  # Go to Whole
        
        kernel.spiral_up()
        
        assert kernel.spiral == 1
        assert kernel.level == 0
    
    def test_spiral_down(self):
        """Test spiraling down from Potential to previous Whole."""
        from butterflyfx import HelixKernel
        
        kernel = HelixKernel()
        kernel.spiral_up()  # Go to spiral 1
        
        kernel.spiral_down()
        
        assert kernel.spiral == 0
        assert kernel.level == 6
    
    def test_collapse(self):
        """Test collapsing to Potential."""
        from butterflyfx import HelixKernel
        
        kernel = HelixKernel()
        kernel.invoke(level=5)
        
        kernel.collapse()
        
        assert kernel.level == 0


class TestGenerativeManifold:
    """Tests for the GenerativeManifold."""
    
    def test_manifold_creation(self):
        """Test manifold initialization."""
        from butterflyfx import GenerativeManifold
        
        manifold = GenerativeManifold()
        assert manifold is not None


class TestDimensionalPrimitives:
    """Tests for dimensional primitives."""
    
    def test_vec3(self):
        """Test Vec3 creation."""
        from butterflyfx import Vec3
        
        v = Vec3(1.0, 2.0, 3.0)
        assert v.x == 1.0
        assert v.y == 2.0
        assert v.z == 3.0


class TestFoundation:
    """Tests for foundation components."""
    
    def test_helix_db(self):
        """Test HelixDB creation."""
        from butterflyfx import HelixDB
        
        db = HelixDB()
        assert db is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
