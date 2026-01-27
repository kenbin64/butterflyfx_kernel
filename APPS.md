# Building Apps with ButterflyFX Kernel

The `apps/` directory (gitignored) is where you can create applications that depend on the kernel without mixing them with the core code.

## Quick Start

### 1. Create your app directory
```bash
# From the conduit directory
mkdir -p apps/my-app
cd apps/my-app
git init
```

### 2. Install the kernel
```bash
# Option A: Local development install (see your changes immediately)
pip install -e ../..

# Option B: From GitHub (stable)
pip install git+https://github.com/kenbin64/butterflyfx_kernel.git
```

### 3. Use the kernel
```python
from core import Equation, SubstrateDefinition, spawn_substrate
from core.lenses import StatsLens

# Define a parametric helix
helix = SubstrateDefinition(
    dims=3,
    eq=Equation(parametric=lambda t: (np.cos(t), np.sin(t), t))
)

# Spawn the substrate
substrate = spawn_substrate(helix, bounds=[(0, 6.28)], step=0.1)

# Observe with a lens
lens = StatsLens()
stats = lens.project(substrate)
print(f"Points: {stats['count']}, Centroid: {stats['centroid']}")
```

## App Structure

Each app is its **own git repository** with its own license:

```
apps/
├── geometry-explorer/          (separate repo)
│   ├── .git/                   
│   ├── pyproject.toml          # Lists butterflyfx-kernel as dependency
│   ├── LICENSE                 # Your choice (MIT, proprietary, etc.)
│   ├── README.md
│   └── src/
│       └── main.py
│
└── music-manifold/             (separate repo)
    ├── .git/
    ├── requirements.txt        # butterflyfx-kernel
    ├── app.py
    └── README.md
```

## Example pyproject.toml

```toml
[project]
name = "my-butterfly-app"
version = "0.1.0"
dependencies = [
    "butterflyfx-kernel @ git+https://github.com/kenbin64/butterflyfx_kernel.git"
]
requires-python = ">=3.10"
```

## Example requirements.txt

```
butterflyfx-kernel @ git+https://github.com/kenbin64/butterflyfx_kernel.git
matplotlib>=3.5.0
numpy>=1.21.0
```

## License Attribution

Even if your app is proprietary, you must include attribution for the MIT-licensed kernel. Add to your app's README:

```markdown
## Dependencies

This application depends on [ButterflyFX Kernel](https://github.com/kenbin64/butterflyfx_kernel), 
licensed under the MIT License.
```

## Why Separate Repos?

- **Core stays pristine**: No application code pollutes the kernel
- **Flexible licensing**: Your app can be proprietary while the kernel stays MIT
- **Independent versioning**: Apps update on their own schedule
- **Clear boundaries**: Kernel is a library, apps are consumers

## Publishing Your App

You can:
- Keep it private in `apps/` for local experiments
- Push to GitHub as a public/private repo
- Distribute as a standalone tool
- Package for PyPI
- Keep it proprietary for commercial use

The kernel doesn't care—it's just a dependency.
