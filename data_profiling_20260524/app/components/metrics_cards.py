"""Summary metric card components."""

from __future__ import annotations

import streamlit as st

from app.profiling.base_profiler import ProfilingMetrics


def render_profiling_summary_cards(metrics: ProfilingMetrics) -> None:
    """Render summary cards for a single profiler's metrics."""
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Runtime (s)", metrics.runtime_seconds)
    col2.metric("Missing %", f"{metrics.missing_percentage}%")
    col3.metric("Duplicates", metrics.duplicate_rows)
    col4.metric("Outliers", sum(metrics.outlier_counts.values()))

    col5, col6, col7 = st.columns(3)
    col5.metric("Numeric Cols", metrics.numeric_column_count)
    col6.metric("Categorical Cols", metrics.categorical_column_count)
    col7.metric(
        "Strong Correlations",
        metrics.correlation_insights.get("strong_correlations_count", 0),
    )
