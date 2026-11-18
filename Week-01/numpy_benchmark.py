"""BMB 961 Week 1: a small numpy benchmark for your first ICER job.

It prints where and how it ran, times a dense matrix product, and reports the speed in GFLOP/s
(billions of floating-point operations per second).

    python numpy_benchmark.py              # use the CPUs Slurm gave this job
    python numpy_benchmark.py --threads 1  # force a number of threads
"""
import argparse, os, socket, sys, time

def cpus_given():
    """Number of CPUs Slurm gave this job; falls back to all CPUs of the machine."""
    for var in ("SLURM_CPUS_PER_TASK", "SLURM_CPUS_ON_NODE"):
        if os.environ.get(var):
            return int(os.environ[var])
    return os.cpu_count() or 1

def cpu_model():
    """Name of the CPU this job landed on (ICER nodes differ a lot, so your numbers will differ from your neighbor's)."""
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    import platform
    return platform.processor() or platform.machine()

ap = argparse.ArgumentParser()
ap.add_argument("--threads", type=int, default=None, help="threads for the linear-algebra library")
args = ap.parse_args()
threads = args.threads or cpus_given()
for var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[var] = str(threads)          # must be set BEFORE numpy is imported
import numpy as np

print("=== where this ran ===")
print("job id      :", os.environ.get("SLURM_JOB_ID", "(not a Slurm job)"))
print("node        :", socket.gethostname())
print("cpu model   :", cpu_model())
print("threads     :", threads)
print("python      :", sys.executable)
print("numpy       :", np.__version__, "from", os.path.dirname(np.__file__))

# Matrix product C = A B for N x N matrices of 64-bit floats.
# Each of the N*N entries of C is a dot product of length N: N multiplies + N adds = 2N operations,
# so one product costs 2 N^3 floating-point operations.  Speed = operations / time.
print("\n=== matrix product benchmark ===")
rng = np.random.default_rng(0)
best_gflops = 0.0
for n in (500, 1000, 2000):
    a = rng.standard_normal((n, n)); b = rng.standard_normal((n, n))
    times = []
    for _ in range(3):
        t0 = time.perf_counter(); c = a @ b; times.append(time.perf_counter() - t0)
    t = min(times); gflops = 2 * n**3 / t / 1e9; best_gflops = max(best_gflops, gflops)
    # check: one entry of C against a plain dot product (they must agree to rounding error)
    assert abs(c[0, 0] - np.dot(a[0, :], b[:, 0])) < 1e-8, "matrix product check failed"
    print(f"N = {n:5d}: best of 3 = {t:7.3f} s -> {gflops:7.1f} GFLOP/s   (check passed)")
print(f"\nPROOF line (paste this into your notebook): job {os.environ.get('SLURM_JOB_ID', 'none')} "
      f"node {socket.gethostname()} cpu [{cpu_model()}] threads {threads} best {best_gflops:.1f} GFLOP/s")
