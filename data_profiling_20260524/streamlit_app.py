"""Data Profiling Evaluation Platform — Streamlit entrypoint."""

from __future__ import annotations

import streamlit as st

from app.utils.constants import APP_TITLE
from app.utils.python_compat import compatibility_message, is_supported_python, python_version_label, supported_range_label
from app.utils.session_state import init_session_state

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()

with st.sidebar:
    st.caption(f"Python {python_version_label()}")
    if not is_supported_python():
        warning = compatibility_message()
        if warning:
            st.warning(warning)
    else:
        st.caption(f"Supported range: {supported_range_label()}")

home = st.Page("app/pages/0_Home.py", title="Home", icon="🏠", default=True)
dataset_overview = st.Page("app/pages/1_Dataset_Overview.py", title="Dataset Overview", icon="📁")
tool_selection = st.Page("app/pages/2_Tool_Selection.py", title="Tool Selection", icon="🔧")
profiling = st.Page("app/pages/3_Profiling_Execution.py", title="Profiling Execution", icon="▶️")
comparison = st.Page("app/pages/4_Comparative_Analysis.py", title="Comparative Analysis", icon="📈")
downloads = st.Page("app/pages/5_Report_Downloads.py", title="Report Downloads", icon="💾")

pg = st.navigation([home, dataset_overview, tool_selection, profiling, comparison, downloads])
pg.run()
