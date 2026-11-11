import warnings; warnings.filterwarnings("ignore")
import time, openmm as mm, openmm.app as app, openmm.unit as u, torch
print("GPU:", torch.cuda.get_device_name(0), "capability", torch.cuda.get_device_capability(0), "torch CUDA", torch.version.cuda)
ff = app.ForceField("amber14-all.xml","amber14/tip3pfb.xml")
m = app.Modeller(app.Topology(), []); m.addSolvent(ff, boxSize=mm.Vec3(4,4,4)*u.nanometer)
s = ff.createSystem(m.topology, nonbondedMethod=app.PME, nonbondedCutoff=1*u.nanometer, constraints=app.HBonds, hydrogenMass=3*u.amu)
sim = app.Simulation(m.topology, s, mm.LangevinMiddleIntegrator(300*u.kelvin, 1/u.picosecond, 4*u.femtoseconds), mm.Platform.getPlatformByName("CUDA"), {"Precision":"mixed"})
sim.context.setPositions(m.positions); sim.minimizeEnergy(maxIterations=200); sim.step(200)
t = time.time(); sim.step(10000); sim.context.getState(getEnergy=True)
print(f"OpenMM CUDA: {m.topology.getNumAtoms()} atoms, {10000*0.004/1000/((time.time()-t)/86400):.0f} ns/day (4 fs HMR, mixed)")
sim.saveCheckpoint("/tmp/ck.chk"); sim.loadCheckpoint("/tmp/ck.chk"); print("checkpoint save/load OK")
from openmmml import MLPotential
from rdkit import Chem
from rdkit.Chem import AllChem
mol = Chem.AddHs(Chem.MolFromSmiles("CCO")); AllChem.EmbedMolecule(mol, randomSeed=1)
top = app.Topology(); r = top.addResidue("MOL", top.addChain()); els={"C":app.element.carbon,"O":app.element.oxygen,"H":app.element.hydrogen}
at=[top.addAtom(a.GetSymbol()+str(i), els[a.GetSymbol()], r) for i,a in enumerate(mol.GetAtoms())]
for b in mol.GetBonds(): top.addBond(at[b.GetBeginAtomIdx()], at[b.GetEndAtomIdx()])
for name in ["ani2x","mace-off23-small"]:
    try:
        sy = MLPotential(name).createSystem(top)
        cx = mm.Context(sy, mm.VerletIntegrator(0.5*u.femtosecond), mm.Platform.getPlatformByName("CUDA"))
        cx.setPositions(mol.GetConformer().GetPositions()/10.0)
        print(f"openmm-ml {name} OK: E =", cx.getState(getEnergy=True).getPotentialEnergy())
    except Exception as e:
        print(f"openmm-ml {name} FAIL: {type(e).__name__}: {str(e)[:200]}")
