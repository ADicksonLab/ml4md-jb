# Week 7 — Machine-learned force fields
**Tue Mar 2 / Thu Mar 4** (last week before spring break)

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- **Builds on:**
  - Week 2: force-field anatomy and parameterization.
  - Week 4: learned potential + autograd.
  - Week 5: equivariant GNNs.
  - Week 6: OpenMM.
- **Sets up:** ML/MM or MLIP projects.
- **Campaign:** this week includes a health check before the campaign runs unattended through spring break.

## Learning objectives
1. Explain the Behler–Parrinello framework (atomic energy decomposition, symmetry functions, cutoff) and the ANI atomic environment vectors.
2. Explain what equivariant MLIPs (NequIP/Allegro, MACE) add, and where pretrained general-purpose models come from (large QM datasets).
3. Train a small NNP and evaluate energy and force errors properly (held-out molecules or conformers, per-atom vs. per-molecule errors).
4. Test whether a low-error model gives stable, energy-conserving MD, and diagnose failures (extrapolation, missing long-range physics, holes in the training data).
5. Run ML or ML/MM simulations in OpenMM with openmm-ml, and decide when ML/MM is the right choice.

## 2022 source material
- `Week-10/W10_Lecture_FFConcepts.ipynb` (39 cells): classical FF review, high-dimensional NNPs, Behler–Parrinello radial/angular symmetry functions, ANI AEVs, the coordinates → AEV → energy process (formaldehyde example). Figures `Week-10/*.png`. Solid foundation; keep it and add a second half on equivariant and foundation models.
- `Week-10/W10_Lab-MLFF_ANI.ipynb` (62 cells):
  - Trains an ANI model with TorchANI on `ani_gdb_s01.h5` (ANI-1 subset), with `sae_linfit.dat`.
  - Uses `torchani.neurochem` / `torchani.data` / `AEVComputer` APIs. Verify against the current TorchANI release or rewrite.
  - Lab questions 1–3.
- `Week-11/W11_Final-Project-Demo-2-ANI-ASE.ipynb`: ANI + ASE MD on peroxide molecules (`perox*.xyz`); Python 3.7 Miniconda install cell.
- **New material needed:** equivariant MLIPs, foundation models, openmm-ml usage, ML/MM.

## Current tooling to verify in this thread
- openmm-ml: which pretrained models it currently exposes (ANI, MACE variants including MACE-OFF, AIMNet2 and others) and its ML/MM interface (`createMixedSystem` or successor).
- MACE training on a small dataset within a 2 h lab on available GPUs, vs. a TorchANI training exercise.
- Licensing of pretrained models used in class.

## Math support (see audience conventions in `00_course_context.md`)
- **Atomic decomposition:** "total energy = sum of one number per atom", shown first for a 3-atom molecule with numbers.
- **Behler–Parrinello radial symmetry function:** one Gaussian of distance, computed by hand for one atom with two neighbors, then the sum. The angular function: give the formula and plot it rather than deriving it.
- **Cutoff function:** a plot first, then the formula.
- **Equivariant features:** only intuitively, as "features that carry direction (arrows) as well as magnitude"; no tensor algebra.
- **Error metrics:** MAE vs. RMSE with a 4-point example; per-atom vs. per-molecule normalization with numbers.

## Lecture ideas (50 min)
- Arc: Week-2 force field → "what if each atom's energy were a learned function of its neighborhood?" → BP/ANI (keep the 2022 material) → equivariance (Week-5 callback) → foundation models → what they still miss (long-range electrostatics, charge states, reactivity outside training data, cost vs. classical FFs).
- Error metrics: why force MAE, energy MAE and MD stability are different questions.

## Lab ideas (2 h)
1. **Train a small NNP and test it as a simulator.**
   - Train on a single-molecule dataset (e.g. a small organic molecule with energies and forces), or keep the ANI-1 subset.
   - Required: an energy/force parity plot on held-out data, then a 10–100 ps NVE run with the model.
   - Measure energy drift and time to failure; find the first configuration where the model goes wrong and check whether it lies outside the training distribution.
   - Leaderboard: force MAE *and* stable simulation time, under a fixed training budget (time or number of samples).
2. **Pretrained model vs. classical FF on a torsion.**
   - Drive a dihedral of a small drug-like molecule or dipeptide and compare classical FF, a pretrained MLIP and a QM reference profile.
   - Instructors precompute the QM reference so no QM is needed in lab.
   - Judgment question: which would you trust for a 1 µs simulation, and why?
3. **ML/MM in OpenMM.** Treat a ligand (or the campaign peptide's side chain) with an MLIP inside a classical environment via openmm-ml. Measure cost relative to classical; discuss when it is worth it.
4. **Campaign health check (first 20 min of lab).** Every team reports ns accumulated per replica, segment failure rate and projected totals by Mar 16. Fix broken chains before break.

## AI-audit notebook (seeded bugs)
- Units mixed when wrapping an MLIP (eV/Å vs. kJ/mol/nm), giving correct energies and wrong forces, or the reverse.
- Per-atom self-energies not subtracted, so the fit is dominated by atom counts.
- Train/test split by frame for a single-molecule MD dataset (leakage, as in Week 4).
- Model run in float32 for NVE energy conservation, producing drift that is wrongly attributed to the model.

## Prediction prompts
- "Will the model with the lowest force MAE also be the most stable in NVE?"

## Deliverables and grading
- Parity plots + stability analysis + failure diagnosis.
- Torsion comparison with judgment answer.
- ML/MM timing.
- Campaign status.
- AI-audit findings.

## Build tasks for this thread
- [ ] Extend the lecture (keep BP/ANI; add equivariance, foundation models, ML/MM, limits).
- [ ] Choose the training stack (TorchANI vs. MACE vs. both) and dataset; check that it runs in lab time on available hardware.
- [ ] Precompute the QM torsion reference.
- [ ] Write the openmm-ml ML/MM example against the current release.
- [ ] Retire or update the ANI-ASE demo.
- [ ] AI-audit notebook, solutions, rubric.
