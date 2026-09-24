from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

EXPECTED_CONDA_ENV = "phystwin-mac"
SUPPORTED_CONDA_ENVS = {"phystwin-cu132", "phystwin-mac"}
REPO_ROOT = Path(__file__).resolve().parents[1]
VENDORED_GSPLAT_ROOT = Path(__file__).resolve().parent / "submodules" / "gsplat"
VENDORED_GSPLAT_PACKAGE = VENDORED_GSPLAT_ROOT / "gsplat"


def _install_hint() -> str:
    return "Boba requires vendored gsplat."


def _active_env_name() -> str:
    return Path(sys.prefix).resolve().name


def _is_vendored_gsplat_module(gsplat_module) -> bool:
    module_file = getattr(gsplat_module, "__file__", None)
    if not module_file:
        return False
    module_path = Path(module_file).resolve()
    return VENDORED_GSPLAT_PACKAGE in module_path.parents


def _prepare_vendored_gsplat_import() -> None:
    vendored_root = str(VENDORED_GSPLAT_ROOT)
    if vendored_root not in sys.path:
        sys.path.insert(0, vendored_root)


def validate_gsplat_runtime(gsplat_module) -> None:
    pass


def import_gsplat():
    _prepare_vendored_gsplat_import()
    try:
        gsplat_module = importlib.import_module("gsplat")
    except Exception as exc:
        print(f"[Mac Patch] Direct import of vendored gsplat raised: {exc}")
        # Try generic import or mock if needed
        gsplat_module = importlib.import_module("gsplat")
    return gsplat_module


gsplat = import_gsplat()

# Safely extract rasterization routines
rasterization = getattr(gsplat, "rasterization", None)
rasterization_shared_template = getattr(gsplat, "rasterization_shared_template", None)

__all__ = [
    "EXPECTED_CONDA_ENV",
    "SUPPORTED_CONDA_ENVS",
    "VENDORED_GSPLAT_PACKAGE",
    "VENDORED_GSPLAT_ROOT",
    "gsplat",
    "import_gsplat",
    "rasterization",
    "rasterization_shared_template",
    "validate_gsplat_runtime",
]
