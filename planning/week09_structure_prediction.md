# Week 9 — Structure prediction: from AlphaFold2 to co-folding
**Tue Mar 23 / Thu Mar 25** (project proposal due)

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- **Builds on:** Week 5 (attention, equivariance) and Week 8 (MD ensembles).
- **Sets up:** Week 10 (AF3's diffusion module introduces generative diffusion), and project starting structures.
- **Key comparison:** static predictions against each team's MD ensemble.

## Learning objectives
1. Trace the history of structure prediction: homology modeling, physics-based folding, coevolution/contacts, AF1, AF2, AF3 and other co-folding models.
2. Explain the AF2 architecture at a conceptual level (MSA + pair representation, Evoformer, structure module) and what AF3 changes (Pairformer, diffusion-based structure generation, ligands/nucleic acids/modifications).
3. Interpret confidence metrics (pLDDT, PAE, pTM/ipTM) and know their limits.
4. Critically assess predictions: complexes, conformational heterogeneity, memorization vs. generalization, and the use of predictions as MD starting points.

## 2022 source material
- `Week-05/W5_Lecture-ProteinStructurePrediction.ipynb` (36 cells): sequence–structure–function, secondary structure, homology modeling, physics-based folding, coevolution, contact prediction, AF1, AF2, quaternary prediction, "are we done?". The historical half is reusable; the AF2-era conclusion needs rewriting.
- `Week-05/W5_Lab_StructurePrediction.ipynb`:
  - Target `7EFY` (`work-7efy/`): PSIPRED secondary structure, then AF2 (DeepMind Colab, ColabFold), RoseTTAFold, RaptorX, I-TASSER and SWISS-MODEL results, compared with mdtraj/NGLview.
  - Several of these servers, and the 2022 job links, are dated.
  - The PDB/GraphQL fetching code is reusable.

## Current tooling to verify in this thread
- Which AF3-class tools students can run: AF3 (weights require an application; GPU), Boltz (open), Chai, OpenFold3, the AlphaFold Server web interface (daily limits), ColabFold for AF2.
- Whether ICER provides any of these, or whether the course environment needs a Boltz install.
- BioEmu2 structure prediction (see `00_course_context.md`), as a comparison point that comes from an ensemble model.
- Instructor experience with local AF3 runs is relevant here.

## Lecture ideas (50 min)
- Keep the history to ~15 min; spend the rest on what changed after 2022 and on the limits.
- Treat confidence scores as model self-assessment, not ground truth: show examples of a high-pLDDT wrong prediction and a low-pLDDT region that is genuinely disordered.
- The ensemble problem: a single prediction vs. Week 8's ensemble. Introduce MSA subsampling and clustering for alternative states as a bridge to Week 10.

## Lab ideas (2 h)
1. **Mini-CASP blind challenge.**
   - Instructors select a few PDB entries released **after** the training cutoffs of the models used: a monomer, a complex, a protein–ligand case.
   - Students predict them and score with lDDT/TM-score/DockQ; leaderboard.
   - The post-cutoff choice prevents memorization. Discuss why that matters.
2. **Prediction vs. the team's MD ensemble.**
   - Predict the campaign system. Does the predicted structure lie inside the MD ensemble (RMSD distribution, TICA projection)?
   - Does per-residue pLDDT anticorrelate with MD RMSF?
   - Judgment question: would you start an MD simulation from this model, and what would you check first?
3. **Single structure vs. ensemble.** Compare AF3/Boltz with BioEmu2 structure prediction for the campaign system, then look ahead to Week 10: does the ensemble model's spread match the MD ensemble?
4. **Alternative states.** For a protein with known multiple conformations, use MSA subsampling or clustering to obtain different predicted states. Compare them with the known structures and discuss whether this samples a Boltzmann ensemble (it does not).

## AI-audit notebook (seeded bugs)
- Structures superposed on all atoms including flexible termini, so the RMSD is misleading.
- Residue numbering offset between prediction and PDB, so the comparison is shifted by N residues.
- pLDDT read from the wrong B-factor column, or scaled 0–1 vs. 0–100.

## Prediction prompts
- "Before running: will the predicted complex interface be correct? Will pLDDT be high where your MD shows flexibility?"

## Deliverables and grading
- Mini-CASP scores with reflection.
- MD-vs-prediction analysis.
- Alternative-state analysis.
- AI-audit findings.
- **Project proposal due.**

## Build tasks for this thread
- [ ] Choose post-cutoff mini-CASP targets close to the semester (check release dates against each model's training cutoff).
- [ ] Decide the tool stack and test installs on ICER (batch GPU jobs; precompute heavy runs for lab).
- [ ] Update the lecture (shorter history; AF3, co-folding, confidence, limits).
- [ ] Rebuild the lab and solutions; retire dated server links.
- [ ] AI-audit notebook, rubric.

## Open decisions
- Swap Weeks 9 and 10? Structure prediction first lets AF3 motivate diffusion; generative first gives a cleaner theory → application order.
