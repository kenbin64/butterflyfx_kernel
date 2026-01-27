# ButterflyFX Basics

**A simple tool for working with mathematical shapes and patterns**

## What is ButterflyFX?

ButterflyFX helps you create and explore mathematical shapes—like curves, surfaces, and patterns—using simple equations. Think of it as a way to describe shapes with math, then sample points from those shapes to visualize or analyze them.

## Why would I use it?

- **Design tools**: Generate interesting curves and surfaces for graphics or 3D modeling
- **Data visualization**: Map data to geometric shapes for better understanding
- **Education**: Explore mathematical concepts hands-on
- **Creative coding**: Build generative art or music from mathematical patterns

## Basic Concepts

### 1. Shapes (called "Substrates")

A substrate is just a mathematical shape. You describe it with an equation, and ButterflyFX samples points from it.

**Example: A simple parabola**
```python
from core import Equation, SubstrateDefinition, spawn_substrate

# Describe the shape: y = x²
parabola = SubstrateDefinition(
    dim=1,
    equation=Equation.parametric(lambda u: [u[0], u[0]**2])
)

# Sample points from it
points = spawn_substrate(parabola, bounds=[(0, 10)], step=1)
print(f"Got {len(points.ones)} points")
```

### 2. Observations (called "Lenses")

A lens looks at your shape and tells you something useful about it—like how big it is, where the center is, or what the highest and lowest points are.

**Example: Getting shape statistics**
```python
from core.lenses import StatsLens

stats = StatsLens()
info = stats.project(points)

print(f"This shape has {info['count']} points")
print(f"The center is at {info['centroid']}")
```

### 3. That's It!

You describe shapes, sample them, and observe them. Everything else builds on these ideas.

## Common Uses

### Generate a Spiral
```python
import math
from core import Equation, SubstrateDefinition, spawn_substrate

spiral = SubstrateDefinition(
    dim=1,
    equation=Equation.parametric(
        lambda u: [u[0] * math.cos(u[0]), u[0] * math.sin(u[0])]
    )
)

points = spawn_substrate(spiral, bounds=[(0, 10)], step=0.1)
# Now you have points tracing a spiral!
```

### Move or Scale a Shape
```python
from core.transforms import translate_definition, scale_definition

# Move the shape 5 units to the right
moved = translate_definition(spiral, offsets=[5, 0])

# Make it twice as big
bigger = scale_definition(moved, factors=2.0)
```

### Analyze Multiple Shapes
```python
from core.lenses import AggregationLens

lens = AggregationLens()
analysis = lens.project(points)

print(f"Min values: {analysis['min']}")
print(f"Max values: {analysis['max']}")
print(f"Average: {analysis['mean']}")
```

## Two Ways to Describe Shapes

### Parametric (Most Common)
"Start with a simple input and generate output coordinates"

Good for: spirals, curves, known shapes
```python
# Circle: given angle t, compute x and y
circle = Equation.parametric(lambda u: [math.cos(u[0]), math.sin(u[0])])
```

### Implicit
"Points that satisfy an equation"

Good for: constraints, regions, membership tests
```python
# Circle: all points where x² + y² = 1
circle = Equation.implicit(lambda p: p[0]**2 + p[1]**2 - 1)
```

## Getting Started

### Install
```bash
pip install git+https://github.com/kenbin64/butterflyfx_kernel.git
```

### Your First Shape
```python
from core import Equation, SubstrateDefinition, spawn_substrate

# Line from 0 to 10
line = SubstrateDefinition(
    dim=1,
    equation=Equation.parametric(lambda u: [u[0]])
)

points = spawn_substrate(line, bounds=[(0, 10)], step=1)

for point in points.ones:
    print(f"Point at: {point.coord}")
```

## Tips for Beginners

1. **Start simple**: Begin with lines and parabolas before complex 3D shapes
2. **Use parametric first**: It's usually faster and more intuitive
3. **Small steps = more points**: Smaller step values give you more detail (but slower)
4. **Use lenses**: They save you from writing analysis code yourself

## What can I build?

- **Visualization apps**: Plot curves and surfaces
- **Generative art**: Create patterns from equations
- **Data mapping**: Turn data into geometric patterns
- **Educational tools**: Interactive math exploration
- **Design utilities**: Generate shapes for CAD or graphics

## Common Shapes to Try

### Parabola
```python
parabola = Equation.parametric(lambda u: [u[0], u[0]**2])
```

### Sine Wave
```python
wave = Equation.parametric(lambda u: [u[0], math.sin(u[0])])
```

### Helix (3D Spiral)
```python
helix = Equation.parametric(
    lambda u: [math.cos(u[0]), math.sin(u[0]), u[0]]
)
```

### Surface (z = xy)
```python
surface = Equation.parametric(lambda u: [u[0], u[1], u[0] * u[1]])
```

## Need Help?

- Check out the examples in `core/tests/` for working code
- Read the full [Developer API](API.md) for all features
- File issues at: https://github.com/kenbin64/butterflyfx_kernel/issues

## What's Next?

Once you're comfortable with basics:
- Explore the **phi recursion** features for growth patterns
- Create **custom lenses** for your specific domain
- Try the **decision helpers** to automatically pick the best form
- Use **sampling utilities** for advanced control

ButterflyFX is simple on the surface but grows with your needs. Start small, experiment, and have fun creating!
