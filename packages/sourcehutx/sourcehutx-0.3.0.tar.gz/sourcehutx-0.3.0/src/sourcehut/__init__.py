# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

"""
Python API client for the Sourcehut API
"""

from __future__ import annotations

import os
import warnings

import pydantic

__version__ = "0.3.0"
__all__ = ("__version__",)


def _filter_pydantic_v2_warnings() -> None:
    """
    Filter DeprecationWarnings from Pydantic v2. We cannot fix these without
    dropping support for v1 entirely, and we don't want to break setups with
    PYTHONWARNINGS=error.
    """

    typ: type[DeprecationWarning] | None
    if typ := getattr(pydantic, "PydanticDeprecatedSince20", None):
        warnings.simplefilter(action="ignore", category=typ)


if "_SOURCEHUTX_SHOW_PYDANTIC_WARNINGS" not in os.environ:
    _filter_pydantic_v2_warnings()
