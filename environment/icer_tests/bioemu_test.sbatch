#!/bin/bash
#SBATCH --account=vermaaslab
#SBATCH --partition=general-short
#SBATCH --time=0:40:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=24G
#SBATCH --gres=gpu:1
#SBATCH --job-name=ml4md_bioemu
#SBATCH --output=%x-%j.out
module purge >/dev/null 2>&1; unset LD_LIBRARY_PATH
P=/mnt/research/BMB_961_SS27_001/env/.pixi/envs/default
export PATH=$P/bin:/usr/bin:/bin KMP_AFFINITY=disabled
export HF_HOME=$SLURM_SUBMIT_DIR/cache/hf
cd $SLURM_SUBMIT_DIR; mkdir -p out
hostname; nvidia-smi --query-gpu=name,compute_cap --format=csv,noheader
OUT=out/adk_$SLURM_JOB_ID
time bioemu2 sample-equilibrium --pdb-id 1AKE --out $OUT 2>&1 | tail -25
ls -la $OUT; du -sh $HF_HOME
python - <<PY
import mdtraj as md
t = md.load("$OUT/samples.xtc", top="$OUT/topology.cif")
print("BIOEMU_OK frames", t.n_frames, "atoms", t.n_atoms)
PY
