"""
ButterflyFX Kernel - Basic Example

Demonstrates the fundamental concepts of dimensional computing:
- Creating a HelixKernel
- Invoking levels directly (no iteration)
- Spiraling up and down
- Working with the GenerativeManifold

Author: Kenneth Bingham <keneticsart@gmail.com>
License: CC BY 4.0
"""

from butterflyfx import HelixKernel, GenerativeManifold, ManifoldSubstrate


def main():
    print("=" * 60)
    print("ButterflyFX Kernel - Dimensional Computing Demo")
    print("=" * 60)
    
    # ===========================================
    # Part 1: The Helix Kernel
    # ===========================================
    print("\n--- Part 1: HelixKernel State Machine ---\n")
    
    kernel = HelixKernel()
    print(f"Initial state: spiral={kernel.spiral}, level={kernel.level}")
    
    # Invoke levels directly - no iteration!
    # Traditional: for i in range(4): advance()  # 4 steps
    # Helix: invoke(4)  # 1 step
    
    kernel.invoke(level=2)  # Jump to Length
    print(f"After invoke(2): spiral={kernel.spiral}, level={kernel.level} (Length)")
    
    kernel.invoke(level=4)  # Jump to Plane
    print(f"After invoke(4): spiral={kernel.spiral}, level={kernel.level} (Plane)")
    
    kernel.invoke(level=6)  # Jump to Whole
    print(f"After invoke(6): spiral={kernel.spiral}, level={kernel.level} (Whole)")
    
    # Spiral up: Whole becomes Potential of next spiral
    kernel.spiral_up()
    print(f"After spiral_up(): spiral={kernel.spiral}, level={kernel.level} (New Potential)")
    
    # ===========================================
    # Part 2: Level Meanings
    # ===========================================
    print("\n--- Part 2: The Seven Levels ---\n")
    
    levels = [
        (0, "Potential", "○", "Pure possibility, nothing instantiated"),
        (1, "Point", "•", "Single instantiation, moment of existence"),
        (2, "Length", "━", "Extension in one dimension"),
        (3, "Width", "▭", "Extension in two dimensions"),
        (4, "Plane", "▦", "Surface, 2D completeness"),
        (5, "Volume", "▣", "Full 3D existence"),
        (6, "Whole", "◉", "Complete entity, ready for next spiral"),
    ]
    
    for level, name, symbol, description in levels:
        print(f"  Level {level}: {symbol} {name:10} - {description}")
    
    # ===========================================
    # Part 3: The For Loop Fallacy
    # ===========================================
    print("\n--- Part 3: The For Loop Fallacy ---\n")
    
    # Traditional approach (DON'T DO THIS)
    print("Traditional iteration (O(N)):")
    print("  for i in range(1000000):")
    print("      process(data[i])  # 1,000,000 steps")
    
    # Helix approach (DO THIS)
    print("\nDimensional invocation (O(7)):")
    print("  kernel.invoke(level=6)  # 1 step - complete entity")
    
    print("\nWhy iterate through every point when you can JUMP to the level?")
    
    # ===========================================
    # Part 4: Manifold of Potential
    # ===========================================
    print("\n--- Part 4: Manifold of Potential ---\n")
    
    print("'All exists. Nothing manifests. Invoke only what you need.'")
    print()
    
    # Conceptual example
    print("Traditional database:")
    print("  SELECT * FROM cars")
    print("  JOIN parts ON cars.id = parts.car_id")
    print("  JOIN materials ON parts.id = materials.part_id")
    print("  -- Forces ALL tables to exist simultaneously")
    
    print("\nButterflyFX approach:")
    print("  car = manifold.get('car')  # Whole exists")
    print("  transmission = car.invoke('transmission')  # Only this manifests")
    print("  # Engine, wheels, body stay as potential")
    print("  # No resources wasted on uninvoked dimensions")
    
    # ===========================================
    # Part 5: Spiral Structure
    # ===========================================
    print("\n--- Part 5: Spiral Structure ---\n")
    
    print("Spiral -1: Subatomic realm")
    print("  ├── Level 0: Quantum potential")
    print("  ├── Level 1: Quark")
    print("  ├── Level 2: String")
    print("  ├── Level 3: Field")
    print("  ├── Level 4: Wave function")
    print("  ├── Level 5: Particle cloud")
    print("  └── Level 6: Atom (→ becomes Level 0 of Spiral 0)")
    print()
    print("Spiral 0: Material realm")
    print("  ├── Level 0: Atom (Potential)")
    print("  ├── Level 1: Element")
    print("  ├── Level 2: Molecule chain")
    print("  ├── Level 3: Compound")
    print("  ├── Level 4: Material surface")
    print("  ├── Level 5: Object")
    print("  └── Level 6: Thing (→ becomes Level 0 of Spiral 1)")
    
    print("\n" + "=" * 60)
    print("Learn more: https://butterflyfx.us")
    print("Author: Kenneth Bingham <keneticsart@gmail.com>")
    print("License: CC BY 4.0")
    print("=" * 60)


if __name__ == "__main__":
    main()
