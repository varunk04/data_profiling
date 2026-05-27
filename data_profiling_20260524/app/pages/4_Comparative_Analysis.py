"""Comparative Analysis page."""

from __future__ import annotations

import streamlit as st

from app.components.charts import (
    plot_data_quality_comparison,
    plot_overall_scores,
    plot_runtime_comparison,
    plot_score_radar,
)
from app.utils.constants import AVAILABLE_PROFILERS
from app.utils.session_state import init_session_state

init_session_state()

st.title("Comparative Analysis")
st.markdown("Compare profiling tool outputs across standardized evaluation metrics.")

if not st.session_state.get("profiling_results"):
    st.warning("Run profiling on the **Profiling Execution** page first.")
    st.stop()

comparison = st.session_state.get("comparison_results")
if comparison is None:
    st.warning("No comparison data available.")
    st.stop()

summary = comparison.get("summary", {})
metrics_df = comparison["metrics_table"]
scores_df = comparison.get("scores_table")

if summary.get("fastest_tool"):
    col1, col2, col3 = st.columns(3)
    col1.metric("Tools Compared", comparison.get("tool_count", 0))
    col2.metric("Fastest Tool", summary.get("fastest_tool", "—"))
    col3.metric("Fastest Runtime (s)", summary.get("fastest_runtime", "—"))

if summary.get("highest_rated_tool"):
    st.metric(
        "Highest Rated Tool",
        summary.get("highest_rated_tool"),
        delta=f"Score: {summary.get('highest_overall_score')}",
    )

st.markdown("---")

tab_metrics, tab_scores, tab_table = st.tabs(["Metrics", "Scores", "Comparison Table"])

with tab_metrics:
    plot_runtime_comparison(metrics_df)
    plot_data_quality_comparison(metrics_df)

with tab_scores:
    if scores_df is not None and not scores_df.empty:
        plot_overall_scores(scores_df)
        plot_score_radar(scores_df)
    else:
        st.info("Score data available after successful profiling runs.")

with tab_table:
    st.subheader("Metrics Comparison")
    st.dataframe(metrics_df, use_container_width=True, hide_index=True)

    if scores_df is not None and not scores_df.empty:
        st.subheader("Evaluation Scores")
        st.dataframe(scores_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption(f"Last run: {st.session_state.get('last_run_timestamp', 'N/A')}")
