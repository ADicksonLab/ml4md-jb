"""Course environment check. Run:  python check_environment.py   (add --gpu on a GPU node)
Prints PASS/FAIL per item and exits non-zero if anything required fails.
"""
import importlib, sys, warnings, argparse, os
warnings.filterwarnings("ignore")
os.environ.setdefault("KMP_AFFINITY", "disabled")      # avoids OpenMP affinity aborts in restricted containers
ap = argparse.ArgumentParser(); ap.add_argument("--gpu", action="store_true"); args = ap.parse_args()
fails = []
def check(name, fn):
    try:
        print(f"PASS  {name}: {fn()}")
    except Exception as e:
        fails.append(name); print(f"FAIL  {name}: {type(e).__name__}: {str(e)[:160]}")
def ver(m):
    return lambda: getattr(importlib.import_module(m), "__version__", "imported")
for label, mod in [("numpy","numpy"),("scipy","scipy"),("pandas","pandas"),("matplotlib","matplotlib"),("pint","pint"),
    ("openmm","openmm"),("pdbfixer","pdbfixer"),("openmmforcefields","openmmforcefields"),("openmm-ml","openmmml"),
    ("openmm-torch","openmmtorch"),("mdtraj","mdtraj"),("MDAnalysis","MDAnalysis"),("nglview","nglview"),
    ("py3Dmol","py3Dmol"),("ipymolstar","ipymolstar"),("deeptime","deeptime"),("torch","torch"),
    ("torchani","torchani"),("torch_geometric","torch_geometric"),("e3nn","e3nn"),("mace","mace"),("ase","ase"),
    ("biopython","Bio"),("rdkit","rdkit"),("bioemu2","bioemu2"),("sam2 (aSAM)","sam"),
    ("jupyterlab_rise","jupyterlab_rise")]:
    check(label, ver(mod))
def autograd():
    import torch
    x = torch.tensor([[0.,0.,0.],[1.2,0.,0.]], requires_grad=True)
    U = 0.5*100*((x[0]-x[1]).norm()-1.0)**2; U.backward()      # F = -dU/dx = -k (r - r0)
    f = (-x.grad[1])[0].item(); assert abs(f + 20.0) < 1e-3, f; return f"force {f:.3f} (expected -20)"
check("autograd force (week 4)", autograd)
def msm():
    import numpy as np
    from deeptime.markov.msm import MaximumLikelihoodMSM
    rng = np.random.default_rng(0); P = np.array([[.95,.05,0],[.05,.9,.05],[0,.1,.9]]); s = [0]
    for _ in range(20000): s.append(rng.choice(3, p=P[s[-1]]))
    return np.round(MaximumLikelihoodMSM(lagtime=1).fit_fetch(np.array(s)).timescales(), 1).tolist()
check("deeptime MSM (week 8)", msm)
def omm_cpu():
    import openmm as mm, openmm.app as app, openmm.unit as u
    ff = app.ForceField("amber14-all.xml","amber14/tip3pfb.xml"); m = app.Modeller(app.Topology(), [])
    m.addSolvent(ff, boxSize=mm.Vec3(2,2,2)*u.nanometer)
    s = ff.createSystem(m.topology, nonbondedMethod=app.PME, constraints=app.HBonds)
    sim = app.Simulation(m.topology, s, mm.LangevinMiddleIntegrator(300*u.kelvin, 1/u.picosecond, 0.002*u.picoseconds),
                         mm.Platform.getPlatformByName("CPU"))
    sim.context.setPositions(m.positions); sim.step(20)
    return f"{m.topology.getNumAtoms()} atoms, 20 steps, hasattr runForClockTime={hasattr(sim,'runForClockTime')}"
check("OpenMM CPU run (week 6)", omm_cpu)
if args.gpu:
    def cuda():
        import torch, openmm as mm
        assert torch.cuda.is_available(), "torch sees no GPU"
        names = [mm.Platform.getPlatform(i).getName() for i in range(mm.Platform.getNumPlatforms())]
        assert "CUDA" in names, f"OpenMM platforms: {names}"
        return f"{torch.cuda.get_device_name(0)}; torch CUDA {torch.version.cuda}; OpenMM {names}"
    check("GPU visible to torch and OpenMM", cuda)
    def cueq():
        import cuequivariance as cue, cuequivariance_torch as cet, torch
        ir = cue.Irreps("O3","4x0e+4x1o"); tp = cet.FullyConnectedTensorProduct(ir, ir, ir, layout=cue.ir_mul, device="cuda")
        x = torch.randn(8, ir.dim, device="cuda"); return f"tensor product {tuple(tp(x,x).shape)}"
    check("cuEquivariance kernel (BioEmu2)", cueq)
print("\nALL REQUIRED CHECKS PASSED" if not fails else f"\n{len(fails)} CHECK(S) FAILED: {fails}")
sys.exit(1 if fails else 0)
