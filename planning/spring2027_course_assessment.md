# BMB 961 (ML4MD) — Spring 2027 course layout assessment

> Per-week handoff documents live alongside this file in `planning/` (start with `README.md`).

Instructors: Josh Vermaas, Alex Dickson, Michael Feig
Source reviewed: `ADicksonLab/ml4md-jb`, `main` @ `56ceb7a` (last commit 2022-04-07)
Status: planning draft for the `spring2027` branch — nothing in the course content has been changed yet.

---

## 1. What the 2022 course actually was

The posted schedule (`Course_Materials/BMB961-003_Schedule.md`) and the content that was actually delivered diverge at the end of the term.

| Wk | 2022 schedule (lecture / lab) | Delivered in repo | Main tools |
|---|---|---|---|
| 1 | Intro / Colab + Python review | Welcome lecture, Python refresher lab | numpy, mdtraj, nglview |
| 2 | ML basics / first NN | Survey lecture, falling-object regression lab | PyTorch |
| 3 | Advanced NNs / "learning something useful" | CNN/GNN/RNN/Transformer lecture; property prediction (Rg, SASA, PB/GB) from coordinates | PyTorch, sklearn |
| 4 | Generative models / GAN lab | Flows / VAE / GAN lecture; GAN for peptide conformations | PyTorch |
| 5 | Protein structure prediction | AF1/AF2 lecture; compare AF2, RoseTTAFold, RaptorX, I-TASSER, SWISS-MODEL | ColabFold, web servers |
| 6 | Hamiltonian mechanics / argon day 1 | MD Concepts 1; single-particle Langevin lab | numpy |
| 7 | PBC + thermostats / argon day 2 | MD Concepts 2; liquid argon + RDF lab | numpy, pint |
| 8 | Biomolecular simulation / OpenMM | History + OpenMM basics; angiotensin lab | OpenMM 7.6 (`openmm` namespace) |
| 9 | Clustering + MSMs | MSM lecture; featurization/TICA/MSM lab | PyEMMA, mdshare |
| 10 | ML force-field parameterization | BP symmetry functions / ANI lecture; train ANI lab | TorchANI |
| 11 | Reactive NN force fields / ANI simulations | **Final-project demos** (CHARMM-GUI → OpenMM on Colab/HPCC; ANI + ASE) | CHARMM-GUI, ASE |
| 12 | Analysis with NNs / VAMPnets | **Not delivered** (no Week-12 folder) | — |
| 13–15 | Independent projects (~2 wk) + presentations | — | — |

Observations:
- In practice the course ran 10 content weeks + 1 project-demo week, and the VAMPnets / "ML integrators" topics listed in the syllabus never appeared. The syllabus also lists `skorch` hyperparameter optimization, which no notebook uses.
- Three notebooks in `unsorted/` (Hamiltonian mechanics, periodic boundaries, `pint` units) are earlier drafts absorbed into Weeks 6–7.

## 2. Calendar constraint for Spring 2027

MSU Spring 2027: classes begin Tue Jan 19, spring break Mar 6–14, classes end May 2, finals May 3–7. With the unchanged Tue 3:00–3:50 / Thu 2:00–4:00 pattern that gives **14 meeting weeks** (2022 had 15):

| Wk | Tue | Thu | | Wk | Tue | Thu |
|---|---|---|---|---|---|---|
| 1 | Jan 19 | Jan 21 | | 8 | Mar 16 | Mar 18 |
| 2 | Jan 26 | Jan 28 | | 9 | Mar 23 | Mar 25 |
| 3 | Feb 2 | Feb 4 | | 10 | Mar 30 | Apr 1 |
| 4 | Feb 9 | Feb 11 | | 11 | Apr 6 | Apr 8 |
| 5 | Feb 16 | Feb 18 | | 12 | Apr 13 | Apr 15 |
| 6 | Feb 23 | Feb 25 | | 13 | Apr 20 | Apr 22 |
| 7 | Mar 2 | Mar 4 | | 14 | Apr 27 | Apr 29 |
| — | spring break | | | | | |

**14 weeks − 4 project weeks = 10 content weeks** — the same number that was actually delivered in 2022, but now it must also absorb substantial new material (Sec. 4). Something has to be merged or dropped; adding topics without removing others will not fit.

