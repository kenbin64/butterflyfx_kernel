# AI Directive: Coding with ButterflyFX Kernel

## Purpose
This document guides AI assistants in helping developers build applications using the ButterflyFX Kernel. Follow these directives to ensure correct, idiomatic, and performant code.

## Core Principles

### 1. Source of Truth
The kernel primitives in `core/substrates.py` define the contract:
- Equations are implicit (`f(p) = 0`) or parametric (`p = g(u)`)
- Sampling is via `spawn_substrate(defn, bounds, step)`
- Lenses are pure observers that do not mutate substrates
- All behavior is validated by tests in `core/tests/`

### 2. Immutability First
- Substrates, definitions, and ones are **frozen/immutable**
- Lenses project, never modify
- Transforms return new definitions, not modified copies
- Use functional composition over mutation

### 3. Performance Awareness
```python
# PREFER: Parametric for known surfaces (faster)
defn = SubstrateDefinition(dim=2, equation=Equation.parametric(lambda u: [u[0], u[1], u[0]*u[1]]))

# AVOID: Implicit when parametric is available (slower, samples N^D space)
# Only use implicit when natural constraint: f(p) = 0
```

## Code Generation Guidelines

### When User Wants a Manifold

**Ask these questions mentally:**
1. Is this a known parametric surface? → Use parametric form
2. Is this a constraint/implicit relationship? → Use implicit form
3. What's the natural parameter space dimensionality?

**Example: "Create a helix"**
```python
from core import Equation, SubstrateDefinition, spawn_substrate
import math

# Helix is naturally parametric (1D parameter -> 3D space)
helix = SubstrateDefinition(
    dim=1,
    equation=Equation.parametric(
        lambda u: [math.cos(u[0]), math.sin(u[0]), u[0] / math.pi]
    )
)

substrate = spawn_substrate(helix, bounds=[(0, 4*math.pi)], step=0.1)
```

### When User Wants to Observe/Analyze

**Use appropriate lens:**
- Quick stats? → `StatsLens()`
- Statistical analysis? → `AggregationLens()`
- Custom domain? → Create custom `Lens[T]`

**Example: "Get the bounds and center"**
```python
from core.lenses import StatsLens

stats = StatsLens().project(substrate)
print(f"Bounds: {stats['bounds']}")
print(f"Center: {stats['centroid']}")
```

### When User Mentions "Golden Ratio" or "Phi" or "33 Steps"

**Use phi recursion tools:**
```python
from core.substrates import generate_cycle, spawn_at_state
from core.phi_lens import PhiCycleLens

# Generate cycle (33 expansions + collapse)
cycle = generate_cycle(base_definition)

# Project at each step
cycle_lens = PhiCycleLens(projector=StatsLens(), bounds=[(0,1)], step=0.1)
results = cycle_lens.project(base_definition)
```

### When User Wants Transformation

**Use transform helpers, not manual equation rewriting:**
```python
from core.transforms import translate_definition, scale_definition

# PREFER this
shifted = translate_definition(defn, offsets=[5, 0])
scaled = scale_definition(shifted, factors=2.0)

# AVOID manual equation wrapping (error-prone)
```

## Common Request Patterns

### "Create a [shape] manifold"
1. Identify if parametric or implicit
2. Define equation with correct dimensionality
3. Provide sensible default bounds and step
4. Return spawned substrate

### "Analyze this substrate"
1. Identify what user wants to know
2. Pick appropriate lens (Stats/Aggregation/Custom)
3. Project and return human-readable results

### "Scale/move this manifold"
1. Use `translate_definition` or `scale_definition`
2. Re-spawn if needed
3. Show before/after if helpful

### "Make this faster"
1. Check if parametric form available
2. Suggest larger step size
3. Consider budget guard if sampling is unbounded
4. Profile if needed

## Error Prevention

### Common Mistakes to Avoid

**❌ Dimension mismatch**
```python
# BAD: 2D equation, 3D bounds
defn = SubstrateDefinition(dim=2, equation=...)
spawn_substrate(defn, bounds=[(0,1), (0,1), (0,1)], step=1)  # ERROR
```

**✅ Correct**
```python
defn = SubstrateDefinition(dim=2, equation=...)
spawn_substrate(defn, bounds=[(0,1), (0,1)], step=1)
```

