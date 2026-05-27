"""Comparison engine for profiling tool evaluation."""

from __future__ import annotations

from typing import Any

import pandas as pd

from app.profiling.base_profiler import ProfilingResult


class ComparisonEngine:
    """Compare profiling outputs across multiple tools."""

    TOOL_SCORES: dict[str, dict[str, float]] = {
        "ydata": {
            "visualization_quality": 9.0,
            "ease_of_interpretation": 8.5,
            "report_completeness": 9.5,
            "usability": 8.0,
        },
        "sweetviz": {
            "visualization_quality": 9.5,
            "ease_of_interpretation": 9.0,
            "report_completeness": 8.0,
            "usability": 8.5,
        },
        "great_expectations": {
            "visualization_quality": 6.5,
            "ease_of_interpretation": 7.0,
            "report_completeness": 8.0,
            "usability": 6.5,
        },
    }

    def compare(self, results: dict[str, ProfilingResult]) -> dict[str, Any]:
        """Build comparative analysis from profiling results."""
        successful = {k: v for k, v in results.items() if v.success}
        metrics_rows = []
        score_rows = []

        runtimes = [r.metrics.runtime_seconds for r in successful.values()]
        min_runtime = min(runtimes) if runtimes else 1.0

        for tool_key, result in results.items():
            m = result.metrics
            total_outliers = sum(m.outlier_counts.values()) if m.outlier_counts else 0

            metrics_rows.append(
                {
                    "tool": m.tool_name,
                    "tool_key": tool_key,
                    "success": result.success,
                    "runtime_seconds": m.runtime_seconds,
                    "missing_values": m.missing_values_total,
                    "missing_pct": m.missing_percentage,
                    "duplicates": m.duplicate_rows,
                    "outliers": total_outliers,
                    "numeric_cols": m.numeric_column_count,
                    "categorical_cols": m.categorical_column_count,
                    "strong_correlations": m.correlation_insights.get("strong_correlations_count", 0),
                }
            )

            if result.success:
                scores = self._score_tool(tool_key, result, min_runtime)
                score_rows.append({"tool": m.tool_name, "tool_key": tool_key, **scores})

        metrics_df = pd.DataFrame(metrics_rows)
        scores_df = pd.DataFrame(score_rows) if score_rows else pd.DataFrame()

        summary = self._build_summary(metrics_df, scores_df)

        return {
            "metrics_table": metrics_df,
            "scores_table": scores_df,
            "summary": summary,
            "tool_count": len(results),
            "successful_count": len(successful),
        }

    def _score_tool(self, tool_key: str, result: ProfilingResult, min_runtime: float) -> dict[str, float]:
        """Compute evaluation scores for a tool."""
        m = result.metrics
        base_scores = self.TOOL_SCORES.get(tool_key, {})

        runtime_score = min(10.0, round((min_runtime / max(m.runtime_seconds, 0.001)) * 8, 1))
        missing_score = 10.0 if m.missing_values_total >= 0 else 5.0
        duplicate_score = 10.0 if m.duplicate_rows >= 0 else 5.0
        outlier_score = 8.0 if m.outlier_counts else 6.0

        return {
            "missing_value_detection": missing_score,
            "duplicate_detection": duplicate_score,
            "outlier_detection": outlier_score,
            "visualization_quality": base_scores.get("visualization_quality", 7.0),
            "ease_of_interpretation": base_scores.get("ease_of_interpretation", 7.0),
            "runtime_performance": runtime_score,
            "report_completeness": base_scores.get("report_completeness", 7.0),
            "usability": base_scores.get("usability", 7.0),
            "overall_score": round(
                (
                    missing_score
                    + duplicate_score
                    + outlier_score
                    + base_scores.get("visualization_quality", 7.0)
                    + base_scores.get("ease_of_interpretation", 7.0)
                    + runtime_score
                    + base_scores.get("report_completeness", 7.0)
                    + base_scores.get("usability", 7.0)
                )
                / 8,
                2,
            ),
        }

    def _build_summary(self, metrics_df: pd.DataFrame, scores_df: pd.DataFrame) -> dict[str, Any]:
        """Build aggregated comparison summary."""
        if metrics_df.empty:
            return {"message": "No profiling results to compare."}

        fastest = metrics_df.loc[metrics_df["runtime_seconds"].idxmin()] if len(metrics_df) else None
        summary: dict[str, Any] = {
            "fastest_tool": fastest["tool"] if fastest is not None else None,
            "fastest_runtime": fastest["runtime_seconds"] if fastest is not None else None,
        }

        if not scores_df.empty and "overall_score" in scores_df.columns:
            best = scores_df.loc[scores_df["overall_score"].idxmax()]
            summary["highest_rated_tool"] = best["tool"]
            summary["highest_overall_score"] = best["overall_score"]

        return summary
