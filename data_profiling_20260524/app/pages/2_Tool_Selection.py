"""Tool Selection page."""

from __future__ import annotations

import streamlit as st

from app.utils.constants import AVAILABLE_PROFILERS
from app.utils.session_state import get_dataset_metadata, init_session_state

init_session_state()

st.title("Tool Selection")
st.markdown("Select which data profiling tools to include in the evaluation.")

if st.session_state.get("dataset") is None:
    st.warning("Please upload a dataset on the **Dataset Overview** page first.")
    st.stop()

metadata = get_dataset_metadata()
st.info(
    f"Current dataset: **{metadata.get('filename')}** "
    f"({metadata.get('row_count', 0):,} rows × {metadata.get('column_count', 0)} columns)"
)

st.markdown("---")
st.subheader("Available Profiling Tools")

selected: list[str] = []
for tool_key, info in AVAILABLE_PROFILERS.items():
    with st.container(border=True):
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(f"**{info['label']}**")
            st.caption(info["description"])
        with col2:
            if st.checkbox("Select", key=f"select_{tool_key}", value=tool_key in st.session_state.selected_tools):
                selected.append(tool_key)

if st.button("Save Selection", type="primary"):
    if not selected:
        st.error("Please select at least one profiling tool.")
    else:
        st.session_state.selected_tools = selected
        st.success(f"Selected {len(selected)} tool(s): {', '.join(selected)}")

if st.session_state.selected_tools:
    st.markdown("---")
    st.subheader("Current Selection")
    for key in st.session_state.selected_tools:
        st.write(f"- {AVAILABLE_PROFILERS[key]['label']}")
