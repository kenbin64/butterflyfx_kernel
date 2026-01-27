import math
import time
from core.substrates import Equation, SubstrateDefinition, spawn_substrate
from core.lenses import StatsLens


def bench(name, fn, repeats=5):
    start = time.perf_counter()
    for _ in range(repeats):
        fn()
    dur = time.perf_counter() - start
    return name, dur / repeats, repeats


def run():
    results = []

    implicit_def = SubstrateDefinition(dim=2, equation=Equation.implicit(lambda p: p[0] + p[1] - 1))
    results.append(bench("implicit_plane_2d", lambda: spawn_substrate(implicit_def, bounds=[(0, 1), (0, 1)], step=0.01), repeats=3))

    helix_def = SubstrateDefinition(dim=1, equation=Equation.parametric(lambda u: [math.cos(u[0]), math.sin(u[0]), u[0] / math.pi]))
    results.append(bench("parametric_helix_3d", lambda: spawn_substrate(helix_def, bounds=[(0, 20 * math.pi)], step=0.05), repeats=3))

    helix_sub = spawn_substrate(helix_def, bounds=[(0, 10 * math.pi)], step=0.05)
    results.append(bench("stats_lens_helix", lambda: StatsLens().project(helix_sub), repeats=10))

    sphere_def = SubstrateDefinition(dim=3, equation=Equation.implicit(lambda p: p[0] ** 2 + p[1] ** 2 + p[2] ** 2 - 1))
    results.append(bench("implicit_sphere_3d", lambda: spawn_substrate(sphere_def, bounds=[(-1, 1), (-1, 1), (-1, 1)], step=0.1), repeats=2))

    print("Benchmark results (avg seconds per run):")
    for name, avg, reps in results:
        print(f"{name}: {avg:.4f}s over {reps} runs")


if __name__ == "__main__":
    run()
