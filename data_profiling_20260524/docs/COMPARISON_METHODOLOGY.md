# Comparison Methodology

This document describes how the platform compares data profiling tools and how evaluation scores are calculated.

## Objectives

The comparison framework is designed to support **research-style evaluation** by:

1. Running all tools on the **same dataset**
2. Extracting **standardised quantitative metrics** from each run
3. Applying a **consistent scoring model** across tools
4. Presenting results in **tables and charts** for interpretation

## Standardised metrics (all tools)

Every profiler adapter computes the following baseline metrics from the uploaded DataFrame (independent of tool-specific output):

| Metric | Description |
|--------|-------------|
| `row_count` | Number of rows |
| `column_count` | Number of columns |
| `missing_values_total` | Total null cells |
| `missing_percentage` | Null cells as % of all cells |
| `duplicate_rows` | Exact duplicate row count |
| `outlier_counts` | Per-column IQR outlier count (numeric columns) |
| `correlation_insights` | Top correlations and count of strong correlations (|r| ≥ 0.7) |
| `numeric_column_count` | Count of numeric columns |
| `categorical_column_count` | Count of object/category/boolean columns |
| `runtime_seconds` | Wall-clock execution time |

These metrics appear in the **Metrics Comparison** table on the Comparative Analysis page.

## Tool-specific outputs

| Tool | Additional output |
|------|-------------------|
| ydata-profiling | Full HTML statistical report, JSON description summary |
| Sweetviz | Visual HTML EDA report |
| Great Expectations | Validation expectations, pass rate, HTML summary |

## Evaluation dimensions (scoring)

Each successful tool receives scores on **eight dimensions** (scale **0–10**). Seven dimensions contribute to a weighted-style average called the **overall score**.

| Dimension | Type | How it is determined |
|-----------|------|----------------------|
| **Missing value detection** | Quantitative | 10.0 when baseline missing-value metrics are computed successfully |
| **Duplicate detection** | Quantitative | 10.0 when duplicate row count is computed successfully |
| **Outlier detection** | Quantitative | 8.0 if IQR outliers were detected; 6.0 otherwise |
| **Runtime performance** | Quantitative | Relative to fastest tool: `min(10, (fastest_runtime / tool_runtime) × 8)` |
| **Visualization quality** | Qualitative (fixed) | Pre-assigned per tool based on report type |
| **Ease of interpretation** | Qualitative (fixed) | Pre-assigned per tool based on UX of reports |
| **Report completeness** | Qualitative (fixed) | Pre-assigned per tool based on depth of insights |
| **Usability** | Qualitative (fixed) | Pre-assigned per tool based on setup and workflow |

### Qualitative baseline scores (Phase 1)

These reflect expected strengths of each tool category for health-data research use cases:

| Tool | Visualization | Interpretation | Completeness | Usability |
|------|---------------|----------------|--------------|-----------|
| ydata-profiling | 9.0 | 8.5 | 9.5 | 8.0 |
| Sweetviz | 9.5 | 9.0 | 8.0 | 8.5 |
| Great Expectations | 6.5 | 7.0 | 8.0 | 6.5 |

> **Research note:** Qualitative scores are configurable in `app/comparison/comparison_engine.py` (`TOOL_SCORES`). They can be calibrated in future phases using structured user studies or rubric-based expert review.

## Overall score formula

```
overall_score = (
    missing_value_detection
  + duplicate_detection
  + outlier_detection
  + visualization_quality
  + ease_of_interpretation
  + runtime_performance
  + report_completeness
  + usability
) / 8
```

Result is rounded to **two decimal places**.

## Comparative summary

After scoring, the engine produces:

| Summary field | Meaning |
|---------------|---------|
| `fastest_tool` | Tool with lowest `runtime_seconds` |
| `fastest_runtime` | That tool’s runtime in seconds |
| `highest_rated_tool` | Tool with highest `overall_score` |
| `highest_overall_score` | That tool’s overall score |

## Visualisations

| Chart | Data source |
|-------|-------------|
| Runtime comparison bar chart | `runtime_seconds` per tool |
| Data quality grouped bar chart | Missing values, duplicates, outliers |
| Overall score horizontal bar | `overall_score` per tool |
| Radar chart | All eight scoring dimensions |

## Limitations (Phase 1)

1. **Same baseline metrics for all tools** — tool-native quality findings may not be fully captured
2. **Qualitative scores are static** — not derived from user surveys in Phase 1
3. **Outlier method** — IQR (1.5×) only; tools may use different statistical definitions
4. **Great Expectations** — uses a focused expectation suite; not a full GE Data Context deployment

## Future enhancements

- User-adjustable rubric weights
- Blind user studies for visualization and interpretation scores
- Agreement metrics between tools (e.g. missing-value detection concordance)
- Dataset-specific benchmarks with ground-truth labels
