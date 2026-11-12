# Week 1 — Welcome, tools, and first contact with a simulation
**Tue Jan 19 (lecture, MPS 1030) / Thu Jan 21 (lab, BMB 202)**

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- **Sets up:** course environment, ICER login, team formation, AI policy, the habit of verification.
- **Next weeks need from it:** every student able to open the course environment in an ICER OnDemand Jupyter session (from a BMB 202 machine or a laptop) and to submit a trivial Slurm job. ICER is the only computing platform in the course, so this must work on day one. Week 3 uses Slurm for real; Week 6 launches the campaign.

## Learning objectives
1. Navigate Jupyter, the course book and the course environment; install and import packages; find documentation.
2. Use numpy fluently enough for Weeks 2–3: array manipulation, vectorization, reading and writing arrays.
3. Log into ICER, start an OnDemand Jupyter session, and submit and monitor a batch job.
4. Explain the course AI policy and why verification matters.

## 2022 source material
- `Week-01/W1_Lecture_Welcome.ipynb` (29 cells): course details, why MD, why ML for MD, background, grading, Slack, community standards, in-class activities (introductions; NGLview of a protein).
  - Keep the structure; rewrite the "why ML for MD" section and update logistics.
- `Week-01/sEH_nowater.pdb`, `Week-01/sEH_unbinding.dcd`: soluble epoxide hydrolase ligand-unbinding trajectory used for the NGLview demo. Reusable.
- `Week-01/W1_Lab_Python_Refresher.ipynb` (83 cells): Jupyter shortcuts, packages and docs, numpy, object-oriented programming (card-deck shuffling exercise). This is a skills drill an assistant can complete instantly; restructure as below.
- `Course_Materials/learn_python.zip`, `BMB_Community_Standards.pdf`: check whether they are still current.
- Stale: Zoom links, Slack invite, Anaconda/Python 3.8 instructions in `SoftwareSetupGuide.md`, COVID policy.

## Lecture ideas (50 min)
- **Hook — two Nobel Prizes a decade apart.** 2013: multiscale models of complex chemical systems (Karplus, Levitt, Warshel; already linked in the 2022 Week 8 lecture). 2024: computational protein design and structure prediction (Baker, Hassabis, Jumper). The course sits between them.
- **The 2027 landscape in one slide each:** structure prediction and co-folding, ML force fields, generative ensembles, ML analysis of MD. Show what each can and cannot do yet. This previews the semester.
- **AI-assistant policy as a discussion, not a rule list.** Live demo: ask an assistant to write a velocity Verlet integrator (it will succeed), then ask how to tell whether it is correct. That question frames the course.
- **Fermi estimate exercise (5 min, in pairs):** how long would 1 µs of the sEH system in water take on a laptop CPU, an ICER CPU node and an ICER GPU? Collect the estimates and revisit them in Week 6 when teams benchmark real ns/day.
- **Short in-class activity:** visualize the sEH unbinding trajectory with NGLview (2022 activity 2). Ask what you would need to measure to say *how long* unbinding takes. This previews Weeks 3 and 8.

## Lab ideas (2 h)
- **ICER onboarding first (≈45 min):** everything else in the lab runs there. Details are in the onboarding bullet below.
- **Replace the drill with a "trajectory detective" notebook.** Students load `sEH_unbinding.dcd` with mdtraj/numpy and answer quantitative questions:
  - ligand–protein distance over time;
  - frame of unbinding;
  - residues the ligand contacts before leaving;
  - Rg of the protein.

  Every answer must include a check (e.g. compute a distance two ways: mdtraj and raw numpy). This exercises numpy, plotting and documentation lookup on real MD data.
- **Small "AI-audit" warm-up:** a provided assistant-generated snippet contains plausible but wrong code (e.g. a nonexistent mdtraj function name or argument, or nm/Å confusion). Students find the errors by reading the documentation.
- **ICER onboarding (first 45 min):** OnDemand login, open the course environment, `sbatch` a provided job (no `--account` line; it runs under the student's default account) that runs a small numpy benchmark, check it with `squeue`/`sacct`, retrieve the output. Confirm that each student can read the research space, i.e. is in the `BMB_961_SS27_001` group.
- **VMD2 first look (15 min):** open the same sEH trajectory in the VMD2 container (ICER OnDemand or locally in BMB 202), make one representation and one measurement, and compare with the notebook view. VMD2 becomes the tool for full campaign trajectories from Week 6 onward.
- Keep the object-oriented material only as optional self-study (`learn_python.zip`). Week 2 needs functions and arrays more than classes.

## Engagement levers
- Background survey (programming, physics, chemistry, biology, ML) to form balanced teams of 2–3 for the semester; teams persist into the campaign.
- Short oral check-off: each student explains one plot from the detective notebook.

## Deliverables and grading
- Detective notebook, with checks (completion + correctness of checks).
- Proof of a successful ICER job (job ID + output).
- AI-use log entry #1.

## Build tasks for this thread
- [ ] Rewrite the lecture notebook (logistics, 2027 landscape, AI policy, Fermi estimate).
- [ ] Write the trajectory-detective lab and its solutions; keep the sEH files.
- [ ] Write the AI-audit snippet.
- [ ] Write the ICER onboarding page and test job (no `--account`). Test before Jan 19 from an ICER account that is **not** in the Vermaas/Dickson/Feig labs, i.e. a plain student account, so that lab defaults do not hide problems.
- [ ] Rewrite `SoftwareSetupGuide.md` around ICER: OnDemand Jupyter, the course environment, Slurm basics. BMB 202 machines and laptops serve only as browser clients.
- [ ] Draft the AI policy text for the syllabus.
- [ ] Write the math primer page and the course notation table (see 'Audience and mathematical level' in `00_course_context.md`); add a math-background question to the survey.
- [ ] Leave a placeholder for the new Slack invite in the lecture notebook and `SoftwareSetupGuide.md`; fill it in once the workspace exists.

## Open decisions
- *(Decided: a new Slack workspace, created close to the semester once enrollment is mostly known.)* Remaining: confirm that the invite goes out with the pre-semester ICER email, and that the Week 1 lecture's Slack slide uses the new link.
- Students use their own ICER accounts; there is no class account. Before Jan 19:
  - every enrolled student must have an active ICER account (most MSU graduate students can request one themselves);
  - every student must be added to the `BMB_961_SS27_001` group.
  There is no fallback platform. Send the pre-semester email (ICER account request + Slack invite), collect NetIDs, and submit the group-membership request; repeat for late enrollees.
