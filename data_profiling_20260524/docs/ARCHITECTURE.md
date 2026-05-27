# Technical Architecture

## Design principles

- **Modular adapters** — each profiling tool implements a common interface
- **Lazy loading** — profiling libraries are imported only when a tool runs
- **Standardised metrics** — all tools return the same metric structure for fair comparison
- **Separation of concerns** — UI, services, profiling, and comparison are isolated

## Directory structure

```
project_root/
├── streamlit_app.py          # Entrypoint and navigation
├── requirements.txt
├── environment.yml           # Optional conda environment
├── pyproject.toml            # Python version constraint
│
├── app/
│   ├── pages/                # Streamlit multipage UI
│   ├── components/           # Reusable charts and preview widgets
│   ├── profiling/            # Tool adapters (ydata, sweetviz, GE)
│   ├── comparison/           # Comparison engine and export helpers
│   ├── services/             # Profiling orchestration, report manager
│   └── utils/                # Constants, validation, session state
│
├── datasets/                 # Optional local sample data
├── reports/                  # Runtime-generated HTML/JSON reports
└── docs/                     # Project documentation
```

## Component overview

### 1. Streamlit UI (`app/pages/`)

| Page | Responsibility |
|------|----------------|
| Home | Introduction and session status |
| Dataset Overview | Upload, preview, metadata, correlation heatmap |
| Tool Selection | Choose profiling tools |
| Profiling Execution | Run tools, view per-tool results |
| Comparative Analysis | Charts and comparison tables |
| Report Downloads | Export HTML, JSON, CSV |

### 2. Profiling layer (`app/profiling/`)

**`BaseProfiler`** defines the adapter contract:

- `run_profile(df)` — execute profiling
- `generate_report()` — save HTML/JSON artifacts
- `extract_metrics()` — return `ProfilingMetrics`

**`metrics.py`** computes shared dataset statistics (missing values, duplicates, outliers, correlations) so every tool is judged on the same quantitative baseline.

| Adapter | Output location |
|---------|-----------------|
| `YDataProfiler` | `reports/ydata/` |
| `SweetvizProfiler` | `reports/sweetviz/` |
| `GreatExpectationsProfiler` | `reports/great_expectations/` |

### 3. Service layer (`app/services/`)

**`ProfilingService`** orchestrates multi-tool runs and invokes the comparison engine.

**`ReportManager`** handles CSV/JSON export and file downloads.

### 4. Comparison layer (`app/comparison/`)

**`ComparisonEngine`** builds:

- A **metrics table** (runtime, missing values, duplicates, outliers, etc.)
- A **scores table** (evaluation dimensions on a 0–10 scale)
- A **summary** (fastest tool, highest-rated tool)

See [COMPARISON_METHODOLOGY.md](COMPARISON_METHODOLOGY.md) for scoring details.

## Data flow

```
User CSV
   ↓
file_validation.load_dataset()
   ↓
session_state (dataset + metadata)
   ↓
ProfilingService.run_profilers()
   ↓
get_profiler(tool_key) → adapter.run_profile()
   ↓
reports/<tool>/profile_<timestamp>.html|.json
   ↓
ComparisonEngine.compare()
   ↓
Streamlit charts + export
```

## Session state

| Key | Description |
|-----|-------------|
| `dataset` | Loaded pandas DataFrame |
| `dataset_metadata` | Row/column counts, dtypes, missing values |
| `selected_tools` | List of tool keys to run |
| `profiling_results` | Dict of `ProfilingResult` per tool |
| `comparison_results` | Output of `ComparisonEngine.compare()` |
| `last_run_timestamp` | Last profiling run time |

## Extension points (future phases)

- Add a new profiler: implement `BaseProfiler`, register in `app/profiling/__init__.py`, add to `constants.AVAILABLE_PROFILERS`
- Add new comparison metrics: extend `ComparisonEngine._score_tool()`
- Add database or API backend: replace session state with persistent storage
