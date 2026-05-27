"""Dataset preview and metadata display components."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from app.utils.constants import MAX_PREVIEW_ROWS


def render_dataset_metadata(metadata: dict[str, Any]) -> None:
    """Render summary metric cards for dataset metadata."""
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{metadata.get('row_count', 0):,}")
    col2.metric("Columns", metadata.get("column_count", 0))
    col3.metric("Missing Values", f"{metadata.get('total_missing', 0):,}")
    col4.metric("Duplicate Rows", f"{metadata.get('duplicate_rows', 0):,}")

    col5, col6, col7 = st.columns(3)
    col5.metric("Missing %", f"{metadata.get('missing_percentage', 0)}%")
    col6.metric("Memory (MB)", metadata.get("memory_usage_mb", 0))
    col7.metric("File", metadata.get("filename", "—"))


def render_dtype_summary(metadata: dict[str, Any]) -> None:
    """Render data type distribution."""
    dtype_counts = metadata.get("dtype_counts", {})
    if dtype_counts:
        st.subheader("Data Types")
        st.dataframe(
            pd.DataFrame(list(dtype_counts.items()), columns=["Data Type", "Count"]),
            use_container_width=True,
            hide_index=True,
        )


def render_missing_values_chart(metadata: dict[str, Any]) -> None:
    """Render missing values by column."""
    missing = metadata.get("missing_by_column", {})
    if not missing:
        return

    st.subheader("Missing Values by Column")
    missing_df = pd.DataFrame(
        [{"column": k, "missing_count": v} for k, v in missing.items() if v > 0]
    )
    if missing_df.empty:
        st.info("No missing values detected.")
        return
    missing_df = missing_df.sort_values("missing_count", ascending=False)
    st.bar_chart(missing_df.set_index("column"))


def render_dataset_preview(df: pd.DataFrame, n_rows: int = MAX_PREVIEW_ROWS) -> None:
    """Render dataset preview table."""
    st.subheader("Dataset Preview")
    st.dataframe(df.head(n_rows), use_container_width=True)
    if len(df) > n_rows:
        st.caption(f"Showing first {n_rows} of {len(df):,} rows.")
