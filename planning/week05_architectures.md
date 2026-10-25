# Week 5 — Architectures for molecules: GNNs, equivariance, attention
**Tue Feb 16 / Thu Feb 18**

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- **Builds on:** Week 4 PyTorch training and leakage-aware splits.
- **Sets up:**
  - Week 7: MACE/NequIP are equivariant message-passing networks.
  - Week 9: AF2/AF3 use attention (Evoformer/Pairformer) and AF3 adds diffusion.
  - Week 10: generative models.

## Learning objectives
1. Explain why molecular models should be invariant or equivariant to translation, rotation and permutation, and test a model for it.
2. Describe message passing on molecular graphs, and the difference between invariant (distance-based) and equivariant (vector/tensor feature) networks.
3. Describe self-attention and how transformers are used for sequences and pairs (protein language models, AF-style pair representations).
4. Train a GNN for a molecular property and compare it with a non-invariant baseline.

## 2022 source material
- `Week-03/W3_Lecture_NNArchitectures.ipynb` (28 cells, no code): CNNs, GNNs, E(n)-equivariant GNNs, RNNs (large-timestep integrator example), transformers, attention. Shift the weight from CNN/RNN to GNN/equivariance/attention.
- `Week-03/W3_Lab_ConvNetworks.ipynb`: predicts Rg, SASA and PB/GB solvation energy of `aq15` conformations from xyz coordinates, distance from center, or atom–atom distance matrices. Data: `aq15_pdbs.tgz`, `aq15.{rgyr,sasa,pb,gb}.dat`.
  - The dataset is reusable and a good fit: it is a property-prediction task on MD conformations with targets of increasing difficulty.
  - Replace the CNN models with a GNN.
- Confirm what `aq15` is (a 15-residue peptide?) and how the conformations were generated; record that in the notebook.

## Math support (see audience conventions in `00_course_context.md`)
- **Rotations:** show a 2-D rotation matrix with a numerical example (rotate (1, 0) by 90°) before 3-D. Then:
  - invariance means "the output number does not change when the molecule is rotated";
  - equivariance means "an output arrow rotates along with the molecule".
  Demonstrate both with energy (invariant) and force (equivariant).
- **Message passing:** a sum over neighbors written out for a 4-atom example, with the neighbor list given explicitly.
- **Attention:** softmax and scaled dot-product attention with a 3-token numerical example computed in a notebook cell. Explain the weights as "how much each token looks at each other token".

## Lecture ideas (50 min)
- Live demo: rotate a molecule by 30° and feed it to the 2022 xyz-input model; the prediction changes. Then explain symmetry.
- Message passing in pictures, then the same idea for equivariant vectors (preview of MACE).
- Attention: query/key/value on a toy sequence; then pair representations and triangle updates as a preview of Week 9.

## Lab ideas (2 h)
1. **Invariance unit tests as a required deliverable.**
   - Students write `test_rotation`, `test_translation` and `test_permutation` functions and run them on three models: an xyz-MLP (fails), a distance-matrix MLP (rotation-invariant but not permutation-invariant), and a GNN (passes).
   - The tests carry the grade, so they cannot be skipped.
2. **Property prediction with a GNN on `aq15`.**
   - Train a GNN on Rg (easy), SASA, then GB/PB solvation energy (hard).
   - Compare against the 2022 baselines using leakage-aware splits.
   - Leaderboard on a hidden test split for the PB solvation energy.
3. **"Break the model."** Students search for an input where their model is badly wrong: a compact vs. extended conformation outside the training range, or a perturbed structure with clashes. They explain the failure. This introduces out-of-distribution failure, which matters for MLIPs in Week 7.
4. **Optional:** an attention-weight visualization on a toy sequence task, or a pretrained protein-language-model embedding (e.g. ESM family) for per-residue property prediction, as a Week 9 bridge.

## AI-audit notebook (seeded bugs)
- Message aggregation by summing over a fixed-size padded neighbor list without masking padding atoms, so permutation invariance breaks.
- Graph edges built with a cutoff in Å while coordinates are in nm.
- Batch normalization across a batch of different molecules leaking test statistics.

## Prediction prompts
- "Which target will benefit most from the GNN over the distance-matrix MLP, and why?"

## Deliverables and grading
- Invariance test suite with results for the three models.
- GNN results table with error bars over seeds.
- Break-the-model report.
- AI-audit findings.

## Build tasks for this thread
- [ ] Rewrite the lecture, keeping the EGNN reference and adding attention/pair-representation material.
- [ ] Choose GNN tooling: plain PyTorch (transparent, more code) or PyTorch Geometric (less code, an extra dependency).
- [ ] Rebuild the `aq15` lab, hidden test split, invariance test scaffold and solutions.
- [ ] AI-audit notebook.

## Open decisions
- Keep any CNN content, or drop it entirely?
- Include a protein-language-model exercise here, or leave it for Week 9?
