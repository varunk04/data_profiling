"""Application-wide constants."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASETS_DIR = PROJECT_ROOT / "datasets"
REPORTS_DIR = PROJECT_ROOT / "reports"

APP_TITLE = "Data Profiling Evaluation Platform"
APP_DESCRIPTION = (
    "A research-oriented platform for evaluating and comparing freely available "
    "data profiling tools on healthcare and noisy datasets."
)

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
MAX_PREVIEW_ROWS = 100
MAX_UPLOAD_SIZE_MB = 200

PROFILER_DIRS = {
    "ydata": REPORTS_DIR / "ydata",
    "sweetviz": REPORTS_DIR / "sweetviz",
    "great_expectations": REPORTS_DIR / "great_expectations",
}

AVAILABLE_PROFILERS = {
    "ydata": {
        "name": "ydata-profiling",
        "label": "ydata-profiling (Pandas Profiling)",
        "description": "Comprehensive statistical summaries, correlations, and HTML reports.",
    },
    "sweetviz": {
        "name": "Sweetviz",
        "label": "Sweetviz",
        "description": "Visual EDA with feature comparisons and target analysis.",
    },
    "great_expectations": {
        "name": "Great Expectations",
        "label": "Great Expectations",
        "description": "Rule-based validation and expectation suite generation.",
    },
}
