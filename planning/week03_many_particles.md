# Week 3 — From one particle to many
**Tue Feb 2 / Thu Feb 4**

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- **Builds on:** Week 2 integrators, thermostats and LJ forces.
- **Sets up:**
  - Week 6: PME, cutoffs, barostats and ensembles in OpenMM.
  - Week 8: error bars and autocorrelation in campaign analysis.
  - Students' first real ICER batch work.

## Learning objectives
1. Implement periodic boundary conditions with the minimum-image convention, and explain wrapping vs. unwrapping.
2. Explain cutoffs (shifted/switched potentials), neighbor or cell lists and their O(N) scaling, and why long-range electrostatics needs Ewald/PME.
3. Distinguish the NVE/NVT/NPT ensembles and say what each controls.
4. Compute structural (RDF) and dynamical (MSD, diffusion coefficient) observables **with statistical error bars** (block averaging, autocorrelation time).
5. Submit and manage a Slurm job array on ICER.

## 2022 source material
- `Week-07/W7_Lab_Liquid-Argon-Simulation(-SOLUTIONS).ipynb`:
  - Content: units with `pint`, parameters, `init_vel`, `apply_pbc`, `shortest_disp_vector`, `vvlangevin`, `sim_manager`, `ljenergy`/`ljforces`, `init_positions`, mdtraj topology, `calc_rdf`, runs at several temperatures.
  - Fix: the lab title still says "Week 06".
  - The precomputed trajectories (`Week-07/traj_pos_T{50,80,120,200}.npy`, `traj_vel_T50.npy`) are reusable as fallback data.
- `Week-07/W7_Lecture_MD-Concepts2.ipynb`: the PBC and displacement-vector sections.
- `unsorted/PeriodicBoundaries.ipynb`, `unsorted/units.ipynb`: fold in or link.
- **New material needed:** cutoff shifting, cell lists, a conceptual Ewald/PME slide, ensembles/barostats, MSD/diffusion, block averaging, autocorrelation.

## Math support (see audience conventions in `00_course_context.md`)
- **Minimum image:** a 1-D picture with a box of length L, worked with numbers (x = 0.9L and x = 0.1L), then the formula.
- **Ewald/PME:** conceptual only, no equations required. Explain why 1/r sums converge slowly, using a plot of a running sum.
- **Statistics:** the standard error first as σ/√N with numbers, then the effective N, with N_eff ≈ N/(2τ_corr) (τ_corr measured in units of the sampling interval) motivated by a picture of a correlated time series. Show block averaging as a procedure ("split into blocks, average each, take the spread"), with the formula afterwards.
- **MSD and diffusion:** "mean squared distance grows linearly in time; the slope is 6D in 3-D". Show where the 6 comes from (2 per dimension).

## Lecture ideas (50 min)
- Start with the failure: naïve O(N²) LJ timings for N = 100 → 10,000, extrapolated to a 100k-atom protein system. Ask how anyone can simulate a ribosome.
- Show visually why electrostatics cannot simply be cut off (1/r decays too slowly; artifacts in ion pairs).
- Statistical error: show a time series with an obviously correlated mean, compare naïve and block-averaged error bars, and introduce "effective number of independent samples". This vocabulary is used for the rest of the semester.

## Lab ideas (2 h)
1. **Class phase map of argon (collective).**
   - Each student or team gets a (T, ρ) cell and submits it as one task of a Slurm job array on ICER (CPU is enough; numpy argon runs in minutes).
   - From each run they report the RDF, the diffusion coefficient with error bars, and a phase call (gas/liquid/solid).
   - The class assembles a shared phase map and compares it with the experimental argon triple point (~83.8 K) and the LJ phase diagram from the literature.
   - The external reference is the check; teams whose phase call disagrees must explain why (equilibration, finite size, statistics).
2. **Neighbor-list speed challenge.**
   - Implement a cell list. Students must reproduce the O(N²) energies exactly, then show a scaling plot.
   - Leaderboard on steps/second at N = 2000, with an energy-correctness gate.
3. **Judgment question:** "How long must you run to report D to 5%? Show the calculation from your autocorrelation time."

## AI-audit notebook (seeded bugs)
- Minimum image applied to positions but not to displacement vectors.
- Pair energy double-counted (sum over i ≠ j without the ½).
- Unshifted cutoff, causing energy jumps in NVE.
- MSD computed on wrapped coordinates.

## Prediction prompts
- "Where on your (T, ρ) grid will the system freeze, and what will the RDF look like there?"

## Deliverables and grading
- Phase-map contribution with error bars and phase call.
- Scaling plot and correctness check.
- Convergence calculation.
- AI-audit findings.
- Job-array submission script.

## Build tasks for this thread
- [ ] Update the argon lab (units, title, MSD, block averaging, Slurm array driver).
- [ ] Write the cell-list scaffold with an energy-equality test.
- [ ] Design the (T, ρ) grid and the shared results sheet.
- [ ] AI-audit notebook.
- [ ] Lecture notebook: PBC (reuse), cutoffs, PME concept, ensembles, statistics.
- [ ] Test the job array on a class account.

## Open decisions
- Thermostat for the phase map: Langevin from Week 2, or the students' own choice? The latter adds variability but also a teaching point.
