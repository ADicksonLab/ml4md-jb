# Week 4 — Machine learning basics, and forces as gradients
**Tue Feb 9 / Thu Feb 11**

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- **Builds on:** Week 2 (U and −∇U, integrators); Week 3 (correlated samples, error bars).
- **Sets up:**
  - Week 5: architectures.
  - Week 7: an ML force field is this week's lab scaled up.
  - Week 8: train/validation splits on correlated MD data.

## Learning objectives
1. Describe supervised learning: model, loss, gradient descent, train/validation/test, overfitting, regularization.
2. Build and train an MLP in PyTorch (dataset, dataloader, model, optimizer, loop).
3. Use `torch.autograd` to obtain −∂U/∂x from a learned energy, and explain why energy-conserving force fields are trained on energies (and forces) rather than predicting forces directly.
4. Recognize data leakage when samples are time-correlated (MD frames), and use split-by-trajectory or split-by-time.

## 2022 source material
- `Week-02/W2_Lecture_MLBasics.ipynb` (42 cells, no code): survey of ML tasks and models, how training works, data bias, interpretation. Reusable; trim the classical-ML survey (SVM, HMM, random forests) to a slide and add autograd.
- `Week-02/W2_Lab_MLBasics.ipynb`: falling-object regression (`apple.vacuum.dat`, `apple.vacuum.highres.dat`, `apple.leaf.air.highres.dat`) in PyTorch. A good 30-minute warm-up; an assistant can finish it alone, so shorten it.
- Syllabus mentions `skorch` hyperparameter optimization; no 2022 notebook uses it. Drop it, or replace with a small manual or Optuna sweep.

## Lecture ideas (50 min)
- Show the link explicitly: last week's LJ energy written in PyTorch, `U.backward()` producing the same forces as the hand-derived expression. Autograd is the same operation as F = −∇U.
- Then: what if U is not known and must be learned from samples? This is the motivation for Weeks 4–7.
- Data leakage demo with MD frames: a random frame split gives a near-perfect test score; a split by trajectory or time gives an honest one.

## Lab ideas (2 h)
1. **Warm-up (≤30 min):** the falling-apple regression, trimmed. The question shifts from "make it train" to extrapolation: "Where does your model fail, and why?" (vacuum vs. air-resistance data).
2. **Learn a potential, then simulate with it (central activity).**
   - Generate LJ-dimer or Week-2 double-well energies (optionally with forces) and fit an MLP U_θ(r).
   - Get forces by autograd and run the Week-2 velocity Verlet integrator with the learned potential.
   - Students measure energy drift and trajectory divergence from the true potential, and find where the model was not trained (short r).
   - Lesson: a model with low test error can still produce an unstable simulation. This anticipates the Week 7 "low MAE ≠ stable MD" result.
   - Variants: train on energies only vs. energies + forces; compare data efficiency.
3. **Leakage experiment.** Using Week-3 argon frames, predict potential energy from a simple descriptor with random-frame vs. time-block splits, and report both test errors.

## AI-audit notebook (seeded bugs)
- Model evaluated on the training set (or validation used for early stopping *and* final reporting).
- Missing `optimizer.zero_grad()`, so gradients accumulate.
- Forces computed as +∂U/∂x.
- Input normalization statistics computed on the full dataset before the split.

## Leaderboard
- Hidden test set for the learned potential, scored on both energy error and NVE stability time with that potential. Two metrics prevent overfitting to one number.

## Prediction prompts
- "Will a model trained on energies only give good forces?"
- "Where will the learned-potential simulation fail first?"

## Deliverables and grading
- Learned-potential notebook with stability analysis.
- Leakage experiment with both test errors and explanation.
- AI-audit findings.
- Oral check-off on the autograd force calculation.

## Build tasks for this thread
- [ ] Revise the lecture (trim the survey, add autograd and leakage demos).
- [ ] Trim the apple lab; build the learn-a-potential lab and solutions.
- [ ] Generate the hidden test set and stability benchmark script.
- [ ] AI-audit notebook.
- [ ] Decide `skorch` vs. Optuna vs. a manual sweep, and update the syllabus topic list.

## Open decisions
- Design the lab to run in an ICER OnDemand CPU session in minutes, so it does not depend on GPU availability during lab time.
