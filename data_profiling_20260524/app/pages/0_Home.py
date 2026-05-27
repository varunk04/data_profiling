"""Home page."""

from __future__ import annotations

import streamlit as st

from app.utils.constants import APP_DESCRIPTION, APP_TITLE
from app.utils.session_state import get_dataset_metadata, init_session_state

init_session_state()

st.title(APP_TITLE)
st.markdown(APP_DESCRIPTION)

st.markdown("---")
st.subheader("Getting Started")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**1. Dataset Overview**\n\nUpload and inspect your dataset.")
with col2:
    st.info("**2. Tool Selection & Profiling**\n\nChoose tools and run profiling.")
with col3:
    st.info("**3. Compare & Export**\n\nAnalyze results and download reports.")

st.markdown("---")
st.markdown(
    "Use the sidebar to navigate between pages. "
    "Start with **Dataset Overview** to upload a CSV file."
)

if st.session_state.get("dataset") is not None:
    meta = get_dataset_metadata()
    st.success(
        f"Dataset loaded: **{meta.get('filename', 'Unknown')}** "
        f"({meta.get('row_count', 0):,} rows × {meta.get('column_count', 0)} columns)"
    )
else:
    st.warning("No dataset loaded yet. Go to **Dataset Overview** to upload a file.")
