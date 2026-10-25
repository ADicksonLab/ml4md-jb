# BMB 961 (ML4MD) Spring 2027 — shared context for all weekly planning threads

Read this first. Each `weekNN_*.md` file is written to be handed to a separate planning conversation; this file holds everything those threads have in common so it is not repeated in each one.

## Course facts

- **Course:** BMB 961, *Machine Learning for Molecular Dynamics*, Michigan State University, Spring 2027.
- **Instructors:** Josh Vermaas, Alex Dickson, Michael Feig.
- **Meetings:**
  - Lecture: Tue 3:00–3:50 PM, Molecular Plant Sciences Building 1030. Students bring laptops.
  - Lab: Thu 2:00–4:00 PM, Biochemistry Building 202 (computer suite). The BMB 202 Linux machines are old and serve as browser terminals into ICER. The one exception is the instructors' existing VMD2 container, which also runs locally on these workstations.
- **Semester:** classes Jan 19 – Apr 29 (14 meeting weeks); spring break Mar 6–14; finals week May 3–7.
- **Repository:** `ADicksonLab/ml4md-jb`, local clone `/home/josh/git/ml4md-jb`, working branch `spring2027`. 2022 material is on `main` in `Week-01/` … `Week-11/` and `unsorted/`. It is a Jupyter Book (`_toc.yml`, `_config.yml`); notebooks are not executed at build time.
- **Full assessment and rationale:** `planning/spring2027_course_assessment.md`.

## Semester sequence (agreed draft)

| Wk | Dates (Tue / Thu) | Topic | Handoff doc |
|---|---|---|---|
| 1 | Jan 19 / 21 | Welcome, Jupyter/Python, environment, ICER onboarding | `week01_welcome_tools.md` |
| 2 | Jan 26 / 28 | How molecular simulation works: F = ma, F = −∇U, force-field anatomy, integrators, thermostats | `week02_md_fundamentals.md` |
| 3 | Feb 2 / 4 | Many particles: PBC, cutoffs, neighbor lists, electrostatics, ensembles, statistical error | `week03_many_particles.md` |
| 4 | Feb 9 / 11 | ML basics, training, autograd (forces as gradients) | `week04_ml_basics.md` |
| 5 | Feb 16 / 18 | Architectures: GNNs, equivariance, attention | `week05_architectures.md` |
| 6 | Feb 23 / 25 | Biomolecular simulation with OpenMM 8; **campaign launch** | `week06_biomolecular_md.md` |
| 7 | Mar 2 / 4 | ML force fields: BP/ANI → equivariant MLIPs → foundation models, ML/MM | `week07_ml_force_fields.md` |
| — | Mar 6–14 | Spring break (campaign keeps running) | — |
| 8 | Mar 16 / 18 | Analysis: convergence, TICA, MSMs, VAMPnets, on campaign data | `week08_analysis_msm.md` |
| 9 | Mar 23 / 25 | Structure prediction: AF2 → AF3 and co-folding (**proposal due**) | `week09_structure_prediction.md` |
| 10 | Mar 30 / Apr 1 | Generative models for ensembles | `week10_generative_ensembles.md` |
| 11–14 | Apr 6 – Apr 29 | Independent projects; four Tuesday topic lectures; presentations | `weeks11-14_projects.md` |

## Cross-cutting design principle: grade what AI tools cannot supply

Students may use AI coding assistants, must disclose that use, and are responsible for every line. Because code is now cheap to produce, each lab should be built from some combination of the mechanisms below. Each weekly doc proposes specific instances.

| Mechanism | What it looks like in a lab |
|---|---|
| **Verification as deliverable** | Tests that show correctness (finite-difference forces, energy-drift scaling, distribution checks, matching a reference code to a tolerance). Code without checks gets partial credit. |
| **Audit the AI** | A provided "AI-written" implementation with 2–4 realistic seeded bugs; students find, explain and fix them. |
| **Predict before you run** | A short written prediction before a key run; graded on how it is reconciled with the result. |
| **Judgment questions** | Questions with no single right answer (timestep choice, convergence, which model to trust), graded on the reasoning given. |
| **Oral check-off** | 3–5 min in lab: explain one figure and one function line by line. |
| **Leaderboard** | A fixed compute or data budget, a hidden test set, and a public ranking. |
| **External reference** | A comparison to experiment or a published dataset that cannot be faked (argon triple point, Lindorff-Larsen 2011 folding data, OpenMM energies, PDB structures released after model training). |
| **AI-use log** | A short log per lab of what was asked, what was wrong, and what was changed. |

