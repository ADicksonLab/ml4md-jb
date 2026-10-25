# Week 6 — Biomolecular simulation with OpenMM, and campaign launch
**Tue Feb 23 / Thu Feb 25**

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- **Builds on:** Weeks 2–3. Every force-field term, integrator, thermostat, cutoff and PBC concept now appears as an OpenMM option.
- **Sets up:** the semester campaign. Its data is analyzed in Weeks 8, 9, 10 and the project.
- **Highest-stakes week:** a failed launch delays everything downstream.

## Learning objectives
1. Map the Week 2–3 concepts onto OpenMM 8 objects: `Topology`, `System`/`Force`s, `Integrator`, `Context`/`Simulation`, reporters.
2. Prepare a solvated biomolecular system with CHARMM-GUI: protonation, missing residues, box size, neutralization/ions, force field and water model choice. Recognize common preparation errors.
3. Use production settings and explain each: PME, cutoffs, constraints, HMR with a 4 fs timestep, Langevin (or other) thermostat, Monte Carlo barostat.
4. Validate an equilibration (T, P, density, energy, RMSD) and benchmark throughput.
5. Run long simulations as ≤4 h checkpointed segments on ICER, and verify that restarts are exact.

## 2022 source material
- `Week-08/W8_Lecture-Biomolecular-Simulation-1.ipynb` (58 cells; Samik Bose):
  - MD history (1964 → 2000s; links to the 2013 Nobel and Feig cytoplasm models);
  - hardware growth;
  - force-field families;
  - OpenMM topology/system/units;
  - water-molecule example (`water.pdb`, `input.pdb`); minimization; writing PDBs.
  - Notebooks already use `openmm` imports; documentation links point to OpenMM 7.0 pages; `openmm=7.6` pinned in setup notes. Update the versions and verify against 8.x.
- `Week-08/W8_Lab-Angiotensin-Simulation.ipynb`: angiotensin (`angiotensin.pdb`), force inspection, mdtraj analysis, a pulling force. A good 30-minute OpenMM warm-up.
- `Week-11/W11_Final-Project-Demo-1-CHARMM-GUI.ipynb`, `CHARMM_GUI_COLAB.ipynb`, `CHARMM_GUI_HPCC.ipynb`: CHARMM-GUI → OpenMM on Colab/HPCC.
  - Their install cells pin Python 3.7, `cudatoolkit=10.0` and `Miniconda3-py37`; the HPCC notebook loads `CUDA/10.0.130` and links the old `wiki.hpcc.msu.edu`.
  - Rewrite them for the course environment and current ICER documentation.
- `Week-08/software.md`: check its contents.

## Campaign system menu (to finalize before the semester)
- Fast-folding miniproteins with published long-timescale reference simulations (Lindorff-Larsen et al., *Science* 2011): chignolin/CLN025, Trp-cage, villin headpiece, BBA, WW domain. The reference data gives teams an external check.
- Fallback: alanine dipeptide or a small peptide that is certain to converge.
- Advanced options: protein–ligand unbinding (Dickson lab expertise; compare to the Week-1 sEH trajectory), or a small permeant crossing a lipid bilayer via CHARMM-GUI Membrane Builder (Vermaas lab expertise).
- For each menu system, instructors need a December benchmark (ns/day per GPU type on ICER) and a fallback trajectory set.

## Lecture ideas (50 min)
- Show a "concept → OpenMM" table, line by line: `HarmonicBondForce` ↔ Week 2 bond term, `NonbondedForce` with PME ↔ Week 3, `LangevinMiddleIntegrator` ↔ Week 2 BAOAB, and so on. Nothing in OpenMM should be a black box.
- System-preparation failures, with images: histidine protonation, a protein interacting with its own periodic image, a non-neutral box, clashes, missing terminal caps.
- HMR and constraints: why 4 fs works, what it changes (dynamics) and what it does not (thermodynamics).
- Revisit the Week-1 Fermi estimates.

## Lab ideas (2 h; likely spills into homework)
1. **Warm-up (20 min):** angiotensin in OpenMM. Inspect forces by force group and connect them to the Week-2 "Match OpenMM" exercise.
2. **System-preparation audit.**
   - Teams get a deliberately flawed prepared system: wrong protonation, missing ions, a box too small for the protein's periodic images, a steric clash.
   - They must find the flaws using only analysis (energies, minimum image distances, net charge, structure checks).
   - Then they prepare their own campaign system correctly with CHARMM-GUI.
3. **Validate and benchmark.** Minimize and equilibrate, inspect the equilibrated box in VMD2 (solvation, ions, periodic images, protein centered), plot T/P/density/energy, measure ns/day on an ICER GPU, and compare with the Week-1 prediction.
4. **Restart-exactness test (required before launch).**
   - Run N steps continuously vs. N/2 + restart + N/2 from a checkpoint, and compare the final states.
   - Checkpoints restore the full state, including RNG and velocities. Bitwise identity additionally requires deterministic force summation on the GPU platform; check the OpenMM platform properties.
   - State-XML restarts are close but not bitwise.
   - Discussing why is part of the lesson.
5. **Launch.**
   - Several replicas per team (different seeds or starting structures).
   - Chained ≤4 h segments using the provided runner template: `runForClockTime` or an equivalent step budget, checkpoint and state files, one trajectory file per segment.
   - Slurm dependency chain or self-resubmission; a log file recording each segment.
   - Instructors check that every team's chain is running before Week 7.

## AI-audit notebook (seeded bugs)
- Runner appends to a single DCD, so a killed segment corrupts the trajectory.
- Restart reads positions but not velocities or the box, so the system silently reheats or the box resets.
- Barostat added but `System` already has a fixed box from a different file.
- Timestep 4 fs without HMR or constraints.
- `runForClockTime` budget longer than the Slurm walltime, so the final checkpoint is never written.

## Prediction prompts
- "What ns/day will your system achieve, and how many µs per replica by Mar 16?" Revisit both in Weeks 7 and 8.

## Deliverables and grading
- Preparation audit findings.
- Validation plots.
- Benchmark.
- Restart-exactness result.
- Running chain (job IDs + first segment output).
- Oral check-off: walk through the runner script.

## Build tasks for this thread
- [ ] Finalize the menu; benchmark each system on ICER GPU types; generate fallback trajectories.
- [ ] Write and test the ≤4 h segment runner template and Slurm chain scripts (including failure and resubmit behavior).
- [ ] Build the flawed system for the audit.
- [ ] Rewrite the lecture (update the 2022 Week 8 material; add the concept → OpenMM table, preparation pitfalls and HMR).
- [ ] Rewrite the CHARMM-GUI → OpenMM notebooks for the course environment and current ICER.
- [ ] Monitoring script that summarizes ns accumulated per team and replica (used in Week 7).
- [ ] Rubric.

## Open decisions
- Replicas per team, and GPU-hours per team, given queue throughput.
- Shared course research space vs. team directories for trajectory storage.
- Default force field and water model (e.g. CHARMM36m/TIP3P vs. AMBER ff19SB/OPC) and whether teams may choose.
