"""Streamlit session state initialization and helpers."""

from __future__ import annotations

from typing import Any

import streamlit as st


def init_session_state() -> None:
    """Initialize default session state keys."""
    defaults: dict[str, Any] = {
        "dataset": None,
        "dataset_metadata": None,
        "selected_tools": [],
        "profiling_results": {},
        "comparison_results": None,
        "last_run_timestamp": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_profiling_results() -> None:
    """Clear profiling and comparison results when dataset changes."""
    st.session_state.profiling_results = {}
    st.session_state.comparison_results = None
    st.session_state.last_run_timestamp = None


def get_dataset_metadata() -> dict[str, Any]:
    """Return dataset metadata dict, or empty dict when unset."""
    metadata = st.session_state.get("dataset_metadata")
    return metadata if isinstance(metadata, dict) else {}
