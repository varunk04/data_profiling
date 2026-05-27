"""Metrics normalization utilities for export."""

from __future__ import annotations

import pandas as pd

from app.profiling.base_profiler import ProfilingResult


def metrics_to_csv_rows(results: dict[str, ProfilingResult]) -> pd.DataFrame:
    """Flatten metrics for CSV export."""
    records = []
    for tool_key, result in results.items():
        m = result.metrics
        records.append(
            {
                "tool_key": tool_key,
                "tool_name": m.tool_name,
                "success": result.success,
                "runtime_seconds": m.runtime_seconds,
                "row_count": m.row_count,
                "column_count": m.column_count,
                "missing_values_total": m.missing_values_total,
                "missing_percentage": m.missing_percentage,
                "duplicate_rows": m.duplicate_rows,
                "total_outliers": sum(m.outlier_counts.values()),
                "numeric_columns": m.numeric_column_count,
                "categorical_columns": m.categorical_column_count,
                "report_path": m.report_path,
                "json_summary_path": m.json_summary_path,
            }
        )
    return pd.DataFrame(records)
