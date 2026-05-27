"""Python version compatibility helpers."""

from __future__ import annotations

import sys

MIN_PYTHON = (3, 10)
MAX_PYTHON = (3, 14)  # exclusive upper bound (3.13.x is OK, 3.14+ is not)


def is_supported_python() -> bool:
    """Return True if the current interpreter is within the supported range."""
    return MIN_PYTHON <= sys.version_info[:2] < MAX_PYTHON


def python_version_label() -> str:
    """Return a human-readable Python version string."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def supported_range_label() -> str:
    """Return the supported Python version range as text."""
    return "3.10 – 3.13"


def compatibility_message() -> str | None:
    """Return a warning message when Python is unsupported, else None."""
    if is_supported_python():
        return None

    current = python_version_label()
    if sys.version_info[:2] >= MAX_PYTHON:
        return (
            f"Python {current} is not supported. "
            f"Profiling libraries require Python {supported_range_label()}. "
            "Create a virtual environment with a supported Python version, then reinstall dependencies."
        )

    return (
        f"Python {current} is not supported. "
        f"Please use Python {supported_range_label()}."
    )
