# Project Overview

## Title

**Data Profiling Evaluation Platform** — Functional evaluation of freely available data profiling tools for health data research.

## Purpose

Healthcare and real-world datasets often contain missing values, duplicates, inconsistent formats, and outliers. Multiple open-source profiling tools exist, but their outputs, usability, and suitability for research vary significantly.

This platform provides a **unified research interface** to:

1. Upload a dataset (CSV or Excel)
2. Run multiple profiling tools on the same data
3. Compare outputs using standardized metrics
4. Export reports and comparative summaries

The application supports dissertation-style experimentation: repeatable workflows, comparable metrics, and exportable evidence.

## Phase 1 scope (current delivery)

| In scope | Out of scope (future phases) |
|----------|------------------------------|
| CSV / Excel upload | Cloud deployment |
| Three profiling tools | Additional tools beyond Phase 1 |
| HTML + JSON report generation | Enterprise authentication |
| Comparative dashboard | Big-data / distributed processing |
| CSV / JSON export of metrics | Automated data cleaning |

## Profiling tools integrated

| Tool | Role |
|------|------|
| **ydata-profiling** | Comprehensive statistical profiling, correlations, HTML report |
| **Sweetviz** | Visual exploratory data analysis (EDA) |
| **Great Expectations** | Rule-based data validation and expectation suites |

> **Note:** DataPrep was evaluated during development but removed in Phase 1 due to dependency compatibility constraints on target Python environments.

## Target users

- Researchers evaluating profiling tools for health data
- Analysts exploring data quality before modelling
- Dissertation students running structured tool comparisons

## Technology stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10 – 3.13 |
| UI | Streamlit |
| Data processing | Pandas, NumPy |
| Visualisation | Plotly, Matplotlib |
| Profiling | ydata-profiling, Sweetviz, Great Expectations |

## High-level workflow

```
Upload dataset → Validate → Select tools → Run profiling
    → Generate per-tool reports → Extract metrics → Compare & score
    → Dashboard visualisation → Export results
```

## Success criteria (Phase 1)

- All three profiling tools run successfully on uploaded datasets
- Reports are saved locally and downloadable from the UI
- Comparative metrics and scores are displayed consistently
- Setup documentation enables independent local installation
