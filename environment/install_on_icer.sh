#!/bin/bash
# Install the course environment once into the course research space (run by an instructor, on a dev node).
# UNTESTED ON ICER: written from the ICER docs and the local build. Read before running.
set -euo pipefail
SPACE=/mnt/research/BMB_961_SS27_001
newgrp_note="Run 'newgrp BMB_961_SS27_001' first so new files are group-owned."
[ "$(id -gn)" = "BMB_961_SS27_001" ] || { echo "$newgrp_note"; exit 1; }
umask 002
mkdir -p "$SPACE/env" "$SPACE/tools" && chmod g+rws "$SPACE/env" "$SPACE/tools"
export PIXI_HOME="$SPACE/tools/pixi"; export PATH="$PIXI_HOME/bin:$PATH"
if ! command -v pixi >/dev/null; then
  curl -fsSL https://pixi.sh/install.sh | PIXI_VERSION=v0.84.1 PIXI_HOME="$PIXI_HOME" bash   # lock was made with pixi 0.84.1
fi
cp pixi.toml pixi.lock check_environment.py "$SPACE/env/"
cd "$SPACE/env"
pixi install --frozen                      # exact versions from pixi.lock; ~13 GB
# Pre-fetch model weights into a shared cache so compute nodes (possibly offline) need no download.
export TORCH_HOME="$SPACE/cache/torch" XDG_DATA_HOME="$SPACE/cache/xdg" HF_HOME="$SPACE/cache/hf"
mkdir -p "$TORCH_HOME" "$XDG_DATA_HOME" "$HF_HOME"
# TODO (instructors): run the week-7 openmm-ml examples (ani2x, mace-off23-small) once with these variables set
# so the weights land in the shared cache; ANI2x and MACE-OFF download from GitHub on first use.
chmod -R g+rX "$SPACE/env" "$SPACE/cache" "$SPACE/tools"
echo "TORCH_HOME/XDG_DATA_HOME/HF_HOME must be exported in job scripts and OnDemand sessions too."
echo "Environment prefix for OnDemand: $SPACE/env/.pixi/envs/default"
pixi run --frozen python check_environment.py --gpu || echo "(--gpu check expected to fail on a node without GPU)"
