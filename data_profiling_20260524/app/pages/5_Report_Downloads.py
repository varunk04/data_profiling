"""Report Downloads page."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.services.report_manager import ReportManager
from app.utils.constants import AVAILABLE_PROFILERS, PROFILER_DIRS
from app.utils.session_state import init_session_state

init_session_state()

st.title("Report Downloads")
st.markdown("Export profiling reports and comparative metrics.")

report_manager = ReportManager()
results = st.session_state.get("profiling_results", {})
comparison = st.session_state.get("comparison_results")

if not results:
    st.warning("No profiling results available. Run profiling first.")
else:
    st.subheader("Export Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "Download Metrics (CSV)",
            data=report_manager.export_metrics_csv(results),
            file_name="profiling_metrics.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "Download Metrics (JSON)",
            data=report_manager.export_metrics_json(results),
            file_name="profiling_metrics.json",
            mime="application/json",
            use_container_width=True,
        )

    with col3:
        if comparison:
            st.download_button(
                "Download Comparison (JSON)",
                data=report_manager.export_comparison_json(comparison),
                file_name="comparison_results.json",
                mime="application/json",
                use_container_width=True,
            )

    st.markdown("---")
    st.subheader("Individual Tool Reports")

    for tool_key, result in results.items():
        label = AVAILABLE_PROFILERS[tool_key]["label"]
        with st.expander(label):
            if not result.success:
                st.error(result.error_message or "Profiling failed — no report available.")
                continue

            if result.report_html_path and Path(result.report_html_path).exists():
                html_data = report_manager.read_report_file(result.report_html_path)
                if html_data:
                    st.download_button(
                        f"Download {label} HTML Report",
                        data=html_data,
                        file_name=Path(result.report_html_path).name,
                        mime="text/html",
                        key=f"html_{tool_key}",
                    )

            if result.json_path and Path(result.json_path).exists():
                json_data = report_manager.read_report_file(result.json_path)
                if json_data:
                    st.download_button(
                        f"Download {label} JSON Summary",
                        data=json_data,
                        file_name=Path(result.json_path).name,
                        mime="application/json",
                        key=f"json_{tool_key}",
                    )

st.markdown("---")
st.subheader("Saved Reports Directory")

for tool_key, tool_dir in PROFILER_DIRS.items():
    reports = report_manager.list_reports_for_tool(tool_key)
    label = AVAILABLE_PROFILERS[tool_key]["label"]
    st.markdown(f"**{label}** — `{tool_dir}` ({len(reports)} files)")
