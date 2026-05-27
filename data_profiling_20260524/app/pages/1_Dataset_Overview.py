"""Dataset Overview page — upload, preview, and metadata."""

from __future__ import annotations

import streamlit as st
import pandas as pd

from app.components.charts import plot_correlation_heatmap, plot_null_percentage
from app.components.dataset_preview import (
    render_dataset_metadata,
    render_dataset_preview,
    render_dtype_summary,
    render_missing_values_chart,
)
from app.utils.file_validation import DatasetValidationError, extract_dataset_metadata, load_dataset
from app.utils.session_state import clear_profiling_results, get_dataset_metadata, init_session_state

init_session_state()

st.title("Dataset Overview")
st.markdown("Upload a CSV or Excel file to begin profiling evaluation.")

uploaded_file = st.file_uploader(
    "Upload dataset",
    type=["csv", "xlsx", "xls"],
    help="Supported formats: CSV, Excel (.xlsx, .xls)",
)

if uploaded_file is not None:
    try:
        df = load_dataset(uploaded_file)
        metadata = extract_dataset_metadata(df, uploaded_file.name)

        if get_dataset_metadata().get("filename") != uploaded_file.name:
            clear_profiling_results()

        st.session_state.dataset = df
        st.session_state.dataset_metadata = metadata
        st.success(f"Successfully loaded **{uploaded_file.name}**")

    except DatasetValidationError as exc:
        st.error(str(exc))
        st.stop()

if st.session_state.get("dataset") is None:
    st.info("Upload a dataset to see preview and metadata.")
    st.stop()

df = st.session_state.dataset
metadata = st.session_state.dataset_metadata

st.markdown("---")
render_dataset_metadata(metadata)

tab_preview, tab_dtypes, tab_missing, tab_corr = st.tabs(
    ["Preview", "Data Types", "Missing Values", "Correlations"]
)

with tab_preview:
    render_dataset_preview(df)

with tab_dtypes:
    render_dtype_summary(metadata)
    st.subheader("Column Data Types")
    dtype_df = pd.DataFrame(
        list(metadata.get("dtypes", {}).items()), columns=["Column", "Data Type"]
    )
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)

with tab_missing:
    render_missing_values_chart(metadata)
    null_pct = metadata.get("null_percentage_by_column", {})
    plot_null_percentage(null_pct)

with tab_corr:
    plot_correlation_heatmap(df)
