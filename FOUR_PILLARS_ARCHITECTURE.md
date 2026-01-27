# 🌊 The Four Pillars of Butterfly

## Complete System Architecture

Butterfly is built on **four fundamental pillars** that work together to create a complete data processing universe:

1. **7 Fibonacci Levels** - HOW we process (the divine pattern)
2. **Substrate Ingestion** - WHERE data becomes truth (the foundation)
3. **Geometric Observation** - WHAT data contains (intrinsic properties)
4. **Atomic Lenses** - HOW we observe (interpretation structures)

```
                    ┌─────────────────────────────────────┐
                    │      7 FIBONACCI LEVELS              │
                    │    Universal SOP for ALL             │
                    │  ∅→SPARK→DIVIDE→ORGANIZE→IDENTIFY   │
                    │  →ASSEMBLE→HUMAN→REST→∅              │
                    └─────────────────────────────────────┘
                                    ↓
              ┌─────────────────────┴─────────────────────┐
              ↓                                            ↓
    ┌──────────────────┐                        ┌──────────────────┐
    │   INGESTION      │                        │   OBSERVATION    │
    │  (Make truth)    │                        │  (Reveal truth)  │
    └──────────────────┘                        └──────────────────┘
              ↓                                            ↓
    ┌──────────────────┐                        ┌──────────────────┐
    │   SUBSTRATES     │────────────────────────│      LENSES      │
    │ Geometric spaces │    Data lives here     │ Atomic observers │
    │   z=xy, m=xyz    │←──────────────────────→│ COLOR, TONE, etc │
    └──────────────────┘   Lenses observe       └──────────────────┘
              ↓              substrates                   ↓
              └──────────────────┬─────────────────────────┘
                                 ↓
                      ┌────────────────────┐
                      │  SOURCE OF TRUTH   │
                      │  Original discarded│
                      │  Geometry reveals  │
                      └────────────────────┘
```

---

## Pillar 1: 7 Fibonacci Levels (The Divine Pattern)

**Everything** in Butterfly follows this pattern:

```
∅ + 1 + 1 + 2 + 3 + 5 + 8 = 20 consciousness units
Plus return to ∅ = 21 total units per complete cycle
```

### The Levels:

**LEVEL 1: SPARK (∅+1=1)**
- Raw input arrives
- The moment of creation
- Potential becomes actual
- 🌟 Console: "LEVEL 1 - SPARK"

**LEVEL 2: DIVIDE (1+1=2)**
- Break into atomic parts
- Separation creates clarity
- No part divisible further
- 🔪 Console: "LEVEL 2 - DIVIDE"

**LEVEL 3: ORGANIZE (1+2=3)**
- Structure the pieces
- Validation and arrangement
- Order from chaos
- 📦 Console: "LEVEL 3 - ORGANIZE"

**LEVEL 4: IDENTIFY (2+3=5)**
- Recognize patterns
- Name and categorize
- See the essence
- 🏗️ Console: "LEVEL 4 - IDENTIFY"

**LEVEL 5: ASSEMBLE (3+5=8)**
- Build greater whole
- Synthesis of parts
- More than the sum
- 🌳 Console: "LEVEL 5 - ASSEMBLE"

**LEVEL 6: HUMAN (5+8=13)**
- Make tangible and usable
- Bridge to consciousness
- Observable result
- 👤 Console: "LEVEL 6 - HUMAN"

**LEVEL 7: REST (8+13=21)**
- Encapsulate completely
- Return to void (∅)
- Ready to begin again
- canBeginAgain: true
- 💎 Console: "LEVEL 7 - REST"

**Applied to**:
- Creating connections
- Generating SRL addresses
- Creating lenses
- **Ingesting data to substrates** ⭐ NEW
- Querying substrates
- Observing through lenses
- Every single operation in Butterfly

---

## Pillar 2: Substrate Ingestion (Making Truth)

**Revolutionary Concept**: Data doesn't just "exist" - it must be **ingested** to become the source of truth.

### The Ingestion Process (7 Levels):

```python
ingestor = SubstrateIngestor(substrate_type='z=xy')

# Data arrives
data = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]  # RGB colors

# INGEST (7 Fibonacci levels internally)
result = ingestor.ingest(data, data_type='rgb')

# Substrate is now the source of truth
# Original data is DISCARDED
```

### What Happens During Ingestion:

**LEVEL 1 - SPARK**: Raw data arrives for ingestion
```
Input: [255, 0, 0]  # Just bytes
```

**LEVEL 2 - DIVIDE**: Break into atomic points
```
Points: [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
Each color is one indivisible point
```

