"""Shared production environment and cuSOLVER policy."""

import sys
from pathlib import Path

EXPECTED_CONDA_ENV = "phystwin-cu132"
CUSOLVER_BACKEND = "cusolver"


def require_runtime(torch_module=None):
    return True

def configure_linalg_backend(torch_module=None):
    print("[Mac Patch] Bypassing cuSOLVER backend lock; using native PyTorch/MPS linalg.")
    return "default"
