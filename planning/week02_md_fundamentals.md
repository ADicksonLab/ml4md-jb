# Week 2 — How molecular simulation works
**Tue Jan 26 / Thu Jan 28**

> Handoff document for a dedicated planning thread. Read `planning/00_course_context.md` first; it covers rooms, dates, the AI-era design principle, the ICER campaign and environment conventions.

## Role in the course
- **Builds on:** Week 1 numpy skills.
- **Sets up:**
  - Week 3: many-particle simulation reuses the integrators and thermostats written here.
  - Week 4: the autograd example computes forces as −∇U.
  - Week 6: OpenMM force groups map onto the force-field terms.
  - Week 7: ML force fields replace U.

## Learning objectives
1. State F = ma with F = −∇U, and derive analytic forces for each classical force-field term.
2. Write out and explain the functional forms of a CHARMM/AMBER-type force field:
   - bonds, angles (+ Urey–Bradley), periodic dihedrals, impropers, CMAP;
   - LJ with combining rules, Coulomb;
   - exclusions and 1–4 scaling.
   Explain where the parameters come from.
3. Compare integrators (explicit Euler, velocity Verlet, leapfrog, adaptive RK45) on accuracy, energy conservation, time reversibility and cost.
4. Explain why symplectic integrators are used for MD even though RK45 is more accurate over short times.
5. Implement and compare thermostats, and identify which ones sample the canonical ensemble.

## 2022 source material
- `Week-06/W6_Lecture_MD-Concepts1.ipynb`: Hamiltonian, net forces, intuition for dU/dx, Euler vs. velocity Verlet, reversibility, chaos, Langevin, NVE vs. NVT. Most of it reusable.
- `Week-06/W6_Lab_Single-Particle-Langevin-Dynamics(-SOLUTIONS).ipynb`: potential, `vv_langevin`, `sim_manager`, free-energy plots, temperature dependence. Reusable as the base.
- `Week-07/W7_Lecture_MD-Concepts2.ipynb`:
  - Reusable: temperature as kinetic energy, Maxwell–Boltzmann, `init_vel`, thermostat overview (Berendsen/Andersen/Nosé–Hoover named only), force-field equations, coded LJ (`ulj`). Move the force-field section here.
  - Leave for Week 3: PBC (`apply_pbc`, `shortest_disp_vector`).
- `unsorted/HamiltonianMechanics-STUDENT.ipynb`: timestep-error exercise with Euler and velocity Verlet. Reuse in the integrator section.
- **New material needed:** leapfrog, RK45 via `scipy.integrate.solve_ivp`, code for each bonded term and Coulomb with analytic forces, additional thermostats (velocity rescaling, Berendsen, Andersen, Bussi/CSVR, optionally Nosé–Hoover; BAOAB Langevin).

## Math support (see audience conventions in `00_course_context.md`)
This week has the densest calculus in the course.
- **Bonds:** write F = −dU/dx for a 1-D spring first, then the 3-D bond force using the chain rule in explicit steps:
  1. U(r);
  2. r = |**r**_i − **r**_j|;
  3. dU/dr;
  4. ∂r/∂x_i = (x_i − x_j)/r.
  Write the x, y, z components separately.
- **Angles:** give the force result and verify it numerically.
- **Dihedrals and CMAP:** give the force result only, and verify it numerically. The Match-OpenMM lab already enforces this verification.
- **Integrators:** introduce them as "position after a small time step ≈ position now + velocity × Δt + …". Show the Taylor expansion term by term, with one worked numerical step of Euler and one of velocity Verlet on a harmonic oscillator, by hand.
- **Thermostats:**
  - Maxwell–Boltzmann: plot the distribution before writing it, then name every factor.
  - Langevin: explain the random force as "random kicks whose size is set by temperature and friction", before the fluctuation–dissipation formula.

## Lecture ideas (50 min)
- Build U for a small molecule one term at a time on screen. Butane, or the alanine dipeptide used later, works well. Show the energy landscape that each term adds.
- Introduce force-field parameterization in one slide (QM targets, condensed-phase properties). This sets up Week 7.
- Integrators: show the RK45 vs. Verlet energy-drift plot as a puzzle before explaining shadow Hamiltonians and symplecticity.

## Lab ideas (2 h)
1. **"Match OpenMM" force-field challenge (central activity).**
   - Instructors provide a small molecule with its parameters and the per-term energies and forces from OpenMM force groups, precomputed so students need no OpenMM yet.
   - Students implement each term in numpy and must match the energies (and forces, to a stated tolerance) term by term.
   - Forces are checked against finite differences of their own U.
   - The reference makes correctness objective: an assistant can write the code, but students must debug it until it matches, and they learn the unit and convention details (degrees vs. radians, 1–4 scaling, kcal vs. kJ) in the process.
2. **Integrator tournament.**
   - Same potential (1-D double well or harmonic bond), four integrators.
   - Required plots: energy drift vs. time; drift vs. dt (log–log, showing dt² for Verlet); force calls per unit simulated time.
   - Challenge: the largest dt that keeps energy bounded for 10⁶ steps.
   - Judgment question: "Your advisor suggests RK45 because it is more accurate. Respond."
3. **"Spot the fake ensemble."**
   - Students receive kinetic-energy histograms (or raw velocity samples) from five unlabelled thermostats on the same system.
   - Using the Maxwell–Boltzmann / canonical KE distribution, they identify which samples NVT correctly and which (Berendsen, plain velocity rescaling) give the right mean but the wrong fluctuations.
   - Then they implement two thermostats and confirm their own diagnosis.

## AI-audit notebook (seeded bugs)
- Leapfrog velocities reported at the integer step instead of the half step, so the energy looks wrong.
- Force sign error in one term; it shows up only as slow heating.
- Dihedral implemented in degrees inside `cos()`.
- Berendsen documented as "samples the canonical ensemble".

## Prediction prompts
- Before the dt sweep: "Which integrator fails first, and how will the failure look?"
- Before the thermostat histograms: "Which thermostat will give the narrowest KE distribution?"

## Deliverables and grading
- Match-OpenMM table (pass/fail per term within tolerance).
- Integrator plots + written judgment answer.
- Thermostat diagnosis with justification.
- AI-audit findings.
- Oral check-off: explain the drift-vs-dt plot.

## Build tasks for this thread
- [ ] Choose the molecule and generate reference energies and forces per force group with OpenMM 8 (script kept for reproducibility).
- [ ] Merge the force-field section of the 2022 Week 7 lecture into a new Week 2 lecture, along with the 2022 Week 6 integrator material.
- [ ] Write the lab, solutions and AI-audit notebooks.
- [ ] Generate the thermostat histograms.
- [ ] Rubric.

## Open decisions
- Week 2 content is large. Compressing MD fundamentals into one week (PBC moved into this lecture, argon as homework) would free a content week; the assessment lists this as an open question.
- Molecule for Match-OpenMM: butane (simple, no CMAP) or alanine dipeptide (CMAP, reused in Weeks 4 and 10)?
