"""
ButterflyFX Kernel - Dimensional Computing Foundation

A computational paradigm that replaces tree-based hierarchical structures 
with a 7-level dimensional helix model based on ordered growth (golden ratio).

Core Insight: Why iterate through N points when you can invoke a single 
dimensional transition?

Copyright (c) 2024-2026 Kenneth Bingham. All Rights Reserved.
Licensed under CC BY 4.0 (Creative Commons Attribution 4.0 International)

Author: Kenneth Bingham <keneticsart@gmail.com>
Website: https://butterflyfx.us
"""

__version__ = "1.0.0"
__author__ = "Kenneth Bingham"
__email__ = "keneticsart@gmail.com"
__license__ = "CC BY 4.0"

# Mathematical Kernel
from .kernel import HelixKernel

# Generative Manifold
from .manifold import GenerativeManifold

# Token Substrate
from .substrate import ManifoldSubstrate

# Dimensional Primitives
from .primitives import (
    DimensionalPrimitive,
    HelixToken,
    HelixLevel,
)

# 3D Graphics Mathematics
from .graphics3d import (
    Vec3,
    Mat4,
    Transform3D,
)

# Foundation (Database, Filesystem, Store, Graph)
from .foundation import (
    HelixDB,
    HelixFS,
    HelixStore,
    HelixGraph,
)

# Utilities
from .utilities import (
    HelixPath,
    HelixQuery,
    HelixCache,
    HelixSerializer,
)

# Networking
from .transport import HelixTransport
from .audio_transport import AudioTransport
from .manifold_server import ManifoldServer

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    
    # Core kernel
    "HelixKernel",
    "GenerativeManifold",
    "ManifoldSubstrate",
    
    # Primitives
    "DimensionalPrimitive",
    "HelixToken",
    "HelixLevel",
    
    # Graphics
    "Vec3",
    "Mat4",
    "Transform3D",
    
    # Foundation
    "HelixDB",
    "HelixFS",
    "HelixStore",
    "HelixGraph",
    
    # Utilities
    "HelixPath",
    "HelixQuery",
    "HelixCache",
    "HelixSerializer",
    
    # Networking
    "HelixTransport",
    "AudioTransport",
    "ManifoldServer",
]
