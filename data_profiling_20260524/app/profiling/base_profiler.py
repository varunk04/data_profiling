"""Abstract base class for profiling tool adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

from app.profiling.metrics import compute_base_metrics


@dataclass
class ProfilingMetrics:
    """Standardized metrics returned by all profilers."""

    tool_name: str
    runtime_seconds: float
    row_count: int
    column_count: int
    missing_values_total: int
    missing_percentage: float
    duplicate_rows: int
    column_dtypes: dict[str, str]
    null_percentage_by_column: dict[str, float]
    outlier_counts: dict[str, int] = field(default_factory=dict)
    correlation_insights: dict[str, Any] = field(default_factory=dict)
    numeric_column_count: int = 0
    categorical_column_count: int = 0
    datetime_column_count: int = 0
    report_path: str | None = None
    json_summary_path: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to a serializable dictionary."""
        return {
            "tool_name": self.tool_name,
            "runtime_seconds": self.runtime_seconds,
            "row_count": self.row_count,
            "column_count": self.column_count,
            "missing_values_total": self.missing_values_total,
            "missing_percentage": self.missing_percentage,
            "duplicate_rows": self.duplicate_rows,
            "column_dtypes": self.column_dtypes,
            "null_percentage_by_column": self.null_percentage_by_column,
            "outlier_counts": self.outlier_counts,
            "correlation_insights": self.correlation_insights,
            "numeric_column_count": self.numeric_column_count,
            "categorical_column_count": self.categorical_column_count,
            "datetime_column_count": self.datetime_column_count,
            "report_path": self.report_path,
            "json_summary_path": self.json_summary_path,
            "extra": self.extra,
        }


@dataclass
class ProfilingResult:
    """Complete result from a profiling run."""

    metrics: ProfilingMetrics
    report_html_path: Path | None = None
    json_path: Path | None = None
    raw_artifact: Any = None
    success: bool = True
    error_message: str | None = None


class BaseProfiler(ABC):
    """Common interface for all profiling tool adapters."""

    tool_key: str = "base"
    tool_name: str = "Base Profiler"

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._df: pd.DataFrame | None = None
        self._metrics: ProfilingMetrics | None = None
        self._report_path: Path | None = None
        self._json_path: Path | None = None
        self._runtime_seconds: float = 0.0

    @abstractmethod
    def run_profile(self, df: pd.DataFrame) -> ProfilingResult:
        """Execute profiling on the given DataFrame."""
        pass

    @abstractmethod
    def generate_report(self) -> Path | None:
        """Generate and save the profiling report."""
        pass

    @abstractmethod
    def extract_metrics(self) -> ProfilingMetrics:
        """Extract standardized metrics from profiling output."""
        pass

    def _compute_base_metrics(self, df: pd.DataFrame) -> dict[str, Any]:
        """Compute common metrics shared across all profilers."""
        return compute_base_metrics(df)
