Separate environment for Boltz (week 9 option). Boltz 2.2.1 hard-pins numpy<2, scipy==1.13.1,
biopython==1.84 and numba==0.61.0, which conflict with the core environment (BioEmu2 needs
biopython>=1.88; numpy is 2.4 there). Solved but NOT built or run here (only `pixi lock`).
Use it as a batch-job tool: `pixi run --manifest-path boltz/pixi.toml boltz predict ...`
