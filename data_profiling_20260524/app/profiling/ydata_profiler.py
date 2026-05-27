"""ydata-profiling adapter."""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from ydata_profiling import ProfileReport

from app.profiling.base_profiler import BaseProfiler, ProfilingMetrics, ProfilingResult


class YDataProfiler(BaseProfiler):
    """Adapter for ydata-profiling (formerly Pandas Profiling)."""

    tool_key = "ydata"
    tool_name = "ydata-profiling"

    def __init__(self, output_dir: Path) -> None:
        super().__init__(output_dir)
        self._profile: ProfileReport | None = None
        self._run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def run_profile(self, df: pd.DataFrame) -> ProfilingResult:
        """Run ydata-profiling and return standardized result."""
        self._df = df.copy()
        start = time.perf_counter()

        try:
            self._profile = ProfileReport(
                df,
                title=f"ydata-profiling Report — {self._run_id}",
                explorative=True,
                minimal=df.shape[0] > 5000,
            )
            report_path = self.generate_report()
            metrics = self.extract_metrics()
            self._runtime_seconds = time.perf_counter() - start
            metrics.runtime_seconds = round(self._runtime_seconds, 3)

            return ProfilingResult(
                metrics=metrics,
                report_html_path=report_path,
                json_path=self._json_path,
                raw_artifact=self._profile,
                success=True,
            )
        except Exception as exc:
            self._runtime_seconds = time.perf_counter() - start
            base = self._compute_base_metrics(df)
            error_metrics = ProfilingMetrics(
                tool_name=self.tool_name,
                runtime_seconds=round(self._runtime_seconds, 3),
                **{k: v for k, v in base.items() if k in ProfilingMetrics.__dataclass_fields__},
            )
            return ProfilingResult(
                metrics=error_metrics,
                success=False,
                error_message=str(exc),
            )

    def generate_report(self) -> Path | None:
        """Generate HTML and JSON summary reports."""
        if self._profile is None or self._df is None:
            return None

        html_path = self.output_dir / f"profile_{self._run_id}.html"
        json_path = self.output_dir / f"profile_{self._run_id}.json"

        self._profile.to_file(html_path)
        self._save_json_summary(json_path)

        self._report_path = html_path
        self._json_path = json_path
        return html_path

    def _save_json_summary(self, json_path: Path) -> None:
        """Save a lightweight JSON summary from the profile report."""
        if self._profile is None:
            return

        description = self._profile.get_description()
        summary: dict = {}

        if description is not None:
            if hasattr(description, "to_dict"):
                summary = description.to_dict()
            elif isinstance(description, dict):
                summary = description

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=str)

    def extract_metrics(self) -> ProfilingMetrics:
        """Extract standardized metrics from ydata-profiling output."""
        if self._df is None:
            raise ValueError("No dataset loaded. Call run_profile first.")

        base = self._compute_base_metrics(self._df)
        extra: dict = {}

        if self._profile is not None:
            description = self._profile.get_description()
            if description is not None:
                desc_dict = description.to_dict() if hasattr(description, "to_dict") else {}
                table_stats = desc_dict.get("table", {})
                extra = {
                    "n_duplicates": table_stats.get("n_duplicates"),
                    "n_cells_missing": table_stats.get("n_cells_missing"),
                    "memory_size_mb": table_stats.get("memory_size"),
                    "report_variables_count": len(desc_dict.get("variables", {})),
                }

        metrics = ProfilingMetrics(
            tool_name=self.tool_name,
            runtime_seconds=round(self._runtime_seconds, 3),
            report_path=str(self._report_path) if self._report_path else None,
            json_summary_path=str(self._json_path) if self._json_path else None,
            extra=extra,
            **{k: v for k, v in base.items() if k in ProfilingMetrics.__dataclass_fields__},
        )
        self._metrics = metrics
        return metrics