## Cross-cutting spine: the semester simulation campaign on ICER

- **What:** each team runs a multi-replica production simulation of one system from Week 6 through the project.
- **Who uses it:** Weeks 8, 9, 10 and the project all analyze it.
- **ICER constraint:** GPU jobs for this course must be split into **≤4 h segments**. Each segment must:
  - restart from an OpenMM checkpoint/state file;
  - write its own trajectory file (`seg_0001.dcd` …), so a killed segment never corrupts earlier data;
  - stop itself cleanly before the walltime;
  - be chained (Slurm `--dependency=afterok`, or a self-resubmitting script).

  OpenMM's `Simulation.runForClockTime(...)`, with checkpoint and state files, appears suited to this; confirm its behavior in the Week 6 thread. A minimal runner is ~50 lines and should be a provided template, with students responsible for understanding and testing it.
- **Throughput:** queue wait between segments reduces the duty cycle below 100%. Benchmark real ns/day *and* real segments/day in December.
- **Teaching opportunity:** the short-segment constraint suits the many-short-trajectories regime in which MSMs work well. Several replicas per team give real error bars.
- **ICER policy facts (from ICER documentation):** 7-day maximum walltime; general accounts capped at 10,000 GPU-hours/year; instructors can create temporary class accounts. The 4-hour constraint comes from the instructors and applies to the GPU resources available to the class.
- **Fallback:** instructor-generated trajectories of every menu system, so no team is blocked by a failed campaign.

## Cross-cutting thread: generated structural ensembles vs. MD

Ensembles from ML generators should be compared directly against the teams' own MD. Two generators are the anchors:

- **aSAM / aSAMt** (Feig lab: Janson, Jussupow & Feig, *Commun. Chem.* 2025, doi:10.1038/s42004-025-01737-2; code and weights at `github.com/giacomo-janson/sam2`).
  - A latent diffusion model that generates heavy-atom protein ensembles.
  - It is conditioned on an initial structure; aSAMt (trained on mdCATH) is also conditioned on temperature.
  - Weights trained on ATLAS and on mdCATH are provided.
  - The paper compares aSAMt with long MD of fast-folding proteins, which are the same systems as the campaign menu. This gives a published baseline for the class comparison.
  - Instructor expertise is in-house.
- **BioEmu2** (Microsoft Research AI for Science, `github.com/microsoft/bioemu2`).
  - Public preview announced Oct 20, 2026 (first tag `v0.1.0rc0`); MIT license, open weights.
  - Handles proteins, nucleic acids and ligands.
  - Provides equilibrium sampling, structure prediction and forward-in-time (time-lagged) trajectory generation.
  - Requires Linux and an NVIDIA GPU; context-parallel sampling needs ≥4 GPUs.
  - The original BioEmu repository is archived in favor of BioEmu2.
  - Because BioEmu2 is a preview release, **pin a version in December** and re-test before the semester.

Where it appears:

| Week | Use |
|---|---|
| 8 | Optional: BioEmu2 time-lagged trajectories → MSM, compared with the MSM from the team's MD (kinetics, not just populations) |
| 9 | BioEmu2 structure prediction alongside AF3/Boltz; single structure vs. ensemble |
| 10 | **Main comparison:** aSAM/aSAMt and BioEmu2 ensembles vs. the team's campaign MD and the Lindorff-Larsen reference |
| 11–14 | Projects, e.g. aSAMt temperature series vs. MD at several temperatures; BioEmu2 on a protein–ligand or nucleic-acid system |

Instructors should precompute aSAM and BioEmu2 ensembles for every menu system on ICER GPUs, so that lab work is analysis rather than waiting in the queue.

