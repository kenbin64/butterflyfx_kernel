import time
from core.substrates import Equation, SubstrateDefinition, spawn_substrate

def bench(name, fn):
    t = time.perf_counter()
    res = fn()
    return name, time.perf_counter() - t, res

# implicit z - x*y = 0 over 0..10
implicit_def = SubstrateDefinition(dim=3, equation=Equation.implicit(lambda p: p[2] - p[0] * p[1]))
name_i, dur_i, sub_i = bench("implicit_z_eq_xy", lambda: spawn_substrate(implicit_def, bounds=[(0, 10), (0, 10), (-100, 100)], step=1))

# parametric p=[x,y,x*y] over same x,y grid
param_def = SubstrateDefinition(dim=2, equation=Equation.parametric(lambda u: [u[0], u[1], u[0] * u[1]]))
name_p, dur_p, sub_p = bench("parametric_z_eq_xy", lambda: spawn_substrate(param_def, bounds=[(0, 10), (0, 10)], step=1))

print(f"{name_i}: {dur_i:.4f}s, ones={len(sub_i.ones)}")
print(f"{name_p}: {dur_p:.4f}s, ones={len(sub_p.ones)}")