**❌ Mutating substrate**
```python
# BAD: Trying to modify frozen dataclass
substrate.ones.append(One(coord=(1,2)))  # ERROR
```

**✅ Correct**
```python
# Create new substrate or use lens to project
new_ones = substrate.ones + (One(coord=(1,2)),)
new_substrate = Substrate(defn=substrate.defn, ones=new_ones)
```

**❌ Lambda closure bugs**
```python
# BAD: Loop variable capture
for i in range(3):
    eq = Equation.parametric(lambda u: [u[0] * i])  # i captured by reference!
```

**✅ Correct**
```python
for i in range(3):
    eq = Equation.parametric(lambda u, scale=i: [u[0] * scale])
```

## Code Style

### Imports
```python
# PREFER: Import core primitives directly
from core import Equation, SubstrateDefinition, spawn_substrate

# PREFER: Import modules for optional features
from core.lenses import StatsLens
from core.phi_lens import PhiCycleLens
from core.decider import choose_definition
```

### Naming
- Definitions: `defn`, `surface_defn`, `helix_defn`
- Substrates: `substrate`, `sub`, `spawned_surface`
- Lenses: descriptive names like `stats_lens`, `color_mapper`
- Results: `result`, `stats`, `projection`

### Comments
```python
# PREFER: Explain the math/intent
# Parametric helix: x=cos(t), y=sin(t), z=t/π
helix = SubstrateDefinition(...)

# AVOID: Obvious comments
# Create a substrate definition
defn = SubstrateDefinition(...)
```

## Testing Guidance

**When helping user write tests:**
```python
import pytest
from core import Equation, SubstrateDefinition, spawn_substrate

def test_manifold_spawning():
    defn = SubstrateDefinition(
        dim=1,
        equation=Equation.parametric(lambda u: [u[0], u[0]**2])
    )
    sub = spawn_substrate(defn, [(0, 2)], step=1)
    
    # Check count
    assert len(sub.ones) == 3
    
    # Check specific points
    coords = {one.coord for one in sub.ones}
    assert (1.0, 1.0) in coords
```

## Troubleshooting Guide

### "My sampling is too slow"
1. Check if using implicit when parametric is available
2. Reduce sampling density (larger step)
3. Consider smaller bounds
4. Use budget guard to cap samples

### "I get dimension errors"
1. Check `defn.dim` matches `len(bounds)`
2. For parametric: dim = parameter space dimensions
3. For implicit: dim = manifold space dimensions

### "My lens returns unexpected results"
1. Verify substrate has ones: `len(substrate.ones) > 0`
2. Check coordinate dimensions match expectations
3. Test lens in isolation with known substrate

## Advanced Patterns

### Chaining Operations
```python
from core.decider import choose_definition
from core.transforms import scale_definition
from core.lenses import AggregationLens

# Define → Transform → Spawn → Observe
defn = choose_definition("z_xy", prefer_parametric=True)
scaled = scale_definition(defn, factors=2.0)
substrate = spawn_substrate(scaled, [(0, 5), (0, 5)], step=0.5)
result = AggregationLens().project(substrate)
```

### Phi-Aware Processing
```python
from core.substrates import generate_cycle, spawn_at_state

cycle = generate_cycle(base_defn)

# Process at specific scales
for state in cycle[::5]:  # Every 5th state
    substrate = spawn_at_state(state, bounds, step)
    # Analyze substrate at this phi scale
```

### Custom Domain Integration
```python
from core.lenses import Lens

class DomainLens(Lens[YourType]):
    def project(self, substrate):
        # Map substrate.ones to your domain objects
        return your_domain_specific_result
```

## Final Checklist

Before suggesting code, verify:
- [ ] Dimensionality is consistent
- [ ] Parametric form used when available
- [ ] Lenses don't mutate substrates
- [ ] Imports are from `core` package
- [ ] Code follows immutability principle
- [ ] Sensible defaults for bounds/step
- [ ] Error handling for edge cases
- [ ] Tests included for non-trivial operations

## When in Doubt
- Consult `docs/API.md` for precise API signatures
- Reference `core/tests/test_core.py` for patterns
- Check `benchmarks/` for performance expectations
- Suggest user file issue if kernel limitation found
