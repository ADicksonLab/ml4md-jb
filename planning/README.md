# Spring 2027 planning documents

Handoff documents for updating BMB 961 (ML4MD). Each weekly file is written for its own planning conversation.

**Start here:** [`00_course_context.md`](00_course_context.md) covers:
- rooms, dates and instructors;
- the semester sequence;
- the cross-cutting rule of grading what AI tools cannot supply;
- ICER as the only computing platform, and the simulation campaign (≤4 h segments);
- comparisons of generated ensembles (aSAM/aSAMt, BioEmu2) with MD;
- environment and repository conventions.

| File | Week(s) | Topic |
|---|---|---|
| `week01_welcome_tools.md` | 1 | Welcome, tools, ICER onboarding |
| `week02_md_fundamentals.md` | 2 | F = ma, F = −∇U, force fields, integrators, thermostats |
| `week03_many_particles.md` | 3 | PBC, neighbor lists, ensembles, statistical error, argon phase map |
| `week04_ml_basics.md` | 4 | ML basics, autograd forces, learned potentials |
| `week05_architectures.md` | 5 | GNNs, equivariance, attention |
| `week06_biomolecular_md.md` | 6 | OpenMM 8, CHARMM-GUI, campaign launch |
| `week07_ml_force_fields.md` | 7 | BP/ANI → MACE → foundation models, ML/MM |
| `week08_analysis_msm.md` | 8 | Convergence, TICA, MSMs, VAMPnets on campaign data |
| `week09_structure_prediction.md` | 9 | AF2 → AF3/co-folding vs. MD ensembles |
| `week10_generative_ensembles.md` | 10 | Diffusion/flow matching, Boltzmann generators; aSAM/aSAMt and BioEmu2 vs. MD |
| `weeks11-14_projects.md` | 11–14 | Projects, Tuesday topics, grading |
| `spring2027_course_assessment.md` | — | Full assessment of the 2022 course and rationale for the new layout |

Each weekly doc has the same sections:
1. Role in the course
2. Learning objectives
3. 2022 source material (files, what to reuse, what is stale)
4. Lecture ideas
5. Lab ideas
6. AI-audit seeded bugs
7. Prediction prompts
8. Deliverables
9. Build-task checklist
10. Open decisions

Weeks 7, 9 and 10 also list current tooling to verify before building.
