# BMB 961 course environment (Spring 2027) — build notes

Replaces the 2022 pins (Python 3.7/3.8, `cudatoolkit=10.0`, `openmm=7.6`, `condacolab`, `module load CUDA/10.0.130`).
Files: `pixi.toml` (manifest), `pixi.lock` (exact versions, linux-64), `check_environment.py` (student/instructor check),
`install_on_icer.sh` + `install_job.sbatch` (research-space install, run on ICER 2026-11-11), `icer_tests/` (GPU and BioEmu2 test jobs), `boltz/` (separate environment).

## What was solved and tested (local workstation, RTX 3080 Ti, CUDA driver 580, Nov 11 2026)

| Package | Version | Source | Week(s) |
|---|---|---|---|
| Python | 3.12.16 | conda-forge | all |
| numpy / scipy | 2.4.6 / 1.18.1 | conda-forge | all |
| PyTorch | 2.12.1 (CUDA 12.9 build) | conda-forge | 4, 5, 7, 9, 10 |
| OpenMM | 8.5.2 | conda-forge | 2, 3, 6, 7 |
| openmm-ml / openmm-torch / NNPOps | 1.7 / 1.5.1 / 0.7 | conda-forge | 7 |
| TorchANI | 2.8.4 | conda-forge | 7 |
| MACE (`mace-torch`) / e3nn | 0.3.17 / 0.4.4 | PyPI | 7 |
| PyTorch Geometric | 2.8.1 | conda-forge | 5 (optional) |
| mdtraj / MDAnalysis | 1.11.2 / 2.11.0 | conda-forge | 1, 3, 8–10 |
| deeptime | 0.5.0 | conda-forge | 8 |
| NGLView / py3Dmol / ipymolstar | 4.0.1 / 2.5.4 / 0.1.0 | conda-forge, conda-forge, PyPI | 1, 9, 10 |
| JupyterLab / jupyterlab_rise | 4.6.6 / 0.43.1 | conda-forge | all |
| BioEmu2 | 0.1.0rc0 (git tag v0.1.0rc0) | GitHub | 8–10 |
| aSAM/aSAMt (`sam2`) | 1.0.0 (git, unpinned commit) | GitHub | 10 |
| cuEquivariance (CUDA 12 ops) | 0.11.1 | PyPI | BioEmu2 |

On-disk size of the built environment: about 13 GB. That argues for **one shared install in the research space**, not per-student builds.

Tests that passed (`check_environment.py --gpu`, 32/32; plus ad-hoc runs):
- imports of every package above;
- OpenMM CUDA, 1,503-atom water box, 4 fs steps with HMR: about 137–152 ns/day on the 3080 Ti (not an ICER number);
- `Simulation.runForClockTime` is present in OpenMM 8.5.2;
- openmm-ml energy evaluation on CUDA with ANI2x and MACE-OFF23-small (ethanol);
- torch autograd bond force matches −k(r − r0) = −20;
- deeptime MSM on a toy chain; cuEquivariance tensor-product kernel on GPU;
- JupyterLab lists `nglview-js-widgets` and `jupyterlab-rise` as enabled/OK;
- `bioemu2` and `sam2-generate-ensemble` CLIs start.

## Decisions forced by the dependency solve

1. **Boltz cannot share the core environment.** It pins numpy<2, scipy==1.13.1, biopython==1.84, numba==0.61.0; BioEmu2 needs biopython>=1.88. A separate environment (`boltz/`) solves; it was not built or run.
2. **CUDA 12 builds only.** BioEmu2's README says V100 (compute capability 7.0, the lab's buy-in nodes) needs its CUDA 12 install, because CUDA 13 dropped Volta. The environment therefore uses CUDA 12.9 conda builds and the `-cu12` cuEquivariance wheels.
3. **torch is capped below 2.14** (BioEmu2 constraint). `openmm-torch` currently drags the solve to torch 2.12.1 and OpenMM 8.5.2; without it the solver picks torch 2.13.0 and OpenMM 8.6.1. Re-check in December: if a newer `openmm-torch` build lands, OpenMM can move up.
4. **e3nn is installed by pip as MACE's pin (0.4.4)**, not from conda (0.6.0 conflicts).
5. **deeptime replaces PyEMMA** (as the Week 8 handoff says).
6. numpy is **2.x**; any 2022 notebook assuming numpy 1.x APIs needs a check.


## ICER results (2026-11-11, run as the instructor account)

