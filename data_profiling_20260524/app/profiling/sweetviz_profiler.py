"""Sweetviz adapter."""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import sweetviz as sv

from app.profiling.base_profiler import BaseProfiler, ProfilingMetrics, ProfilingResult


class SweetvizProfiler(BaseProfiler):
    """Adapter for Sweetviz EDA reports."""

    tool_key = "sweetviz"
    tool_name = "Sweetviz"

    def __init__(self, output_dir: Path) -> None:
        super().__init__(output_dir)
        self._report: sv.DataframeReport | None = None
        self._run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def run_profile(self, df: pd.DataFrame) -> ProfilingResult:
        """Run Sweetviz profiling and return standardized result."""
        self._df = df.copy()
        start = time.perf_counter()

        try:
            self._report = sv.analyze(df)
            report_path = self.generate_report()
            metrics = self.extract_metrics()
            self._runtime_seconds = time.perf_counter() - start
            metrics.runtime_seconds = round(self._runtime_seconds, 3)

            return ProfilingResult(
                metrics=metrics,
                report_html_path=report_path,
                json_path=self._json_path,
                raw_artifact=self._report,
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
        """Generate HTML report and JSON summary."""
        if self._report is None:
            return None

        html_path = self.output_dir / f"profile_{self._run_id}.html"
        json_path = self.output_dir / f"profile_{self._run_id}.json"

        self._report.show_html(filepath=str(html_path), open_browser=False)
        self._save_json_summary(json_path)

        self._report_path = html_path
        self._json_path = json_path
        return html_path

    def _save_json_summary(self, json_path: Path) -> None:
        """Save a JSON summary of Sweetviz metrics."""
        if self._df is None:
            return

        base = self._compute_base_metrics(self._df)
        summary = {
            "tool": self.tool_name,
            "run_id": self._run_id,
            "metrics": {k: v for k, v in base.items()},
            "feature_count": self._df.shape[1],
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=str)

    def extract_metrics(self) -> ProfilingMetrics:
        """Extract standardized metrics from Sweetviz output."""
        if self._df is None:
            raise ValueError("No dataset loaded. Call run_profile first.")

        base = self._compute_base_metrics(self._df)
        extra = {
            "visual_eda": True,
            "pairwise_analysis": self._df.shape[1] >= 2,
            "feature_count": self._df.shape[1],
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
