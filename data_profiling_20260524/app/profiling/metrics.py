"""Shared dataset metrics used across all profilers."""

from __future__ import annotations

from typing import Any

import pandas as pd


def compute_base_metrics(df: pd.DataFrame) -> dict[str, Any]:
    """Compute standardized metrics from a DataFrame."""
    missing_counts = df.isnull().sum()
    total_cells = df.shape[0] * df.shape[1]
    total_missing = int(missing_counts.sum())

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns
    datetime_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns

    outlier_counts: dict[str, int] = {}
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 4:
            continue
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outlier_counts[str(col)] = int(((series < lower) | (series > upper)).sum())

    correlation_insights: dict[str, Any] = {}
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        pairs = []
        for i, col_a in enumerate(numeric_cols):
            for col_b in numeric_cols[i + 1 :]:
                value = corr.loc[col_a, col_b]
                if pd.notna(value):
                    pairs.append(
                        {
                            "column_a": str(col_a),
                            "column_b": str(col_b),
                            "correlation": round(float(value), 4),
                        }
                    )
        pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)
        correlation_insights = {
            "top_correlations": pairs[:10],
            "strong_correlations_count": sum(1 for p in pairs if abs(p["correlation"]) >= 0.7),
        }

    return {
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "missing_values_total": total_missing,
        "missing_percentage": round((total_missing / total_cells * 100) if total_cells else 0, 2),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "null_percentage_by_column": {
            col: round((count / len(df) * 100) if len(df) else 0, 2)
            for col, count in missing_counts.items()
        },
        "outlier_counts": outlier_counts,
        "correlation_insights": correlation_insights,
        "numeric_column_count": len(numeric_cols),
        "categorical_column_count": len(categorical_cols),
        "datetime_column_count": len(datetime_cols),
    }
