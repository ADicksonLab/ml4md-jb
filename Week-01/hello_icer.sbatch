#!/bin/bash --login
#SBATCH --job-name=ml4md_week1
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --output=%x-%j.out
# Lines starting with #SBATCH are requests to the scheduler: a 5-minute job on 1 node, 1 task, 2 CPUs, 4 GB of memory.
# There is no --account and no --partition line on purpose: your own login uses its default account,
# and ICER chooses the partition from your request.

# Start from a clean environment: ICER loads some modules for you by default, and they can interfere with the course environment.
module purge

ENV=/mnt/research/BMB_961_SS27_001/env/.pixi/envs/default     # the course environment

echo "job $SLURM_JOB_ID started $(date) on $(hostname)"
"$ENV/bin/python" numpy_benchmark.py
echo "job $SLURM_JOB_ID finished $(date)"