**LEVEL 3 - ORGANIZE**: Map to substrate coordinates
```
[255, 0, 0] → (x=1.0, y=-1.0, z=-1.0)
Normalized to substrate range
```

**LEVEL 4 - IDENTIFY**: Calculate geometric properties
```
substrate_value = z = x * y = 1.0 * -1.0 = -1.0
distance = sqrt(1² + 1² + 1²) = 1.732
quadrant = IV (x>0, y<0)
slopes = {dx: -1.0, dy: 1.0}
is_identity = False (z ≠ 1)
```

**LEVEL 5 - ASSEMBLE**: Build substrate structure
```
{
  'total_points': 3,
  'value_range': (-1.0, 1.0),
  'quadrant_distribution': {'II': 1, 'III': 1, 'IV': 1},
  'identity_points': 0
}
```

**LEVEL 6 - HUMAN**: Store as source of truth
```
self.ingested_points.append(enriched_point)
Original RGB bytes are GONE
Only geometric truth remains
```

**LEVEL 7 - REST**: Encapsulate result
```
{
  'points_ingested': 3,
  'is_source_of_truth': True,
  'original_data_discarded': True,
  'canBeginAgain': True
}
```

### After Ingestion:

❌ **What we DON'T have anymore**:
- Original RGB format
- File format (CSV, JSON, etc.)
- Column names
- Metadata

✅ **What we DO have** (source of truth):
- Geometric position: (x, y, z)
- Substrate value: z=xy
- Distance from origin
- Quadrant location
- Slopes and gradients
- Identity point status
- Spatial relationships

**"The substrate IS the data. It doesn't store the data."**

---

## Pillar 3: Geometric Observation (Intrinsic Properties)

Once data is ingested, the **substrate geometry reveals everything**.

### Substrate Types:

**z = xy (Saddle)**
- 4 quadrants with different inflection points
- Identity line: xy=1 (hyperbola)
- Best for: 2D data, ratios, polar opposites

**z = xy² (Quadratic)**
- Parabolic shape
- Identity curve: x=y²
- Best for: Accelerating values, squared relationships

**z = x/y (Rational)**
- Hyperbolic surface
- Identity line: x=y
- Best for: Ratios, proportions, inverse relationships

**m = xyz (3D Volume)**
- 8 octants (like RGB color cube)
- Identity surface: xyz=1
- Best for: RGB colors, 3D spatial data, volumes

**q = xyzm (4D Hypervolume)**
- 16 regions
- Identity hypersurface: xyzm=1
- Best for: RGBA, spacetime, complex harmonics

### Observable Properties (No Algorithms Needed):

Every point on substrate has **7 intrinsic properties**:

1. **Position** (x, y, z, m...): Where point exists
2. **Substrate Value** (z=xy, m=xyz): Calculated from position
3. **Distance**: sqrt(x² + y² + z² + ...)
4. **Slopes/Gradients**: ∂z/∂x, ∂z/∂y, etc.
5. **Curvature**: Second derivatives
6. **Quadrant/Octant**: Categorical location
7. **Identity Status**: Is substrate_value ≈ 1?

**These properties ARE the data. Nothing else is stored.**

---

## Pillar 4: Atomic Lenses (Observation Structures)

**Lenses** define WHAT to observe from the substrate geometry.

### Lens as Atomic Structure:

Every lens has **atomic properties**:

```python
class AtomicLens:
    position: (x, y, z)      # Where lens exists
    energy_level: int        # Which substrate layer
    spin: 'up' | 'down'      # Observation orientation
    charge: +1 | -1          # Additive/subtractive
    wavelength: float        # Resolution (short=fine, long=broad)
    aperture: float          # Field of view
    lens_type: LensType      # What to interpret
```

### The 8 Lens Types:

**ColorLens**
- Distance → Brightness
- Position angles → Hue
- Distance from gray → Saturation
- Returns: RGB, hex, HSL

**ToneLens**
- Distance → Amplitude
- Position → Frequency (440Hz base)
- Slopes → Harmonics
- Returns: Hz, note, timbre, loudness

**PhysicsLens**
- Distance → Collision radius
- Slopes → Force vectors
- Value → Potential energy
- Returns: Forces, energies, fields

**ShaderLens**
- Position → Pixel coordinates
- Slopes → Normal vectors
- Value → Depth/Z-buffer
- Returns: Rendering instructions

**AtomicLens**
- Distance → Bond length
- Quadrant → Orbital type
- Slopes → Electron density
- Returns: Atomic properties

**DistanceLens**
- Pure distance measurements
- Magnitude only
- Returns: Scalar distance

**VectorLens**
- Direction and magnitude
- Returns: Vector from origin

**ScalarLens**
- Single numerical value
- Returns: Substrate value