## Course-wide infrastructure (owned outside the weekly threads)

1. **ICER is the computing platform for everything.**
   - Labs and in-lecture activities run in ICER OnDemand Jupyter sessions, opened from BMB 202 machines or laptops in a browser.
   - The campaign and all GPU-heavy work run as Slurm batch jobs.
   - Colab is not used; at most it is an emergency fallback if ICER is down.
   - One pinned course environment (conda/pixi lock file) lives on ICER: a shared install in the course research space, or one built per student from the lock file in Week 1.
   - **Lab-time capacity:** ~20 students requesting OnDemand sessions at 2:00 PM on Thursday may wait in the queue. Ask ICER about a recurring Slurm reservation for Thursday 2–4 PM (and short Tuesday activities). Design labs so that CPU sessions suffice for the interactive work, with GPU-heavy steps (MLIP training, AF3/Boltz, BioEmu2, aSAM) either submitted as batch jobs or supplied as precomputed outputs in the course space.
   - Sessions longer than 4 h are not needed in lab; the 4 h limit matters only for the campaign.

   The environment replaces the 2022 pins (Python 3.7/3.8, `cudatoolkit=10.0`, `openmm=7.6`, `condacolab`, `module load CUDA/10.0.130`). Weekly threads should list the packages they need rather than install ad hoc.
2. **Molecular visualization in notebooks** (decide and test on ICER OnDemand in December).
   - **NGLView** stays the default for trajectories, because it takes mdtraj/MDAnalysis objects directly and has a frame player.
     - The 4.0.1 package has an open frontend-version bug; pin a combination that has been tested.
     - Its JupyterLab extension must be installed in the *Jupyter server* environment that OnDemand launches, not only in the course kernel.
   - **Mol\*** via ipymolstar or MolViewSpec for structure prediction (Week 9: pLDDT coloring, AF3 outputs), so students use the same viewer as RCSB and the AlphaFold DB.
   - **py3Dmol** as the widget-free fallback, and for small generated ensembles (Week 10).
   - **VMD2 is the primary viewer for full trajectories.**
     - All three instructors know VMD, and a VMD2 container used in other courses already runs through ICER OnDemand and on the BMB 202 workstations.
     - Use it for campaign trajectories (multi-µs, one file per segment), which are too large for browser widgets.
     - It also gives students a standard tool for selections, alignment, RMSD/RMSF and rendering figures.
     - Notebook widgets are for quick in-notebook views only. Always stride or subsample before viewing in a notebook.
     - Point the course at the existing container rather than building a new install. Check that it reads the campaign output formats (DCD/XTC + PSF/PDB from CHARMM-GUI) and the course research-space paths.
   - Wrap the chosen backend in one course helper (e.g. `view(traj, stride=...)`), so a broken widget can be swapped without editing every notebook.
3. **ICER:** class accounts, course research space for shared data and fallback trajectories, template Slurm scripts.
4. **Syllabus / `intro.md`:**
   - instructors, rooms and dates;
   - remove the Zoom/hybrid format and COVID text; replace the expired Slack invite;
   - AI policy;
   - grading rebalanced toward verification, interpretation and oral check-offs. The 2022 weights were participation 50 / proposal 10 / project 40.
5. **Jupyter Book:** stay on 1.x or migrate to 2.x; `_toc.yml` `raw/main/...` URLs must point to the right branch; update the README.

## Conventions for the weekly threads

- Each thread delivers, for its week:
  - lecture notebook (slides via `jupyter nbconvert --to slides`);
  - student lab notebook and a separate solutions notebook (the 2022 `-SOLUTIONS.ipynb` pattern);
  - seeded-bug "AI-audit" notebook, where applicable;
  - data files or fetch scripts;
  - grading rubric;
  - `_toc.yml` entries;
  - list of required packages.
- Put new material in `Week-NN/` folders numbered by the **2027** week. 2022 folder numbers differ; each weekly doc lists its source folders.
- Use the units already set up in the 2022 labs (reduced LJ units with `pint` in the argon lab; OpenMM units in biomolecular labs) and state them in every notebook.
- Solutions must not be published to the student-facing book.