Rooms for 2027: lectures (Tue 3:00–3:50) in Molecular Plant Sciences Building 1030; labs (Thu 2:00–4:00) in Biochemistry Building 202. Consequences:
- Lecture room changes from BPS 1420 to MPS 1030; lab stays in BMB 202. Update the syllabus and `intro.md`.
- Remove the hybrid/Zoom format, Zoom links, and the COVID-19 mask policy.
- All computing runs on ICER. The BMB 202 Linux machines are old and serve only as browser terminals into ICER OnDemand; laptops do the same in lecture. Colab is dropped.

## 3. Does the order still make sense?

The 2022 order is ML basics → ML applications (generative, structure prediction) → MD fundamentals → biomolecular MD → ML for MD. Problems with this order:

1. **ML applications come before students know what MD produces.** The Week 3 lab predicts Rg/SASA/solvation energies of MD conformations, and the Week 4 GAN lab generates peptide conformations and evaluates them with Ramachandran plots — both two to three weeks before MD is introduced. The generative-ensemble topic is much stronger when students can compare generated ensembles against MD ensembles they understand.
2. **Proposal timing.** With a 4-week project starting Apr 6, proposals should be due around Week 8–9. Under the 2022 order, students would have seen biomolecular MD only in Week 8 and no MD analysis or ML force fields yet when choosing a project.
3. **Natural bridge lost.** Forces as −∇U (MD) and autograd (PyTorch) are the same idea; teaching MD first lets the ML-basics week show `torch.autograd` computing forces, which in turn sets up ML force fields.

Arguments for keeping ML first: students start PyTorch practice early, and structure prediction is an attractive hook for biochemistry students. A compromise is to keep a brief AlphaFold-era framing in the Week 1 lecture, while moving the full structure-prediction unit later.

**Recommendation: fundamentals of MD first, then ML basics, then biomolecular MD + analysis, then the ML-for-MD application units, then projects.**

## 4. What has changed since 2022 (topic by topic)

