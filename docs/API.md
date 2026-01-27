# ButterflyFX Kernel - Developer API Reference

## Core Primitives

### Types
```python
from core import Scalar, Vec, Equation, SubstrateDefinition, Substrate, One

Scalar = float              # Real number
Vec = List[Scalar]          # Point in n-dimensional space
```

### Equations
Define manifolds using implicit or parametric forms:

```python
# Implicit: f(p) = 0
eq_implicit = Equation.implicit(lambda p: p[2] - p[0] * p[1])  # z = xy

# Parametric: p = g(u)
eq_parametric = Equation.parametric(lambda u: [u[0], u[1], u[0] * u[1]])
```

### Substrate Definitions
Pure mathematical descriptions of manifolds:

```python
defn = SubstrateDefinition(
    dim=2,                    # Dimensionality (parameter space for parametric)
    equation=eq_parametric    # Equation defining the manifold
)
```

### Spawning Substrates
Collapse a definition into observable points:

```python
from core import spawn_substrate

substrate = spawn_substrate(
    defn,
    bounds=[(0, 10), (0, 10)],  # Min/max per dimension
    step=1.0                     # Sampling increment
)

# Access observed points
for one in substrate.ones:
    print(one.coord)  # Tuple of coordinates
```

## Lenses (Observers)

Lenses project substrates into meaningful representations without mutation.

### Built-in Lenses
```python
from core.lenses import IdentityLens, StatsLens, AggregationLens

# Identity - returns raw ones unchanged
identity = IdentityLens()
ones = identity.project(substrate)

# Stats - count, centroid, bounds
stats = StatsLens()
result = stats.project(substrate)
# {'count': int, 'centroid': tuple, 'bounds': tuple}

# Aggregation - min/max/mean/variance per dimension
agg = AggregationLens()
result = agg.project(substrate)
# {'count': int, 'min': tuple, 'max': tuple, 'mean': tuple, 'var': tuple}
```

### Custom Lenses
```python
from core.lenses import Lens

class MyLens(Lens[dict]):
    def project(self, substrate):
        # Your observation logic
        return {"custom": "result"}
```

## Phi (φ) Recursion

### Dimensional States
```python
from core.substrates import generate_cycle, spawn_at_state, phi_scale, PHI

# Generate full cycle: 1 → φ → φ² → ... → φ³³ → 1
cycle = generate_cycle(base_definition)
print(len(cycle))  # 34 states

# Spawn at specific phi scale
state = cycle[4]  # Fifth state (φ^5)
substrate = spawn_at_state(state, bounds=[(0, 1)], step=0.1)
```

### Phi Lenses
```python
from core.phi_lens import PhiStepLens, PhiCycleLens

# Project at single step
step_lens = PhiStepLens(
    step_index=5,
    projector=StatsLens(),
    bounds=[(0, 1)],
    step=0.1
)
result = step_lens.project(definition)

# Project across full cycle
cycle_lens = PhiCycleLens(
    projector=AggregationLens(),
    bounds=[(0, 1)],
    step=0.1,
    include_collapse=True  # Include step 34
)
results = cycle_lens.project(definition)  # List of 34 results
```

## Sampling Utilities

```python
from core.sampling import grid_params, random_params, enforce_budget

# Grid sampling
params = grid_params(bounds=[(0, 1), (0, 1)], step=0.1)

# Random sampling
params = random_params(bounds=[(0, 1), (0, 1)], count=100)

# Budget enforcement (prevent runaway sampling)
limited = enforce_budget(items, max_count=1000)
```

## Transforms

```python
from core.transforms import translate_definition, scale_definition

# Translate manifold
shifted = translate_definition(defn, offsets=[5, 5])

# Scale manifold (uniform or per-dimension)
scaled = scale_definition(defn, factors=2.0)      # Uniform
scaled = scale_definition(defn, factors=[2, 3])   # Per-dimension
```

## Decision Helpers

```python
from core.decider import choose_definition, def_z_xy, def_z_x_over_y

# Choose form (parametric faster for sampling)
defn = choose_definition("z_xy", prefer_parametric=True)

# Explicit helpers
defn = def_z_xy(form="parametric")        # z = x*y
defn = def_z_x_over_y(form="implicit")    # z = x/y
```

## Human Interface Layer

```python
from core.hil import name_substrate, name_lens, humanize_state

# Name substrate
named = name_substrate("Saddle", "Hyperbolic paraboloid", defn)
print(named.name, named.description)

# Name lens
named_lens = name_lens("ColorMapper", "Maps coords to RGB", MyLens())

# Humanize phi states
human_state = humanize_state(dimensional_state)
print(human_state.label)  # "First Spark", "Expansion φ^5", etc.
```

## Best Practices

### Performance
- **Prefer parametric** for known manifolds (z=xy, spirals): O(n) where n = parameter samples
- **Use implicit** when constraints are clearer or you need membership testing: O(n^d) where d = dimensions
- **Cap sampling** with budget guard to prevent runaway grids
- **Use appropriate step size** - smaller steps = more points = slower

### Design
- **Keep lenses pure** - no side effects, no mutation
- **Compose lenses** - pass one lens as projector to another
- **Use HIL for UX** - wrap technical objects with human-readable names
- **Version-pin dependencies** - `butterflyfx-kernel==0.1.0` in production

### Testing
```python
import pytest
from core import Equation, SubstrateDefinition, spawn_substrate

def test_my_manifold():
    defn = SubstrateDefinition(dim=1, equation=Equation.parametric(lambda u: [u[0]]))
    sub = spawn_substrate(defn, [(0, 1)], 1)
    assert len(sub.ones) == 2
```

## Common Patterns

### Custom Domain Lens
```python
class MusicLens(Lens[dict]):
    def project(self, substrate):
        notes = []
        for one in substrate.ones:
            freq = 440 + one.coord[0] * 10  # Map to frequency
            notes.append(freq)
        return {"frequencies": tuple(notes)}
```

### Multi-stage Processing
```python
# Generate → Transform → Observe
defn = def_z_xy()
scaled = scale_definition(defn, factors=2)
substrate = spawn_substrate(scaled, [(0, 5), (0, 5)], step=1)
result = AggregationLens().project(substrate)
```

### Phi-aware Application
```python
cycle = generate_cycle(base_defn)
for state in cycle[:10]:  # First 10 steps
    sub = spawn_at_state(state, [(0, 1)], step=0.5)
    # Process substrate at this phi scale
```

## API Stability

- **Core primitives** (`Equation`, `SubstrateDefinition`, `spawn_substrate`, `Lens`) are stable
- **Helper modules** (decider, sampling, transforms, phi_lens) may expand but won't break existing APIs
- **Version updates** follow semantic versioning (major.minor.patch)

## Support

- GitHub Issues: https://github.com/kenbin64/butterflyfx_kernel/issues
- Tests: See `core/tests/test_core.py` for comprehensive examples
- Benchmarks: See `benchmarks/` for performance references
