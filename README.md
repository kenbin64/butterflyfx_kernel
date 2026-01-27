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
- `core/fibonacci.py` — Fibonacci helpers compatible with substrates
- `core/tests/` — test suite

## License
Proprietary (specify if different).
