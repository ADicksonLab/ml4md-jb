#!/bin/bash
#SBATCH --partition=general-short
#SBATCH --time=0:30:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --gres=gpu:1
#SBATCH --job-name=ml4md_gputest
#SBATCH --output=%x-%j.out
module purge >/dev/null 2>&1; unset LD_LIBRARY_PATH
P=/mnt/research/BMB_961_SS27_001/env/.pixi/envs/default
export PATH=$P/bin:/usr/bin:/bin KMP_AFFINITY=disabled
export TORCH_HOME=$SLURM_SUBMIT_DIR/cache/torch XDG_DATA_HOME=$SLURM_SUBMIT_DIR/cache/xdg
hostname; nvidia-smi --query-gpu=name,driver_version,compute_cap --format=csv,noheader
cd $SLURM_SUBMIT_DIR
python check_environment.py --gpu 2>&1 | grep -E "FAIL|PASS  (GPU|cuEq)|CHECK"
python gpu_bench.py 2>&1 | grep -E "GPU:|OpenMM|checkpoint|openmm-ml|Error|Traceback"
