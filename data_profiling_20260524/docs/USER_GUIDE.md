# User Guide

This guide explains how to use the **Data Profiling Evaluation Platform** dashboard.

## Before you start

1. Complete installation per [SETUP.md](SETUP.md)
2. Activate your environment: `conda activate data-profiling`
3. Launch the app: `streamlit run streamlit_app.py`
4. Open the URL shown in the terminal (typically `http://localhost:8501`)

## Dashboard pages

### 1. Home

Overview of the platform and confirmation of whether a dataset is loaded.

### 2. Dataset Overview

**Upload a dataset**

- Supported formats: `.csv`, `.xlsx`, `.xls`
- Use the file uploader at the top of the page

**After upload you will see:**

- Summary cards: rows, columns, missing values, duplicates, memory usage
- Tabs:
  - **Preview** — first 100 rows
  - **Data Types** — column type distribution
  - **Missing Values** — bar chart of nulls by column
  - **Correlations** — heatmap for numeric columns

> Uploading a **new file** clears previous profiling results automatically.

### 3. Tool Selection

- Review the three available profiling tools
- Check **Select** for each tool you want to run
- Click **Save Selection**

| Tool | Best for |
|------|----------|
| ydata-profiling | Deep statistical summaries and HTML reports |
| Sweetviz | Visual EDA and quick pattern discovery |
| Great Expectations | Validation rules and pass/fail expectations |

### 4. Profiling Execution

1. Confirm a dataset and tool selection are in place
2. Click **Run Profiling**
3. Wait for completion (runtime depends on dataset size)
4. Expand each tool’s result panel to view metrics

**Outputs saved to:**

```
reports/ydata/
reports/sweetviz/
reports/great_expectations/
```

Each run creates timestamped `profile_<YYYYMMDD_HHMMSS>.html` and `.json` files.

### 5. Comparative Analysis

Available after a successful profiling run.

| Tab | Content |
|-----|---------|
| **Metrics** | Runtime bar chart, data-quality comparison |
| **Scores** | Overall scores and radar chart by evaluation dimension |
| **Comparison Table** | Full metrics and scores tables |

Summary cards highlight the **fastest tool** and **highest-rated tool**.

### 6. Report Downloads

Export options:

| Export | Format | Contents |
|--------|--------|----------|
| Metrics | CSV | Flattened per-tool metrics |
| Metrics | JSON | Full metrics per tool |
| Comparison | JSON | Comparison tables and summary |
| Per-tool | HTML | Original profiling report |
| Per-tool | JSON | Tool-specific summary file |

## Recommended workflow

```
Dataset Overview  →  Tool Selection  →  Profiling Execution
        →  Comparative Analysis  →  Report Downloads
```

## Tips

- Start with a **small dataset** (under 10,000 rows) for faster first runs
- Run **all three tools** for the most complete comparison
- Use **ydata-profiling** when you need a publication-ready HTML report
- Use **Great Expectations** when validation pass rates matter for your research
- Review [COMPARISON_METHODOLOGY.md](COMPARISON_METHODOLOGY.md) to interpret scores

## Sample dataset

A sample dirty cafe sales CSV is included at:

```
datasets/dirty_cafe_sales.csv
```

Upload this file on the Dataset Overview page to test the platform immediately.
