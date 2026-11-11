#!/bin/bash
#SBATCH --account=vermaaslab
#SBATCH --partition=general-short
#SBATCH --time=3:30:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --job-name=ml4md_install
#SBATCH --output=%x-%j.out
# Submit from the directory that holds install_on_icer.sh, pixi.toml, pixi.lock, check_environment.py.
cd "$SLURM_SUBMIT_DIR"
sg BMB_961_SS27_001 -c "bash $SLURM_SUBMIT_DIR/install_on_icer.sh"
