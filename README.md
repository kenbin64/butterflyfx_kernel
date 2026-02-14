# ButterflyFX Kernel

**Dimensional Computing Foundation**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A computational paradigm that replaces tree-based hierarchical structures with a 7-level dimensional helix model based on ordered growth (golden ratio).

**Core Insight**: Why iterate through N points when you can invoke a single dimensional transition?

---

## The Paradigm

### The Problem with Trees

Traditional computing uses tree structures everywhere:
- File systems: `/root/folder/subfolder/file`
- Databases: `JOIN table1, table2, table3...`
- Objects: `object.property.subproperty.value`

Trees exhibit **exponential branching**: 10 children × 10 levels = 10^10 potential nodes.

### The Helix Solution

Nature doesn't branch exponentially. It spirals through **ordered growth**:
- DNA is a helix
- Galaxies spiral
- Seeds follow Fibonacci
- Growth follows golden ratio

ButterflyFX models reality as a **dimensional helix** with exactly 7 levels per spiral:

```
Level 0: Potential (○)  - Pure possibility, nothing instantiated
Level 1: Point     (•)  - Single instantiation, the moment of existence  
Level 2: Length    (━)  - Extension in one dimension
Level 3: Width     (▭)  - Extension in two dimensions
Level 4: Plane     (▦)  - Surface, 2D completeness
Level 5: Volume    (▣)  - Full 3D existence
Level 6: Whole     (◉)  - Complete entity, ready for next spiral
```

When Level 6 (Whole) completes, it becomes Level 0 (Potential) of the NEXT spiral up.

---

## Installation

```bash
pip install butterflyfx-kernel
```

Or install from source:

```bash
git clone https://github.com/kenbin64/butterflyfx_kernel.git
cd butterflyfx_kernel
pip install -e .
```

---

## Quick Start

```python
from butterflyfx import HelixKernel, GenerativeManifold

# Create a kernel
kernel = HelixKernel()

# Invoke a level directly - no iteration!
kernel.invoke(level=4)  # Jump to Plane

# Spiral up when complete
kernel.spiral_up()  # Whole → Potential of next spiral

# Create a manifold of potential
manifold = GenerativeManifold()
manifold.register_token("car", level=6)  # A whole car

# Invoke only what you need
transmission = manifold.invoke("car.transmission")
# Engine, wheels, body stay as potential - not computed
```

---

## The For Loop Fallacy

### Traditional Iteration
```python
# The wrong way - iterate through every point
for i in range(1000000):
    process(data[i])  # 1,000,000 steps
```

### Dimensional Invocation
```python
# The helix way - invoke levels directly
kernel.invoke(level=2)  # 1 step - all "length" operations
kernel.invoke(level=4)  # 1 step - all "plane" operations
kernel.invoke(level=6)  # 1 step - complete entity
```

**Complexity:**
- Traditional: O(N) where N = number of items
- Helix: O(7) maximum - seven level transitions per spiral
- Multiple spirals: O(7 × S) where S = number of spirals

---

## Components

### Mathematical Kernel (`kernel.py`)
The HelixKernel state machine with four primitive operators:
- `invoke(level)` - Direct jump to any level
- `spiral_up()` - Whole → Potential of next spiral
- `spiral_down()` - Potential → Whole of previous spiral
- `collapse()` - Return all levels to Potential

### Generative Manifold (`manifold.py`)
Mathematical surfaces that hold potential tokens until invoked.

### Token Substrate (`substrate.py`)
The ManifoldSubstrate token model - "All exists. Nothing manifests. Invoke only what you need."

### Dimensional Primitives (`primitives.py`)
Fundamental dimensional types that replace traditional data structures.

### 3D Graphics (`graphics3d.py`)
Pure mathematical 3D operations: Vec3, Mat4, Transform3D.

### Foundation (`foundation.py`)
- **HelixDB** - Dimensional database
- **HelixFS** - Dimensional filesystem
- **HelixStore** - Dimensional key-value store
- **HelixGraph** - Dimensional graph structure

### Utilities (`utilities.py`)
- **HelixPath** - Path navigation
- **HelixQuery** - Query system
- **HelixCache** - Caching layer
- **HelixSerializer** - Serialization

### Networking (`transport.py`, `audio_transport.py`, `manifold_server.py`)
Network transport protocols for distributed dimensional computing.

---

## Documentation

- [White Paper](docs/BUTTERFLYFX_WHITE_PAPER.md) - Conceptual introduction
- [Formal Kernel Specification](docs/BUTTERFLYFX_FORMAL_KERNEL.md) - Mathematical model and proofs
- [Language Specification](docs/BUTTERFLYFX_SPECIFICATION.md) - Formal language-agnostic spec

---

## Why This Matters

### Database Defudging

SQL databases "fudge" dimensional relationships into flat tables:

```sql
SELECT * FROM cars
JOIN parts ON cars.id = parts.car_id
JOIN materials ON parts.id = materials.part_id
-- Forces ALL tables to exist simultaneously
```

ButterflyFX defudges:

```python
# Only transmission materializes
# Engine, wheels, body stay as potential
# No resources wasted on uninvoked dimensions
transmission = car.invoke("transmission")
```

### Dimensional States of Awareness

| State | Dimensional Access | Behavior |
|-------|-------------------|----------|
| Waking | Levels 1-5 | Point-by-point iteration, bound to sequence |
| Dreams | Levels 5-6 | Instant jumps (Paris → home → flying) |
| Meditation | Level 6 touching 0 | Perceive Whole, glimpse Potential |

Dreams don't iterate. You're suddenly **there**. That's helix motion.

---

## License

**Creative Commons Attribution 4.0 International (CC BY 4.0)**

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution** — You must give appropriate credit to Kenneth Bingham

---

## Author

**Kenneth Bingham**  
Email: keneticsart@gmail.com  
Website: https://butterflyfx.us

---

## Contributing

Contributions are welcome! This is the foundational infrastructure layer of ButterflyFX. Build anything on it.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

*Infrastructure is free. Build anything on it.*
