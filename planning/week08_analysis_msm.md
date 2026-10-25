# Week 8 — Analyzing simulations: convergence, MSMs and VAMPnets
**Tue Mar 16 / Thu Mar 18** (first week after spring break)

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- **Builds on:** Week 3 (statistical error), Week 4 (leakage), Week 6 (campaign).
- **Data:** about 3 weeks of each team's own campaign data.
- **Sets up:** Weeks 9–10 (comparison against the MD ensemble) and the project. Assign the project proposal here; it is due in Week 9.

## Learning objectives
1. Assess convergence before any other analysis: time series, replica-to-replica comparison, block averages, autocorrelation, and claims the data cannot support.
2. Featurize trajectories (distances, dihedrals, contacts) and reduce them with TICA. Explain the lag time.
3. Build and validate an MSM: clustering, implied timescales, Chapman–Kolmogorov test, stationary distribution, MFPTs, error estimates.
4. Explain the variational approach (VAMP scores) and train a VAMPnet, scored by cross-validation on held-out trajectories.
5. Write an "honesty report" stating what the data supports.

## 2022 source material
- `Week-09/W9_Lecture-MarkovStateModels.ipynb` (29 cells): motivation, MD limitations, MSM definition and properties, features. VAMP/VAMPnets mentioned once. Keep it and add convergence and VAMPnets.
- `Week-09/W9_Lab-SimulationAnalysis.ipynb`:
  - Pentapeptide data from `mdshare` (`pentapeptide-impl-solv.pdb`, `pentapeptide-*-500ns-impl-solv.xtc`) analyzed with **PyEMMA** (30 references).
  - PyEMMA is no longer maintained. Port to **deeptime**, which also provides VAMPnets.
- The VAMPnets topic was scheduled for 2022 Week 12, which was never delivered; it is folded in here.
- Week-1 sEH unbinding trajectory: an optional rare-event example.

## Math support (see audience conventions in `00_course_context.md`)
This is the main linear-algebra week; budget lecture time for it.
- **Transition matrix:** a 3-state example with numbers:
  - each row sums to 1;
  - propagate a population vector by hand for two steps;
  - show the stationary distribution as "the populations that stop changing".
- **Eigenvalues and eigenvectors:** introduce them through that same 3×3 example ("special population patterns that only shrink, without changing shape, each step"), computed with `numpy.linalg.eig` beside the hand reasoning.
- **Implied timescales:** t_i = −τ / ln λ_i with numbers (λ = 0.99, τ = 1 ns → t ≈ 99.5 ns). Explain why eigenvalues near 1 mean slow processes.
- **TICA:** "find the combinations of features that change most slowly". Show it as a picture (a 2-D feature scatter with the slow direction drawn), with the generalized eigenvalue problem in an optional box.
- **VAMP-2:** treat it as "a score for how well the model captures slow processes; higher is better", with the formula optional.

## Lecture ideas (50 min)
- Open with two teams' replicas of the same system disagreeing. Ask which is right; the answer is that neither is converged yet, and the lecture shows how to quantify that.
- MSM from intuition (coarse-grained kinetics) to validation tests; lag-time trade-offs.
- VAMP as "TICA with a neural network", and the VAMP-2 score as a principled model-selection metric.
- A short slide on enhanced sampling (metadynamics, umbrella sampling, weighted ensemble) as the alternative when brute-force sampling is insufficient. This links to the Week 11+ topics.

## Lab ideas (2 h)
1. **Validated pipeline on reference data (45 min).** Port the 2022 pentapeptide lab to deeptime. Students reproduce known implied timescales; this proves the pipeline before applying it to their own data.
2. **Apply to the team's campaign (central activity).**
   - Convergence first: per-replica distributions, block averages, replica disagreement.
   - Then TICA → clustering → MSM → validation.
   - Load representative structures from each metastable state (and the full strided campaign trajectory) in VMD2 to check that the states are physically meaningful.
   - For the folding miniproteins, compare folded fraction and folding time with Lindorff-Larsen 2011 and explain the differences: force field, temperature, HMR, sampling.
3. **VAMPnet vs. TICA+MSM,** scored by cross-validated VAMP-2 on held-out *trajectories* (not frames).
   - Leaderboard across teams that share a system.
4. **Optional: emulated kinetics.**
   - BioEmu2 can propagate structures forward in time. Build an MSM from instructor-precomputed BioEmu2 time-lagged trajectories of the team's system, and compare its implied timescales and stationary populations with the MD-based MSM.
   - Judgment question: does the emulator get the thermodynamics right but the kinetics wrong, or the reverse?
5. **Cross-team discussion (last 20 min):** teams on the same system compare results. "Would you publish this timescale?"

## AI-audit notebook (seeded bugs)
- TICA lag time much shorter than the dynamics of interest; implied timescales never plateau, but the pipeline reports a number.
- Cross-validation split by frames, inflating the VAMP score.
- MSM built by concatenating replicas into one trajectory, creating artificial transitions at the joins.
- Periodic dihedral features used as raw angles instead of sin/cos.

## Prediction prompts
- "Before analysis: is your system converged? What fraction of time do you expect it to spend folded?"

## Deliverables and grading
- Convergence analysis.
- Validated MSM (implied timescales, CK test).
- VAMPnet comparison.
- One-page honesty report.
- AI-audit findings.
- **Project proposal assigned** (due Week 9).

## Build tasks for this thread
- [ ] Port the pentapeptide lab to deeptime and check the reference timescales.
- [ ] Write the campaign-analysis template that handles one trajectory file per segment, multiple replicas and HMR timestep bookkeeping.
- [ ] Fetch the Lindorff-Larsen reference observables for the menu systems.
- [ ] Revise the lecture (convergence, VAMP/VAMPnets, enhanced-sampling outlook).
- [ ] AI-audit notebook, solutions, rubric.
- [ ] Proposal template and rubric (coordinate with `weeks11-14_projects.md`).
