"""Plotly and Matplotlib visualization helpers."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def plot_runtime_comparison(metrics_df: pd.DataFrame) -> None:
    """Bar chart comparing profiler runtime."""
    if metrics_df.empty:
        st.info("No runtime data available.")
        return

    fig = px.bar(
        metrics_df,
        x="tool",
        y="runtime_seconds",
        title="Runtime Comparison (seconds)",
        color="tool",
        text="runtime_seconds",
    )
    fig.update_traces(texttemplate="%{text:.2f}s", textposition="outside")
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)


def plot_data_quality_comparison(metrics_df: pd.DataFrame) -> None:
    """Grouped bar chart for data quality metrics across tools."""
    if metrics_df.empty:
        return

    melted = metrics_df.melt(
        id_vars=["tool"],
        value_vars=["missing_values", "duplicates", "outliers"],
        var_name="metric",
        value_name="count",
    )
    fig = px.bar(
        melted,
        x="tool",
        y="count",
        color="metric",
        barmode="group",
        title="Data Quality Detection Comparison",
    )
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)


def plot_score_radar(scores_df: pd.DataFrame) -> None:
    """Radar chart comparing tool evaluation scores."""
    if scores_df.empty:
        return

    score_cols = [
        c
        for c in scores_df.columns
        if c not in ("tool", "tool_key", "overall_score")
    ]
    if not score_cols:
        return

    fig = go.Figure()
    for _, row in scores_df.iterrows():
        fig.add_trace(
            go.Scatterpolar(
                r=[row[c] for c in score_cols],
                theta=[c.replace("_", " ").title() for c in score_cols],
                fill="toself",
                name=row["tool"],
            )
        )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        title="Tool Evaluation Scores",
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_overall_scores(scores_df: pd.DataFrame) -> None:
    """Bar chart of overall evaluation scores."""
    if scores_df.empty or "overall_score" not in scores_df.columns:
        return

    fig = px.bar(
        scores_df.sort_values("overall_score", ascending=True),
        x="overall_score",
        y="tool",
        orientation="h",
        title="Overall Evaluation Score",
        color="overall_score",
        color_continuous_scale="Blues",
    )
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    """Plotly correlation heatmap for numeric columns."""
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        st.info("Need at least 2 numeric columns for correlation heatmap.")
        return

    corr = numeric_df.corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Heatmap",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def plot_null_percentage(null_pct: dict[str, float], top_n: int = 15) -> None:
    """Horizontal bar chart of null percentages by column."""
    if not null_pct:
        return

    df = pd.DataFrame(list(null_pct.items()), columns=["column", "null_pct"])
    df = df[df["null_pct"] > 0].sort_values("null_pct", ascending=False).head(top_n)
    if df.empty:
        st.info("No null values in any column.")
        return

    fig = px.bar(
        df,
        x="null_pct",
        y="column",
        orientation="h",
        title="Null Percentage by Column (Top Columns)",
    )
    fig.update_layout(height=max(300, len(df) * 25))
    st.plotly_chart(fig, use_container_width=True)