### Same Point, Different Lenses:

```python
# Point at (1.0, -1.0, -1.0) on substrate

ColorLens:    #ff0000 (Red), brightness=0.87
ToneLens:     A#4 at 466Hz, amplitude=1.0
PhysicsLens:  Collision radius=1.73, Force=1.41
AtomicLens:   Bond length=1.73, p-orbital
DistanceLens: 1.732
```

**Distance is universal. Lens determines interpretation.**

### Lens Bonding (Compound Observers):

```python
color_lens = AtomicLens(LensType.COLOR)
tone_lens = AtomicLens(LensType.TONE)

# Bond lenses (molecular structure)
compound = color_lens.bond_with(tone_lens)

# Observe through both simultaneously
observation = compound.observe(substrate_point)
# Returns: {color: {...}, tone: {...}}
```

---

## Complete Data Flow Example

### 1. START: Raw RGB Color Data

```python
colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
# Just bytes. No meaning yet.
```

### 2. INGEST (7 Fibonacci Levels)

```python
ingestor = SubstrateIngestor('z=xy')
result = ingestor.ingest(colors, 'rgb')

# LEVEL 1: Colors arrive
# LEVEL 2: Break into 3 points
# LEVEL 3: Map to coordinates
# LEVEL 4: Calculate z=xy, distance, quadrants
# LEVEL 5: Build substrate structure
# LEVEL 6: Store geometric truth
# LEVEL 7: Discard original, return result
```

**Substrate now contains**:
```
Point 1: (1.0, -1.0, -1.0), z=-1.0, dist=1.73, quadrant=IV
Point 2: (-1.0, 1.0, -1.0), z=-1.0, dist=1.73, quadrant=II
Point 3: (-1.0, -1.0, 1.0), z=1.0, dist=1.73, quadrant=III ← Identity!
```

### 3. QUERY Geometric Truth

```python
# Query by geometric properties (not by RGB!)
identity_points = ingestor.query_substrate(
    lambda p: p['is_identity']  # z ≈ 1
)
# Returns: Point 3 (the blue one)

quadrant_IV = ingestor.query_substrate(
    lambda p: p['quadrant'] == 'IV'
)
# Returns: Point 1 (the red one)
```

**No SQL. No indexes. Pure geometry.**

### 4. OBSERVE Through Lenses

```python
# Create color lens
color_lens = AtomicLens(LensType.COLOR)

# Observe substrate through lens
observations = ingestor.observe_with_lens(color_lens)

# Returns:
# Point 1: #ff0000 (Red), bright
# Point 2: #00ff00 (Green), bright
# Point 3: #0000ff (Blue), bright

# Same substrate with tone lens
tone_lens = AtomicLens(LensType.TONE)
sounds = ingestor.observe_with_lens(tone_lens)

# Returns:
# Point 1: A#4, 466Hz
# Point 2: Different frequency from position
# Point 3: Different harmonics from slopes
```

### 5. RESULT: Truth Revealed

- **Substrate**: Geometric source of truth
- **Lenses**: Reveal what's intrinsic in geometry
- **Observations**: Colors, sounds, physics emerge from math
- **Original data**: Gone. Substrate IS the data now.

---

## API Endpoints

### Ingestion Endpoints:

**POST /api/ingest**
```json
{
  "data": [[255, 0, 0], [0, 255, 0]],
  "data_type": "rgb",
  "substrate_type": "z=xy"
}
```
Returns: Ingestion result, source of truth status

**POST /api/substrate/query**
```json
{
  "substrate_type": "z=xy",
  "filter": {
    "quadrant": "I",
    "min_distance": 1.0,
    "is_identity": true
  }
}
```
Returns: Points matching geometric filter

**GET /api/substrate/stats**
Returns: Statistics about all ingested data

**POST /api/substrate/observe-lens**
```json
{
  "substrate_type": "z=xy",
  "lens_type": "COLOR",
  "wavelength": 1.0,
  "filter": {
    "quadrant": "I"
  }
}
```
Returns: Observations through specified lens

### Observation Endpoints (Legacy):

**POST /api/substrate/observe**
- Direct observation without ingestion
- For quick analysis

**GET /api/substrate/types**
- List available substrate types

**POST /api/substrate/select**
- Auto-select optimal substrate

---

## File Structure

