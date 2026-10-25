# Weeks 11–14 — Independent projects
**Apr 6 – Apr 29** (optionally presentations in finals week, May 3–7)

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- Four weeks for team projects that use the campaign data, the Week 2–10 methods, and ICER.
- Proposals are assigned in Week 8 and due in Week 9 (Mar 23/25), so feedback arrives before kickoff.
- The four 50-min Tuesday slots carry advanced topics; the Thursday 2 h labs are supervised work sessions with check-ins.

## 2022 source material
- `Course_Materials/Final_project_description.pdf` (2 pages): the 2022 project description. Reuse its structure and update it for the requirements below.
- 2022 grading: proposal 10, project 40, participation 50. Rebalance alongside the AI-era mechanisms.
- 2022 project demos (CHARMM-GUI, ANI-ASE) are absorbed into Weeks 6 and 7.

## Project types (menu; students may propose others)
1. **Extend the campaign:** more replicas or longer runs, a force-field comparison (e.g. CHARMM36m vs. AMBER), temperature dependence, or comparison with the reference data.
2. **Enhanced sampling with learned CVs:** use a VAMPnet or deep-TICA CV from Week 8 to drive metadynamics or OPES (e.g. via PLUMED/mlcolvar). Compare cost and accuracy against brute force.
3. **ML/MM or MLIP study:** a ligand or reactive site treated with an MLIP; compare with classical. Or test MLIP stability on a new chemistry.
4. **Generative ensemble benchmark:** aSAM/aSAMt, BioEmu2 or a self-trained model vs. MD for a new system, with rigorous evaluation. Examples:
   - an aSAMt temperature series vs. MD run at several temperatures;
   - BioEmu2 on a protein–ligand or nucleic-acid system vs. MD;
   - BioEmu2 time-lagged kinetics vs. an MD MSM.
5. **Structure prediction + MD:** AF3/Boltz complex prediction → MD stability test → are the predicted interfaces stable?
6. **Research-connected projects** drawn from the students' own labs, subject to instructor approval of scope and compute.

## Requirements that make projects robust to AI-generated work
- **Pre-registered proposal:** question, hypothesis, prediction, planned verification checks, compute budget (GPU-hours, ≤4 h segment plan), fallback plan.
- **Verification section:** the checks used to show that methods and code are correct (as practiced in every lab).
- **Convergence and error bars** on every quantitative claim, or an explicit statement that the claim is qualitative.
- **Reproducibility:** repository with environment lock, scripts and README. Another team must be able to rerun one figure.
- **AI-use log** for the project.
- **Presentation with Q&A** in which each team member answers questions about any part of the project. This is the oral check-off at project scale.

## Weekly structure
| Wk | Tue (MPS 1030) | Thu (BMB 202) |
|---|---|---|
| 11 (Apr 6 / 8) | Topic lecture A + project kickoff (feedback on proposals returned) | Work session; compute plan check (jobs running) |
| 12 (Apr 13 / 15) | Topic lecture B | Work session; **peer review of convergence analyses** (teams swap and critique) |
| 13 (Apr 20 / 22) | Topic lecture C or 5-min progress talks | Work session; draft figures due |
| 14 (Apr 27 / 29) | Topic lecture D or work session | **Final presentations** (or move to finals week and use Apr 29 as a work session) |

## Candidate Tuesday topics (pick four; assign to instructors)
- ML-driven enhanced sampling and learned collective variables (mlcolvar, OPES/metadynamics with NN CVs).
- ML coarse-graining (learned CG force fields, backmapping).
- Large-timestep or learned integrators (listed in the 2022 syllabus, never delivered).
- AI agents and LLMs in computational science: what they can do, how to verify them, reproducibility. This fits the course theme.
- Instructor research talks (one each), as models of how these methods are used.

## Grading (draft for discussion)
- Proposal 10.
- Mid-project check-ins and peer review 10.
- Final report/repository 25.
- Presentation and Q&A 15.
- The remaining 40 for Weeks 1–10 lab work (verification, interpretation, oral check-offs, AI-audit findings) and participation.

## Build tasks for this thread
- [ ] Rewrite the project description (replacing `Final_project_description.pdf`) with types, requirements and timeline.
- [ ] Proposal template + rubric (used in Week 8).
- [ ] Peer-review form for convergence analyses.
- [ ] Final rubric (report, repository, presentation, Q&A).
- [ ] Assign the four Tuesday topics and owners.
- [ ] ICER compute budget per team for weeks 11–14, plus a monitoring script (reuse from Week 6).
- [ ] Decide whether presentations are on Apr 29 or in finals week.
