"""Great Expectations adapter."""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from app.profiling.base_profiler import BaseProfiler, ProfilingMetrics, ProfilingResult


class GreatExpectationsProfiler(BaseProfiler):
    """Adapter for Great Expectations validation suite."""

    tool_key = "great_expectations"
    tool_name = "Great Expectations"

    def __init__(self, output_dir: Path) -> None:
        super().__init__(output_dir)
        self._run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._validation_result: dict | None = None

    def run_profile(self, df: pd.DataFrame) -> ProfilingResult:
        """Run Great Expectations profiling and return standardized result."""
        self._df = df.copy()
        start = time.perf_counter()

        try:
            report_path = self.generate_report()
            metrics = self.extract_metrics()
            self._runtime_seconds = time.perf_counter() - start
            metrics.runtime_seconds = round(self._runtime_seconds, 3)

            return ProfilingResult(
                metrics=metrics,
                report_html_path=report_path,
                json_path=self._json_path,
                raw_artifact=self._validation_result,
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
        """Generate HTML and JSON validation reports."""
        if self._df is None:
            return None

        html_path = self.output_dir / f"profile_{self._run_id}.html"
        json_path = self.output_dir / f"profile_{self._run_id}.json"

        results = self._run_expectations()
        success_count = sum(1 for r in results if r.get("success"))

        self._validation_result = {
            "expectations_run": len(results),
            "expectations_passed": success_count,
            "success_rate": round(success_count / len(results) * 100, 2) if results else 0,
            "results": results,
        }

        self._save_json_summary(json_path)
        self._generate_html_report(html_path)

        self._report_path = html_path
        self._json_path = json_path
        return html_path

    def _run_expectations(self) -> list[dict]:
        """Run validation expectations using GE when available, else pandas checks."""
        if self._df is None:
            return []

        try:
            from great_expectations.dataset import PandasDataset

            dataset = PandasDataset(self._df)
            expectations = [
                dataset.expect_table_row_count_to_be_between(
                    min_value=1, max_value=max(len(self._df), 1)
                ),
                dataset.expect_table_columns_to_match_ordered_list(self._df.columns.tolist()),
            ]
            for col in self._df.columns:
                null_pct = self._df[col].isnull().mean()
                expectations.append(
                    dataset.expect_column_values_to_not_be_null(
                        col, mostly=max(0.0, 1.0 - null_pct - 0.01)
                    )
                )
            results = []
            for exp in expectations:
                if hasattr(exp, "to_json_dict"):
                    results.append(exp.to_json_dict())
                else:
                    results.append({"success": getattr(exp, "success", False)})
            return results
        except Exception:
            return self._run_pandas_expectations()

    def _run_pandas_expectations(self) -> list[dict]:
        """Fallback expectation checks using pandas when GE API is unavailable."""
        if self._df is None:
            return []

        results: list[dict] = []
        row_count = len(self._df)
        results.append(
            {
                "expectation_type": "expect_table_row_count_to_be_between",
                "success": row_count >= 1,
                "result": {"observed_value": row_count},
            }
        )
        results.append(
            {
                "expectation_type": "expect_table_columns_to_match_ordered_list",
                "success": len(self._df.columns) > 0,
                "result": {"observed_value": list(self._df.columns)},
            }
        )
        for col in self._df.columns:
            null_pct = self._df[col].isnull().mean()
            results.append(
                {
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "column": col,
                    "success": null_pct < 1.0,
                    "result": {"null_percentage": round(null_pct * 100, 2)},
                }
            )
        return results

    def _save_json_summary(self, json_path: Path) -> None:
        """Save validation results as JSON."""
        if self._validation_result is None:
            return

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self._validation_result, f, indent=2, default=str)

    def _generate_html_report(self, html_path: Path) -> None:
        """Generate a simple HTML summary report."""
        if self._validation_result is None or self._df is None:
            return

        base = self._compute_base_metrics(self._df)
        vr = self._validation_result

        rows = ""
        skip_keys = {"column_dtypes", "null_percentage_by_column", "outlier_counts", "correlation_insights"}
        for key, value in base.items():
            if key not in skip_keys:
                rows += f"<tr><td>{key}</td><td>{value}</td></tr>"

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Great Expectations Report — {self._run_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
        h1 {{ color: #1a5276; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #1a5276; color: white; }}
        .success {{ color: #27ae60; font-weight: bold; }}
        .metric {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>Great Expectations Validation Report</h1>
    <p>Run ID: {self._run_id}</p>
    <div class="metric">
        <p><strong>Expectations Run:</strong> {vr['expectations_run']}</p>
        <p><strong>Passed:</strong> <span class="success">{vr['expectations_passed']}</span></p>
        <p><strong>Success Rate:</strong> {vr['success_rate']}%</p>
    </div>
    <h2>Dataset Summary</h2>
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        {rows}
    </table>
</body>
</html>"""

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def extract_metrics(self) -> ProfilingMetrics:
        """Extract standardized metrics from Great Expectations output."""
        if self._df is None:
            raise ValueError("No dataset loaded. Call run_profile first.")

        base = self._compute_base_metrics(self._df)
        extra = self._validation_result or {}

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
