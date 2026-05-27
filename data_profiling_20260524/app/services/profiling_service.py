"""Orchestrates profiling runs across multiple tools."""

from __future__ import annotations

from datetime import datetime
from typing import Callable

import pandas as pd

from app.comparison.comparison_engine import ComparisonEngine
from app.profiling import get_profiler
from app.profiling.base_profiler import ProfilingMetrics, ProfilingResult
from app.profiling.metrics import compute_base_metrics
from app.utils.constants import AVAILABLE_PROFILERS


class ProfilingService:
    """Service layer for running and comparing profilers."""

    def __init__(self) -> None:
        self.comparison_engine = ComparisonEngine()

    def run_profilers(
        self,
        df: pd.DataFrame,
        tool_keys: list[str],
        progress_callback: Callable[[str, str], None] | None = None,
    ) -> dict[str, ProfilingResult]:
        """Run selected profilers on the dataset."""
        results: dict[str, ProfilingResult] = {}

        for tool_key in tool_keys:
            if progress_callback:
                progress_callback(tool_key, "running")

            try:
                profiler = get_profiler(tool_key)
                result = profiler.run_profile(df)
                results[tool_key] = result
                status = "success" if result.success else "failed"
            except Exception as exc:
                tool_name = AVAILABLE_PROFILERS[tool_key]["name"]
                base = compute_base_metrics(df)
                error_metrics = ProfilingMetrics(
                    tool_name=tool_name,
                    runtime_seconds=0.0,
                    **{k: v for k, v in base.items() if k in ProfilingMetrics.__dataclass_fields__},
                )
                results[tool_key] = ProfilingResult(
                    metrics=error_metrics,
                    success=False,
                    error_message=str(exc),
                )
                status = "failed"

            if progress_callback:
                progress_callback(tool_key, status)

        return results

    def compare_results(self, results: dict[str, ProfilingResult]) -> dict:
        """Run comparative analysis on profiling results."""
        return self.comparison_engine.compare(results)

    @staticmethod
    def timestamp() -> str:
        """Return current run timestamp string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
