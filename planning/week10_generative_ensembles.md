# Week 10 — Generative models for molecular ensembles
**Tue Mar 30 / Thu Apr 1**

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- **Builds on:** Week 4 (training), Week 5 (equivariance), Week 8 (ensembles and error bars), Week 9 (AF3 diffusion).
- **Last content week** before projects; several projects may build on it.

## Learning objectives
1. Explain the main generative-model families: VAE, normalizing flows, GAN (briefly), diffusion and flow matching. Say why diffusion and flow matching now dominate molecular structure generation.
2. Explain Boltzmann generators and why exact likelihoods allow reweighting to the true Boltzmann distribution.
3. Describe pretrained ensemble generators, in particular aSAM/aSAMt (latent diffusion conditioned on structure and temperature) and BioEmu2 (equilibrium sampling and time-lagged generation for proteins, nucleic acids and ligands), and learned collective variables (e.g. mlcolvar) as ways to accelerate or replace sampling.
4. Evaluate a generated ensemble rigorously:
   - distributional distances (JS divergence over dihedrals/TICA);
   - classifier two-sample tests;
   - physical validity (clashes, bond lengths, chirality);
   - error bars from MD replicas.

## 2022 source material
- `Week-04/W4_Lecture_GenerativeModels.ipynb` (66 cells): what generative models are, molecular applications, representations, normalizing flows, VAEs, GANs. Clear and reusable for the background half; add diffusion and flow matching, Boltzmann generators and emulators.
- `Week-04/W4_Lab_GenerateMolecularConformations.ipynb`:
  - A GAN on alanine dipeptide heavy-atom positions (FU Berlin `alanine-dipeptide-3x250ns-heavy-atom-positions.npz` via mdshare; `alanine-dipeptide-nowater.pdb`).
  - Evaluation uses distance distributions and Ramachandran plots.
  - The dataset and evaluation code are reusable; replace the GAN with diffusion or flow matching.

## Current tooling to verify in this thread
- **aSAM/aSAMt** (`github.com/giacomo-janson/sam2`; Janson, Jussupow & Feig, *Commun. Chem.* 2025):
  - inputs: initial PDB structure, optional temperature;
  - available weights: ATLAS, mdCATH;
  - runtime per ensemble on ICER GPUs;
  - output format.
  - Feig lab can advise directly.
- **BioEmu2** (`github.com/microsoft/bioemu2`; public preview, `v0.1.0rc0`, MIT):
  - install on ICER (Linux + NVIDIA GPU);
  - CLI `sample-equilibrium` and the Python API;
  - single-GPU runtime for the menu systems;
  - API stability before January. Pin a version.
- Precompute ensembles for all menu systems so lab time is spent on analysis.

## Lecture ideas (50 min)
- 15 min of background on VAEs and flows from the 2022 lecture; GANs reduced to one slide of history.
- Diffusion and flow matching from first principles. The link to Langevin dynamics from Week 2 is direct: score-based sampling is closely related to Langevin dynamics on a learned score (annealed Langevin sampling is exactly that).
- Boltzmann generators vs. emulators: exact (reweightable) vs. approximate, and where each is useful.
- Two current generators as case studies, contrasting what each is trained on and conditioned on:
  - **aSAM/aSAMt:** trained on MD (ATLAS/mdCATH), conditioned on a starting structure and temperature. Its paper benchmarks against fast-folding protein MD, the same systems as the campaign.
  - **BioEmu2:** a foundation model covering multiple molecule types, with time-lagged generation.
- How to evaluate a generated ensemble so the result is credible.

## Lab ideas (2 h)
1. **Train a small diffusion or flow-matching model on alanine dipeptide** (internal coordinates or φ/ψ first, Cartesian as an extension). Compare with the 3×250 ns MD reference: Ramachandran JS divergence, basin populations with error bars from the three MD trajectories.
   - Leaderboard: JS divergence to held-out MD.
   - Physical-validity gate: no clashes; correct L-chirality.
2. **"Turing test" for ensembles.** Train a classifier to distinguish MD from generated samples. Classifier accuracy near 50% means the two ensembles are indistinguishable. Students report this alongside JS divergence and discuss what each metric misses.
3. **aSAM and BioEmu2 vs. the team's campaign (central comparison).**
   - Using instructor-precomputed ensembles (or a short batch job), compare aSAM/aSAMt and BioEmu2 ensembles with:
     - the team's MD replicas;
     - the Lindorff-Larsen reference;
     - the student-trained model from part 1, where applicable.
   - Metrics:
     - same TICA projection as Week 8;
     - folded fraction;
     - RMSF profile;
     - JS divergence with replica-based error bars;
     - classifier two-sample test;
     - physical validity (clashes, chirality).
   - Compare the cost: GPU-minutes for the generators vs. GPU-days for the MD.
   - Judgment question: what would you use these generators for, and what would you not? Where does the MD itself fall short (force field, convergence)?
   - Optional: an aSAMt temperature series vs. the Week 3 idea of temperature-dependent structure.
4. **Optional:** reweight a flow's samples to the Boltzmann distribution (small system) to show the Boltzmann-generator idea.

## AI-audit notebook (seeded bugs)
- Evaluated against the training data instead of held-out MD.
- φ/ψ treated as non-periodic in the model or the JS histogram (wrap-around at ±180°).
- Generated Cartesian structures include D-amino acids (chirality not checked).
- Noise schedule or timestep mismatch between training and sampling.

## Prediction prompts
- "Which basin will your model under-populate, and why?"

## Deliverables and grading
- Model + evaluation table (JS, classifier test, validity) with error bars.
- Emulator vs. campaign comparison with judgment answer.
- AI-audit findings.

## Build tasks for this thread
- [ ] Extend the lecture (keep VAE/flow background; add diffusion and flow matching, Boltzmann generators, emulators, evaluation).
- [ ] Build the diffusion/flow-matching scaffold on the 2022 alanine dipeptide data; check that it trains in lab time.
- [ ] Install and pin aSAM and BioEmu2 on ICER; precompute ensembles for all menu systems; record runtimes.
- [ ] Classifier two-sample test helper.
- [ ] AI-audit notebook, solutions, rubric.