| Topic | 2022 content | Status in 2027 | Suggested action |
|---|---|---|---|
| MD fundamentals (Wk 6–7) | Hamiltonian, Euler vs. velocity Verlet, Langevin, temperature, PBC, argon; LJ energy/forces coded, bonded terms and Coulomb shown as equations only; Berendsen/Andersen/Nosé–Hoover named but only Langevin implemented | Physics unchanged, but coverage of force-field terms and thermostats was thin | **Expand** per Sec. 5a: full force-field anatomy with F = −∇U, integrator and thermostat comparison lab; reuse the numpy code (`vv_langevin`, `ljforces`, `apply_pbc`, `init_vel`) |
| ML basics (Wk 2) | Survey of ML models; first PyTorch regression | Still appropriate | **Keep**, add autograd-as-forces example |
| NN architectures (Wk 3) | CNN, GNN, EGNN, RNN, transformers | Equivariant message-passing networks and transformers are now the core architectures in the field; RNN material is less central | **Revise**: emphasize GNNs/equivariance and attention; replace CNN-on-distance-matrix lab with a GNN lab |
| Generative models (Wk 4) | Flows, VAE, GAN; GAN lab | Diffusion and flow matching have become the dominant generative approaches for molecular structure and ensembles (e.g. AF3's diffusion module, Boltzmann generators, BioEmu-type ensemble emulators) | **Rewrite**: brief VAE/flow background, center on diffusion/flow matching; replace the GAN lab |
| Structure prediction (Wk 5) | AF1/AF2; compare five servers | AF3 (code released late 2024), open reproductions/alternatives (Boltz, Chai, OpenFold3), complexes with ligands/nucleic acids, ColabFold still usable; several 2022 comparison servers are now historical | **Rewrite**: AF2 → AF3 and co-folding; limitations (dynamics, ensembles, confidence metrics); new lab built on AF3-class tools |
| Biomolecular MD (Wk 8) | OpenMM 7.x basics, angiotensin | OpenMM 8.x current; 2022 notebooks already use `openmm` imports but pin `openmm=7.6`; CHARMM-GUI still standard for setup | **Update** version pins and verify against 8.x; merge the CHARMM-GUI demo (old Wk 11) into this lab so students can set up their own system early |
| MD analysis / MSMs (Wk 9) | PyEMMA, mdshare | PyEMMA is no longer maintained (repo archived Sep 2023); deeptime is the maintained successor and also implements VAMPnets | **Port** lab to deeptime; merge in VAMP/VAMPnets (the never-delivered Wk 12 topic) |
| ML force fields (Wk 10–11) | Behler–Parrinello, ANI, TorchANI training; ANI + ASE demo | Equivariant MLIPs (MACE, NequIP/Allegro) and pretrained general models (MACE-OFF, AIMNet2, UMA) now usable directly in OpenMM via openmm-ml, including ML/MM | **Keep** BP/ANI as the conceptual entry point, **add** foundation-model/ML-MM section; lab: small training exercise + openmm-ml simulation |
| ML for sampling / CVs | Not covered | Learned CVs for enhanced sampling (e.g. mlcolvar, deep-TICA) are now routine | **Add** as part of the analysis or generative unit, or as a project-week Tuesday lecture |
| Coarse-grained ML, ML integrators | Listed in syllabus, not delivered | Active research area | Optional Tuesday topic during project weeks |
| AI coding assistants | Not relevant in 2022 | Students will use LLM coding tools | **Add** a syllabus policy and a Week 1 discussion |

## 5. Proposed 14-week layout (draft for discussion)

| Wk | Dates (Tue / Thu) | Lecture | Lab | Reuse from 2022 |
|---|---|---|---|---|
| 1 | Jan 19 / 21 | Welcome; why ML for MD in 2027; course tools; AI-assistant policy | Python/Jupyter refresher; course environment; visualizing a trajectory | Wk 1 (update) |
| 2 | Jan 26 / 28 | How molecular simulation works: F = ma, F = −∇U, anatomy of a classical force field | Integrators (Euler, velocity Verlet, leapfrog, RK45) and thermostats in Python | Wk 6 + Wk 7 (expand; see 5a) |
| 3 | Feb 2 / 4 | From one particle to many: PBC, cutoffs and neighbor lists, long-range electrostatics, ensembles; statistical error and autocorrelation | Liquid argon + RDF, run as a first Slurm job array (temperature sweep) on ICER | Wk 7 lab (keep; add ICER) |
| 4 | Feb 9 / 11 | ML basics; training; autograd (forces as gradients) | First neural network in PyTorch | Wk 2 (revise) |
| 5 | Feb 16 / 18 | Architectures: GNNs, equivariance, attention/transformers | Learning molecular properties with a GNN | Wk 3 (rewrite lab) |
| 6 | Feb 23 / 25 | Biomolecular simulation: force fields, system prep, OpenMM 8; HMR, constraints, checkpointing | CHARMM-GUI → OpenMM; **launch the semester simulation campaign on ICER** (Sec. 5c) | Wk 8 + Wk 11 demo 1 (update) |
| 7 | Mar 2 / 4 | ML force fields: BP/ANI → equivariant MLIPs → foundation models, ML/MM | Train a small NNP; run openmm-ml (ML/MM); campaign health check | Wk 10 + Wk 11 demo 2 (revise) |
| — | Mar 6–14 | Spring break (campaign keeps running) | | |
| 8 | Mar 16 / 18 | Analysis: convergence, featurization, TICA, clustering, MSMs, VAMPnets | MSM / VAMPnet analysis of the students' own ~3-week campaign data with deeptime; project ideas discussed | Wk 9 (port) |
| 9 | Mar 23 / 25 | Structure prediction: AF2 → AF3 and co-folding; limitations | Predict and assess a complex; compare to PDB and to the campaign ensemble | Wk 5 (rewrite) — **proposal due** |
| 10 | Mar 30 / Apr 1 | Generative models for ensembles: VAE/flows → diffusion/flow matching; Boltzmann generators; learned CVs | Generate an ensemble and compare it with the campaign MD ensemble | Wk 4 (rewrite) |
| 11 | Apr 6 / 8 | Project kickoff + Tuesday topic (e.g. ML-enhanced sampling) | Project work | — |
| 12 | Apr 13 / 15 | Tuesday topic (e.g. ML coarse-graining) / check-in | Project work | — |
| 13 | Apr 20 / 22 | Tuesday topic or progress reports | Project work | — |
| 14 | Apr 27 / 29 | Project work | Final presentations | — |

### 5a. Weeks 2–3 in detail: how molecular simulation works

Week 2 follows the Jupyter preliminaries and is meant to take apart a classical force field piece by piece.

**Lecture (Tue Jan 26):**
- Newton: F = ma, with F = −∇U. The force on every atom is the negative gradient of one scalar potential energy.
- Anatomy of a classical force field, one term at a time, each with its functional form and analytic force:
  - Bonded terms: harmonic bonds, harmonic angles (+ Urey–Bradley), periodic dihedrals, impropers, CMAP.
  - Nonbonded terms: Lennard-Jones (combining rules), Coulomb; 1–2/1–3 exclusions and 1–4 scaling.
  - Where the parameters come from (QM targets, condensed-phase data), as the hook for ML force fields in Week 7.
- Integrating the equations of motion: what makes an integrator good for MD (time reversibility, symplecticity, one force call per step) and not just accurate over short times.
- Thermostats as the bridge to temperature.

**Lab (Thu Jan 28): integrators and thermostats**
1. Implement U and −∇U for a 1-D double well and a harmonic bond. Check the analytic forces against finite differences.
2. Integrate with explicit Euler, velocity Verlet, leapfrog, and a general ODE solver (`scipy.integrate.solve_ivp`, RK45 — the Python analogue of MATLAB's `ode45`).
   - Compare energy drift over long runs and the effect of timestep.
   - Count force evaluations per step.
   - Show that RK45's adaptive error control keeps short-time accuracy but still drifts in energy, while Verlet/leapfrog energy errors stay bounded.
3. Thermostats on the same system, or on a small LJ cluster:
   - velocity rescaling
   - Berendsen
   - Andersen
   - Langevin (BAOAB or the existing VV-Langevin)
   - Bussi (CSVR), optionally Nosé–Hoover
   Compare kinetic-energy distributions against the canonical (Maxwell–Boltzmann) result, showing that Berendsen gets the average temperature right but the fluctuations wrong.

**Reuse:**
- The 2022 Week 6 lecture already has Euler vs. velocity Verlet, reversibility, chaos and Langevin.
- The 2022 Week 7 lecture has Maxwell–Boltzmann, `init_vel`, the force-field equations, and a coded Lennard-Jones energy (`ulj`) with PBC helpers; the 2022 Week 7 argon lab has `ljenergy`/`ljforces`. The bonded terms (bonds, angles, dihedrals, impropers) and Coulomb appear only as equations.
- `unsorted/HamiltonianMechanics-STUDENT.ipynb` has a timestep-error exercise that fits step 2.
- New material: leapfrog, RK45, the extra thermostats, and per-term force implementations.

**Week 3** then covers what changes with many particles:
- periodic boundaries and minimum image
- cutoffs and neighbor lists
- why Ewald/PME is needed for electrostatics
- NVE/NVT/NPT

The existing liquid-argon + RDF lab is the exercise, now running with a thermostat students built in Week 2.

**Open question:** the Week 2 content is large. Keep two MD weeks (as above), or compress to one week by moving PBC into the Week 2 lecture and making argon a homework extension? The second option recovers a content week, which the 10-week budget needs.

### 5b. Making the course harder to complete by prompting alone

AI coding assistants can now write most of the 2022 lab code (integrators, LJ forces, a PyTorch training loop, a PyEMMA pipeline) from a one-line prompt. Banning them is unenforceable and teaches the wrong habit. The proposal is to allow them, but to grade what they cannot supply: whether the student can **verify** a result, make and defend **judgments**, and **interpret** it physically. Concrete mechanisms:

1. **Verification is the deliverable.** Each lab requires tests that show the code is correct, not just code that runs. Examples:
   - finite-difference checks of −∇U
   - energy drift vs. dt² for Verlet
   - Maxwell–Boltzmann kinetic-energy distributions from each thermostat
   - detailed balance and implied-timescale plateaus for MSMs
   - train/validation/test splits by trajectory, not by frame (frame-level splits leak correlated data)
   Notebooks that run but have no checks get partial credit.
2. **Audit the AI.** One section per lab gives students an AI-written implementation that contains subtle, realistic errors, and asks them to find and explain them. Candidate seeded bugs:
   - Week 2: Berendsen presented as sampling the canonical ensemble; leapfrog velocities reported at the wrong half-step; a force sign error that only shows up as slow heating.
   - Week 3: minimum image applied to positions but not displacements; LJ energy double-counting pairs; no cutoff shift, producing energy jumps.
   - Week 4/5: test-set leakage from correlated frames; a model that is not rotation-invariant.
   - Week 7: units mixed (kcal/mol vs. kJ/mol, Å vs. nm) when wrapping an MLIP; energies right but forces wrong.
   - Week 8: TICA lag time chosen too short; MSM built on unconverged data, giving confident but meaningless timescales.
3. **Predict before you run.** Before each key simulation, students write a short dated prediction (e.g. "the RDF first peak will drop and broaden at T = 120 K because…", "the MSM slowest process will be…"). They are graded on how they reconcile the prediction with the result, not on whether it was right.
4. **Open questions without a single answer:**
   - What is the largest timestep you would trust here, and why?
   - How long must this simulation run before property X is converged, and what are its error bars (block averaging, autocorrelation time)?
   - Which of these three structure predictions would you use as a simulation starting point?
   These require judgment; an assistant can only offer a plausible-sounding guess.
5. **Short oral check-offs in lab.** The 2-hour Thursday lab allows a 3–5 minute walkthrough per student or team: explain one figure and one function line by line. This is the most reliable check that students understand code they did not type.
6. **Leaderboard challenges with a compute or data budget:**
   - Week 2: largest stable timestep with bounded energy drift.
   - Week 5: GNN property prediction on a hidden test set.
   - Week 7: NNP energy/force MAE under a fixed training budget.
   - Week 10: generated ensemble closest to held-out MD (e.g. Jensen–Shannon divergence over backbone dihedrals).
   These add competition, and students must understand the trade-offs to improve beyond what an assistant produces on the first attempt.
7. **Disclosure and reflection.** Students keep a short AI-use log for each lab and for the project: what they asked, what was wrong, and what they changed. This also produces teaching material for the next offering.

Effect on the syllabus: an explicit AI policy (allowed with disclosure; the student is responsible for every line), and grading shifted from "completed notebook" toward verification, interpretation and oral check-offs (Sec. 7).

### 5c. A semester-long simulation campaign on ICER

All students have ICER access, so the course can include simulations long enough to be worth analyzing: hundreds of nanoseconds to microseconds per team, rather than the few-nanosecond runs that fit in a lab period. The relevant ICER limits (to confirm for class accounts):
- 7-day maximum walltime per job
- 10,000 GPU-hours per calendar year on general accounts
- temporary student accounts that instructors can create for a class

One GPU running continuously for four weeks is about 670 GPU-hours, so the yearly cap is not binding. **Instructor constraint: GPU jobs for this course must run in ≤4 h segments.** Production therefore uses checkpointed, chained segments, each writing its own trajectory file; see `planning/00_course_context.md` and `planning/week06_biomolecular_md.md`. Queue wait and fair-share priority across ~15–20 students will be the practical constraint and should be tested in December.

**Design: one campaign, analyzed by every later unit.**
- **Week 3 — first contact with Slurm.** The argon temperature sweep is submitted as a job array. Students learn submission, monitoring, output handling and `SLURMUsage` on a cheap, low-risk job.
- **Week 6 — launch.**
  - Each team builds a system with CHARMM-GUI from a menu chosen to have known behavior on accessible timescales (suggested below).
  - Teams validate it with a short equilibration in lab, then launch production as chained, checkpointed jobs: several independent replicas, 4 fs timestep with hydrogen mass repartitioning (HMR), restart via Slurm job dependencies.
  - The restart chain itself is part of the lab, because surviving node failures and walltime limits is a real skill.
- **Week 7 — health check.** Before spring break, teams check throughput (ns/day), temperature/pressure/density, and that restarts are working. The campaign then runs through spring break.
- **Week 8 — analysis on the students' own data** (~3 weeks of sampling).
  - Convergence and error bars first, then TICA, clustering, MSM and VAMPnet.
  - Replicas allow a direct comparison of how far apart independent runs are.
  - This is why Weeks 7 and 8 are swapped relative to the earlier draft: analysis now happens after the campaign has had time to sample.
- **Week 9 — structure prediction against the campaign ensemble.** Does the AF3/Boltz model fall inside the MD ensemble? Do confidence metrics (pLDDT/PAE) relate to MD fluctuations?
- **Week 10 — generative models against the campaign ensemble.** aSAM/aSAMt (Feig lab) and BioEmu2 ensembles, plus a model trained in lab, are compared with the team's MD, with error bars from the replicas.
- **Weeks 11–14 — project.** The campaign data is the default starting point for projects, so no team starts its project with zero sampling. Teams can extend the runs, add enhanced sampling or ML/MM, or compare force fields.

**Candidate systems** (to be benchmarked on ICER GPUs before choosing):
- Fast-folding miniproteins with published long-timescale reference simulations (Lindorff-Larsen et al., Science 2011): chignolin/CLN025, Trp-cage, villin headpiece, BBA, WW domain. A reference dataset gives a correctness check that students cannot obtain by prompting.
- Alanine dipeptide or small peptides as a guaranteed-converged fallback.
- Instructor-research systems: a protein–ligand unbinding case (Dickson lab), or a small solute/gas permeating a lipid bilayer (Vermaas lab; CHARMM-GUI Membrane Builder). These are harder, more open-ended options for strong teams.

**Instructor-side requirements:**
- Request class accounts and a course research space for shared data.
- Provide a pinned course environment on ICER (the only computing platform).
- Prepare template Slurm scripts with checkpoint/restart.
- Do a pre-semester benchmark (ns/day per system on the available GPU types).
- Keep a fallback set of instructor-generated trajectories so no team is blocked by a failed campaign.

Design notes:
- Content load: 10 content weeks, matching what was delivered in 2022. Net changes: GAN lab, multi-server comparison and the separate project-demo week are removed; CHARMM-GUI and openmm-ml are folded into regular labs; VAMPnets and learned CVs are added inside existing units.
- Weeks 9 and 10 could be swapped. Keeping structure prediction before generative models lets the AF3 diffusion module introduce diffusion; putting generative models first gives a cleaner theory → application sequence.
- The four Tuesday slots in Weeks 11–14 are 50-minute periods that can carry the "listed but never delivered" topics without consuming content weeks.
- Option: present final projects during the finals-week slot (May 3–7) to recover Apr 29 as a work session.

## 6. Technical debt to clear regardless of layout

- Environment pins: Python 3.7/3.8, `cudatoolkit=10.0`, `openmm=7.6`, `condacolab` install cells, HPCC `module load CUDA/10.0.130`. Replace with a single pinned course environment (environment.yml or lock file) on ICER (OnDemand + batch).
- PyEMMA → deeptime (Wk 9 lab: 30 PyEMMA references).
- TorchANI lab uses the old `torchani.neurochem` / `torchani.data` API — verify against the current release or rewrite.
- Week 5 links to the DeepMind AF2 Colab and to RaptorX / I-TASSER / SWISS-MODEL outputs from 2022.
- Syllabus/intro: instructor list (add Josh Vermaas; affiliate instructors from 2022), dates, lecture room (BPS 1420 → MPS 1030), Zoom/hybrid, COVID policy, expired Slack invite, grading weights for a 4-week project (proposal 10 / project 40 / participation 50 may need rebalancing).
- `_config.yml` author line; `README.md` says "Spring 2022" and refers to `Day-02` folders. Jupyter Book has since released a 2.x line with a different configuration format — decide whether to pin 1.x for this term or migrate.
- Hard-coded `raw/main/...` URLs in `_toc.yml` will point to `main`, not `spring2027`, until the branch is merged.

## 7. Open questions for the instructors

1. Order: adopt MD-first (Sec. 5), or keep ML-first with targeted fixes?
2. *(Resolved: all computing on ICER; BMB 202 machines are browser terminals.)* Open: can ICER provide a recurring reservation for the Thursday lab?
3. Which units does each instructor own? (Natural mapping from 2022: Dickson — MD concepts, analysis; Feig — ML basics, structure prediction; Vermaas — biomolecular simulation/setup, ML force fields?)
4. Is the ~10-content-week budget acceptable, or should the project shrink to 3 weeks to recover one content week?
5. AI coding assistant policy for labs and the final project.
6. Adopt the AI-era grading mechanisms (Sec. 5b)? In particular, are oral check-offs feasible for the expected enrollment, and should participation (currently 50%) be split into lab verification and interpretation, oral check-offs, and attendance?
7. ICER: who requests class accounts and course research space, and can the campaign systems be benchmarked on the available GPU types in December?
8. Campaign system menu: miniproteins with published reference data only, or also instructor-research systems (unbinding, membrane permeation)?