- **Installed** at `/mnt/research/BMB_961_SS27_001/env/.pixi/envs/default` (pixi binary in `tools/pixi`, shared BioEmu2 weights in `cache/hf`; set `HF_HOME=/mnt/research/BMB_961_SS27_001/cache/hf`). Install job: 9.5 min on a compute node, ~16 GB and ~107k files on GPFS. All files group-owned (`BMB_961_SS27_001`), group read/write.
- `check_environment.py` passes on a CPU node; with `--gpu` on a V100S (driver 580.178.04, sm_70) and an A100 (driver 610.57.04, sm_80).
- V100S: OpenMM CUDA 1275 ns/day on a 6,282-atom water box (4 fs, HMR, mixed); checkpoint save/load OK; openmm-ml ANI2x and MACE-OFF23-small evaluate on GPU. (The ~140 ns/day local figure above came from a contended sandbox GPU; ignore it.)
- **BioEmu2 end-to-end on V100S:** `bioemu2 sample-equilibrium --pdb-id 1AKE` produced 8 conformations in 85 s; 8/8 passed its physicality checks.
- **cuEquivariance's own tensor-product kernel fails on V100** (compute capability 7.0; `cudaFuncSetAttribute` error) but passes on A100. BioEmu2 still runs on V100 and only logs missing tuning-cache warnings. `check_environment.py --gpu` will therefore report one FAIL on V100 nodes; this is expected.
- **Bug found and fixed:** conda-forge's Triton does not ship `cuda.h`, so BioEmu2 failed on any GPU at Triton's JIT step. Fixed by adding `cuda-cudart-dev` (lock changes only by 5 CUDA header packages). Commit 37f8e08 predates the fix.
- OnDemand launch was simulated on a dev node (`module purge; module load Miniforge3; conda activate <prefix>`): JupyterLab 4.6.6 started from the prefix, HTTP 200, kernel `python3`, NGLView and RISE extensions enabled. Not yet tried through the OnDemand web form. In an interactive dev-node shell a loaded `Python` module blocks `module load Miniforge3`; OnDemand should start clean.
- Gotchas: the default ICER login shell loads a cURL module whose libraries break `curl` on some node types (installer purges modules); `sbatch` is shadowed on the gateway (submit via a dev node).
- Still open: A100 BioEmu2 run (queued at time of writing), browser check of NGLView and MathJax, the Boltz environment, and the aSAM weights test.

## Remaining risks (partly superseded by the ICER results above)

- **ICER itself.** No ICER access from here. Not verified: GPU driver version on class-eligible nodes (CUDA 12.9 builds need a recent driver, or CUDA minor-version compatibility), that `pixi` can be installed on the dev nodes, and that OnDemand accepts a pixi prefix. The ICER docs describe OnDemand Jupyter with "Conda Environment using Miniforge3 module" and a path such as `$RESEARCH_SPACE/envs/<name>`; the prefix here would be `/mnt/research/BMB_961_SS27_001/env/.pixi/envs/default`. If OnDemand rejects it, fallbacks: `conda create -p` from an exported spec, or a kernelspec with the "Default" location (then NGLView/RISE extensions would NOT load, because they must live in the Jupyter server environment).
- **Browser rendering.** NGLView 4.0.1 has a known frontend-version bug and `jupyterlab-mathjax3` is flagged "X" (version-range warning) by `jupyter labextension list`. Open a notebook with NGLView, an equation cell, and RISE in a real browser session; equations matter for this course.
- **BioEmu2 and aSAM sampling.** Only imports and CLI help were tested. Weights come from Hugging Face / Zenodo; not downloaded here. Run one `predict-structure` and one `sam2-generate-ensemble` on an ICER GPU.
- **Offline compute nodes.** ANI2x and MACE-OFF weights download from GitHub on first use; pre-populate a shared cache (see the TODO in `install_on_icer.sh`).
- **sam2 is installed from the default branch** (no tag exists besides data/zenodo tags); pin a commit hash before the semester. `pixi.lock` records the commit solved today.
- **Only linux-64 is locked.** Instructors presenting from a laptop (the RISE question in `00_course_context.md`) would need `osx-arm64`; BioEmu2 and CUDA parts will not work there.
- Sandbox note: OpenMP aborted on thread affinity here; I set `KMP_AFFINITY=disabled`. Unlikely to matter on ICER.
- AmberTools components pulled in by `openmmforcefields` trigger `pip check` warnings (e.g., `proprep` wants numpy<2). They are not imported by course code.

## Next steps
1. Instructors: `newgrp BMB_961_SS27_001`, then run `install_on_icer.sh` on a dev node once accounts are live.
2. Launch OnDemand with the prefix above and run `check_environment.py --gpu` on a V100 and on another GPU type.
3. Browser test (NGLView, MathJax, RISE).
4. December: re-solve (`pixi update`), re-run the check, tag a release of the lock.
