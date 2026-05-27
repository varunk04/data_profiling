"""Profiling Execution page."""

from __future__ import annotations

import streamlit as st

from app.components.metrics_cards import render_profiling_summary_cards
from app.services.profiling_service import ProfilingService
from app.utils.constants import AVAILABLE_PROFILERS
from app.utils.dependency_check import dependency_install_hint, missing_runtime_dependencies
from app.utils.session_state import init_session_state

init_session_state()

st.title("Profiling Execution")
st.markdown("Run selected profiling tools on the uploaded dataset.")

if st.session_state.get("dataset") is None:
    st.warning("Please upload a dataset first.")
    st.stop()

if not st.session_state.selected_tools:
    st.warning("Please select profiling tools on the **Tool Selection** page.")
    st.stop()

df = st.session_state.dataset
selected = st.session_state.selected_tools

st.info(f"Ready to profile **{len(selected)}** tool(s) on {len(df):,} rows.")

missing_deps = missing_runtime_dependencies()
if missing_deps:
    st.error(
        "Missing runtime dependencies:\n\n"
        + "\n".join(f"- {item}" for item in missing_deps)
        + f"\n\nRun in your active environment:\n\n`{dependency_install_hint()}`"
    )
    st.stop()

if st.button("Run Profiling", type="primary", use_container_width=True):
    service = ProfilingService()
    progress = st.progress(0, text="Starting profiling...")
    status_box = st.empty()
    total = len(selected)

    def on_progress(tool_key: str, status: str) -> None:
        label = AVAILABLE_PROFILERS[tool_key]["label"]
        status_box.info(f"**{label}**: {status}")

    with st.spinner("Running profilers... This may take a few minutes."):
        results = service.run_profilers(df, selected, progress_callback=on_progress)
        comparison = service.compare_results(results)

    st.session_state.profiling_results = results
    st.session_state.comparison_results = comparison
    st.session_state.last_run_timestamp = service.timestamp()
    progress.progress(1.0, text="Profiling complete!")
    st.success(f"Profiling completed at {st.session_state.last_run_timestamp}")

results = st.session_state.get("profiling_results", {})

if not results:
    st.stop()

st.markdown("---")
st.subheader("Profiling Results")

for tool_key, result in results.items():
    label = AVAILABLE_PROFILERS[tool_key]["label"]
    with st.expander(f"{label} — {'Success' if result.success else 'Failed'}", expanded=False):
        if result.success:
            render_profiling_summary_cards(result.metrics)
            if result.report_html_path:
                st.markdown(f"Report saved: `{result.report_html_path}`")
        else:
            st.error(result.error_message or "Profiling failed.")
