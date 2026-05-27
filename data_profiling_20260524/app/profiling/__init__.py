"""Profiler factory and registry (lazy imports)."""

from __future__ import annotations

import importlib
from typing import Type

from app.profiling.base_profiler import BaseProfiler
from app.utils.constants import PROFILER_DIRS

# Lazy registry: import heavy libraries only when a profiler is actually used.
_PROFILER_SPECS: dict[str, tuple[str, str]] = {
    "ydata": ("app.profiling.ydata_profiler", "YDataProfiler"),
    "sweetviz": ("app.profiling.sweetviz_profiler", "SweetvizProfiler"),
    "great_expectations": ("app.profiling.great_expectations_profiler", "GreatExpectationsProfiler"),
}

_PROFILER_CACHE: dict[str, Type[BaseProfiler]] = {}


def _load_profiler_class(tool_key: str) -> Type[BaseProfiler]:
    """Import and cache a profiler class by tool key."""
    if tool_key in _PROFILER_CACHE:
        return _PROFILER_CACHE[tool_key]

    if tool_key not in _PROFILER_SPECS:
        raise ValueError(f"Unknown profiler: {tool_key}")

    module_path, class_name = _PROFILER_SPECS[tool_key]
    module = importlib.import_module(module_path)
    profiler_cls = getattr(module, class_name)
    _PROFILER_CACHE[tool_key] = profiler_cls
    return profiler_cls


def get_profiler(tool_key: str) -> BaseProfiler:
    """Instantiate a profiler adapter by tool key."""
    profiler_cls = _load_profiler_class(tool_key)
    return profiler_cls(PROFILER_DIRS[tool_key])


def list_available_profilers() -> list[str]:
    """Return list of registered profiler keys."""
    return list(_PROFILER_SPECS.keys())
