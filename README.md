# ButterflyFX Kernel

**MIT Licensed Open Source**

Generative substrate-of-substrates kernel with φ-recursion, human interface wrappers, and observer lenses. Pure equation-driven manifolds—no hard-coded shapes.

## Features
- Implicit and parametric manifold definitions with sampling-based `spawn_substrate`
- φ-recursion engine (`DimensionalState`, `generate_cycle`, `spawn_at_state`)
- Lenses including identity and stats observers
- Human Interface Layer (HIL) for naming substrates, lenses, and dimensional states
- Fibonacci utilities adapted to substrates
- Comprehensive tests in `core/tests/test_core.py`

## Installation

### From source (for development)
```bash
git clone https://github.com/kenbin64/butterflyfx_kernel.git
cd butterflyfx_kernel
pip install -e .
```

### As a dependency in your app
```bash
# Once published to PyPI:
pip install butterflyfx-kernel

# Or from git:
pip install git+https://github.com/kenbin64/butterflyfx_kernel.git
```

## Documentation

- **[Basics Guide](docs/BASICS.md)** - Friendly introduction for everyone
- **[Developer API](docs/API.md)** - Complete technical reference
- **[AI Directive](docs/AI_DIRECTIVE.md)** - Guidance for AI assistants

## Quick start

### Using the package
```python
from core import Equation, SubstrateDefinition, spawn_substrate
from core.lenses import StatsLens

# Define a parametric manifold
defn = SubstrateDefinition(
    dim=2,
    equation=Equation.parametric(lambda u: [u[0], u[1], u[0] * u[1]])
)

# Spawn and observe
substrate = spawn_substrate(defn, bounds=[(0, 10), (0, 10)], step=1)
stats = StatsLens().project(substrate)
print(f"Sampled {stats['count']} points")
```

### Development
```bash
# Run tests
pytest

# Or with the full path (without package install):
python -m pytest
```

## Repository structure
- `core/substrates.py` — generative kernel + φ recursion
- `core/lenses.py` — observer interfaces and simple projections
- `core/hil.py` — human-friendly naming wrappers
- `core/decider.py` — decision helpers for common manifolds (z=xy, z=x/y, z=xy^2, m=xyz)
- `core/sampling.py` — grid/random sampling helpers and budget guard
- `core/transforms.py` — affine translate/scale wrappers for definitions
- `core/phi_lens.py` — optional phi-cycle lenses (per-step and full cycle)
- `core/fibonacci.py` — Fibonacci helpers compatible with substrates
- `core/tests/` — test suite

## Tests performed
- `python -m pytest`
	- Implicit/parametric substrate spawning
	- φ-cycle generation and scaled spawning
	- Lens projections (identity, stats)
	- Aggregation lens (min/max/mean/var)
	- Human Interface Layer wrappers
	- Domain-specific lenses (color, wind velocity, DAL stocks, music, TSP with O(n^2) heuristic)
	- Fibonacci utilities
	- Decision helpers and decision-tree substrate
	- Sampling helpers, budget guard, affine transforms
	- Phi step/cycle lenses

## Recent actions
- Added Human Interface Layer wrappers (`core/hil.py`).
- Implemented domain-specific lens examples and tests (color, wind, stocks, music, TSP).
- Updated README and .gitignore.
- Added benchmarks (`benchmarks/bench.py`) and recorded results in `BENCHMARK.md`.
- Added decision helpers (`core/decider.py`) and tests.
- Added sampling helpers, affine transforms, and aggregation lens.
- Added phi-cycle lenses.

## Contribution guide (source of truth)
- Treat the kernel primitives in `core/substrates.py` as the contract: equations are implicit or parametric; sampling is via `spawn_substrate`; lenses are observers that do not mutate substrates.
- Prefer parametric forms when performance matters; use implicit when natural or when constraints are clearer in f(p)=0 form.
- Add lenses as projections only; keep domain meaning outside the core kernel.
- Keep tests authoritative: new functionality should extend `core/tests/test_core.py` (or new test modules) to lock behavior.
- Benchmarks are informational; align new performance experiments with `benchmarks/` scripts.

## License & Governance

### License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

The ButterflyFX Kernel is pure mathematical abstraction and remains **free and open source**. Applications built on top of the kernel may use any license, but must retain the MIT license attribution for the core components.

### Governance
- The kernel is designed to be **free from single-entity control**.
- Multi-maintainer governance with branch protections and code review requirements.
- Contributions are welcome via pull requests with tests and documentation.
- See [NOTICE](NOTICE) for attribution and stewardship details.

### Using in Proprietary Applications
You may use this MIT-licensed kernel in proprietary applications without restriction. Simply:
1. Include the MIT license text and copyright notice from this project.
2. Install the kernel as a dependency rather than copying source code.
3. Your application code can remain closed-source and under any license you choose.