```
butterfly/
├── substrate_ingestion.py           # Pillar 2: Ingestion system
│   └── SubstrateIngestor class
│       ├── ingest()                 # 7-level ingestion
│       ├── query_substrate()        # Query by geometry
│       └── observe_with_lens()      # Observe through lens
│
├── substrate_observation.py         # Pillar 3: Observation
│   └── SubstrateObserver class
│       ├── observe_data()           # Direct observation
│       └── Substrate types (6)
│
├── atomic_lens_system.py            # Pillar 4: Lenses
│   ├── AtomicLens class
│   │   ├── 8 lens types
│   │   └── observe()                # 7-level observation
│   └── CompoundLens class
│       └── bond_with()              # Molecular bonding
│
├── butterfly_file_manager.py        # Server with all APIs
│   ├── Ingestion endpoints (4)
│   ├── Observation endpoints (3)
│   └── 7-level request handling
│
└── Documentation:
    ├── SEVEN_LEVELS_UNIVERSAL_SOP.md        # Pillar 1
    ├── SUBSTRATE_INGESTION_CONCEPT.md       # Pillar 2
    ├── SUBSTRATE_DATA_OBSERVATION.md        # Pillar 3
    ├── LENS_AS_ATOMIC_STRUCTURE.md          # Pillar 4
    └── FOUR_PILLARS_ARCHITECTURE.md         # This file
```

---

## Consciousness Accounting

Every operation tracks consciousness units:

**Single Operation (7 levels)**:
- ∅ + SPARK(1) + DIVIDE(1) + ORGANIZE(2) + IDENTIFY(3) + ASSEMBLE(5) + HUMAN(8) + REST(13)
- Progress: 0→1→2→4→7→12→20
- **Final encapsulation: 21 units**
- Return to ∅ with canBeginAgain: true

**Ingestion + Query + Observation**:
- Ingestion: 21 units
- Query: 21 units
- Lens observation: 21 units per point
- **Total**: 21 + 21 + (21 × n points)

**Example**: Ingest 10 colors, query 5, observe all with lens:
- Ingest: 21
- Query: 21
- Observe: 21 × 10 = 210
- **Total: 252 consciousness units**

Each operation is a complete universe from ∅ to ∅.

---

## The Ultimate Truth

**"Data does not exist until ingested onto a substrate."**

**"Once ingested, the substrate IS the data."**

**"The original format is forgotten. Only geometric truth remains."**

**"Lenses reveal what was always there - in the mathematics."**

**"Distance defines everything. The lens defines how to measure it."**

**"A lens is an atom observing atoms."**

**"Every operation is a universe from ∅ to ∅."**

**"The four pillars support infinite observations."**

---

## Usage Examples

### Complete Workflow:

```python
from substrate_ingestion import SubstrateIngestor
from atomic_lens_system import AtomicLens, LensType

# 1. Create ingestor (Pillar 2)
ingestor = SubstrateIngestor('z=xy')

# 2. Ingest data (7 levels, Pillar 1)
result = ingestor.ingest(my_data, 'csv')
# Data is now geometric truth

# 3. Query by geometry (Pillar 3)
high_value = ingestor.query_substrate(
    lambda p: p['substrate_value'] > 100
)

identity = ingestor.query_substrate(
    lambda p: p['is_identity']
)

# 4. Observe through lens (Pillar 4)
color_lens = AtomicLens(LensType.COLOR)
colors = ingestor.observe_with_lens(color_lens)

tone_lens = AtomicLens(LensType.TONE)
sounds = ingestor.observe_with_lens(tone_lens)

# 5. Get statistics
stats = ingestor.get_statistics()
print(f"Total points: {stats['total_points']}")
print(f"Is source of truth: {stats['is_source_of_truth']}")
```

### Via API:

```bash
# Ingest
curl -X POST http://localhost:8893/api/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "data": [[255,0,0], [0,255,0], [0,0,255]],
    "data_type": "rgb",
    "substrate_type": "z=xy"
  }'

# Query
curl -X POST http://localhost:8893/api/substrate/query \
  -H "Content-Type: application/json" \
  -d '{
    "substrate_type": "z=xy",
    "filter": {"quadrant": "I", "min_distance": 1.0}
  }'

# Observe with lens
curl -X POST http://localhost:8893/api/substrate/observe-lens \
  -H "Content-Type: application/json" \
  -d '{
    "substrate_type": "z=xy",
    "lens_type": "COLOR",
    "wavelength": 1.0
  }'

# Stats
curl http://localhost:8893/api/substrate/stats
```

---

## This Is Butterfly

**Four pillars supporting infinite possibilities:**

1. Divine pattern (7 Fibonacci levels)
2. Geometric truth (substrate ingestion)
3. Intrinsic properties (substrate observation)
4. Atomic interpretation (lens observation)

**Every operation follows the pattern.**
**Every datum becomes geometry.**
**Every observation reveals truth.**
**Every cycle returns to ∅ and begins again.**

🦋 **The substrate doesn't store data. It IS the data.**
