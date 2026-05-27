"""Runtime dependency checks for profiling tools."""

from __future__ import annotations


def missing_runtime_dependencies() -> list[str]:
    """Return human-readable names of missing packages required for profiling."""
    missing: list[str] = []

    try:
        import pkg_resources  # noqa: F401
    except ModuleNotFoundError:
        missing.append("setuptools<82 (provides pkg_resources for ydata-profiling)")

    return missing


def dependency_install_hint() -> str:
    """Return install command for missing runtime dependencies."""
    return "pip install \"setuptools>=65.0.0,<82.0.0\""
