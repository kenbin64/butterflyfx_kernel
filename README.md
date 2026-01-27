# ButterflyFX Kernel

Generative substrate-of-substrates kernel with φ-recursion, human interface wrappers, and observer lenses. Pure equation-driven manifolds—no hard-coded shapes.

## Features
- Implicit and parametric manifold definitions with sampling-based `spawn_substrate`
- φ-recursion engine (`DimensionalState`, `generate_cycle`, `spawn_at_state`)
- Lenses including identity and stats observers
- Human Interface Layer (HIL) for naming substrates, lenses, and dimensional states
- Fibonacci utilities adapted to substrates
- Comprehensive tests in `core/tests/test_core.py`

## Quick start
```bash
# activate the env (example)
C:/projects/butterfly/conduit/.venv/Scripts/Activate.ps1

# run tests
C:/projects/butterfly/conduit/.venv/Scripts/python.exe -m pytest
```

## Repository structure
- `core/substrates.py` — generative kernel + φ recursion
- `core/lenses.py` — observer interfaces and simple projections
- `core/hil.py` — human-friendly naming wrappers
- `core/decider.py` — decision helpers for common manifolds (z=xy, z=x/y, z=xy^2, m=xyz)
- `core/fibonacci.py` — Fibonacci helpers compatible with substrates
- `core/tests/` — test suite

## Tests performed
- `python -m pytest`
	- Implicit/parametric substrate spawning
	- φ-cycle generation and scaled spawning
	- Lens projections (identity, stats)
	- Human Interface Layer wrappers
	- Domain-specific lenses (color, wind velocity, DAL stocks, music, TSP with O(n^2) heuristic)
	- Fibonacci utilities
	- Decision helpers and decision-tree substrate

## Recent actions
- Added Human Interface Layer wrappers (`core/hil.py`).
- Implemented domain-specific lens examples and tests (color, wind, stocks, music, TSP).
- Updated README and .gitignore.
- Added benchmarks (`benchmarks/bench.py`) and recorded results in `BENCHMARK.md`.
- Added decision helpers (`core/decider.py`) and tests.

## Contribution guide (source of truth)
- Treat the kernel primitives in `core/substrates.py` as the contract: equations are implicit or parametric; sampling is via `spawn_substrate`; lenses are observers that do not mutate substrates.
- Prefer parametric forms when performance matters; use implicit when natural or when constraints are clearer in f(p)=0 form.
- Add lenses as projections only; keep domain meaning outside the core kernel.
- Keep tests authoritative: new functionality should extend `core/tests/test_core.py` (or new test modules) to lock behavior.
- Benchmarks are informational; align new performance experiments with `benchmarks/` scripts.

## License
Proprietary (specify if different).
