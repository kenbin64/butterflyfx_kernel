# Benchmark results

Command:
```
$env:PYTHONPATH="C:/projects/butterfly/conduit"; C:/projects/butterfly/conduit/.venv/Scripts/python.exe benchmarks/bench.py
```

Date: 2026-01-27

Average seconds per run (PowerShell, Windows):
- implicit_plane_2d: 0.0029s over 3 runs
- parametric_helix_3d: 0.0008s over 3 runs
- stats_lens_helix: 0.0002s over 10 runs
- implicit_sphere_3d: 0.0041s over 2 runs

Notes:
- Benchmarks sample implicit/parametric spawning and a stats lens projection.
- PYTHONPATH set to project root to import local packages.
- Additional comparison (z = x*y): implicit vs parametric sampling over x,y∈[0,10], step=1
	- implicit_z_eq_xy: ~0.0080s, 121 ones
	- parametric_z_eq_xy: ~0.0001s, 121 ones (avoids 3D grid membership test)
