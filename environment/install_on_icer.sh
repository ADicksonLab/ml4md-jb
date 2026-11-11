#!/bin/bash
# Install the course environment once into the course research space (instructor, on ICER).
# Run it inside a Slurm job (see install_job.sbatch) under the course group:
#   sbatch install_job.sbatch        # which runs:  sg BMB_961_SS27_001 -c "bash install_on_icer.sh"
set -euo pipefail
# ICER login shells load a cURL module whose libs clash with system curl on some node types: start clean.
command -v module >/dev/null 2>&1 && module purge >/dev/null 2>&1 || true
unset LD_LIBRARY_PATH LIBRARY_PATH CPATH
export PATH=/usr/local/bin:/usr/bin:/bin
SPACE=/mnt/research/BMB_961_SS27_001
HERE=$(cd "$(dirname "$0")" && pwd)
[ "$(id -gn)" = "BMB_961_SS27_001" ] || { echo "Run under the course group: sg BMB_961_SS27_001 -c 'bash $0'"; exit 1; }
umask 002                                         # group-writable, setgid dirs keep the group
mkdir -p "$SPACE/env" "$SPACE/tools"
export PIXI_HOME="$SPACE/tools/pixi"              # pixi binary lives in the space
export PATH="$PIXI_HOME/bin:$PATH"
# Caches go to scratch, NOT home (home is near its file-count quota) and not the research space.
CACHE=${SCRATCH_CACHE:-/mnt/gs21/scratch/$USER/ml4md_cache}
mkdir -p "$CACHE"; export RATTLER_CACHE_DIR="$CACHE/rattler" UV_CACHE_DIR="$CACHE/uv" PIP_CACHE_DIR="$CACHE/pip"
export CONDA_OVERRIDE_CUDA=12                     # CPU-only build node: satisfy the __cuda virtual package
export PIXI_NO_PATH_UPDATE=1                      # do not edit ~/.bashrc
if ! command -v pixi >/dev/null; then
  mkdir -p "$PIXI_HOME/bin"
  /usr/bin/curl -fsSL https://github.com/prefix-dev/pixi/releases/download/v0.84.1/pixi-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C "$PIXI_HOME/bin"                   # lock was made with pixi 0.84.1
fi
pixi --version
cp "$HERE/pixi.toml" "$HERE/pixi.lock" "$HERE/check_environment.py" "$SPACE/env/"
cd "$SPACE/env"
pixi install --frozen                              # exact versions from pixi.lock; ~13 GB
PY="$SPACE/env/.pixi/envs/default/bin/python"
KMP_AFFINITY=disabled "$PY" check_environment.py   # CPU checks; GPU checks run later on a GPU node (--gpu)
du -sh "$SPACE/env/.pixi" || true
echo "Environment prefix for OnDemand: $SPACE/env/.pixi/envs/default"
