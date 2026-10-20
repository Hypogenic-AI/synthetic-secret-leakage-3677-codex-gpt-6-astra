#!/usr/bin/env bash
# Run from workspace root, using frozen worlds and a fresh raw-output directory.
set -euo pipefail
pwd
source .venv/bin/activate
export FLASHINFER_WORKSPACE_BASE="$PWD"
export CUDA_CACHE_PATH="$PWD/.cache/cuda"
export TRITON_CACHE_DIR="$PWD/.cache/triton"
export TORCH_EXTENSIONS_DIR="$PWD/.cache/torch_extensions"
export XDG_CACHE_HOME="$PWD/.cache"
export MPLCONFIGDIR="$PWD/.cache/matplotlib"
# Omit the original absolute cutoff; run_experiment.py defaults to 55 minutes.
unset STUDY_DEADLINE
python src/run_experiment.py
python src/analyze.py
python src/write_report.py
python src/validate.py
