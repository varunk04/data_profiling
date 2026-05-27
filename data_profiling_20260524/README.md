# Data Profiling Evaluation Platform

A Streamlit application for evaluating and comparing open-source data profiling tools on healthcare and noisy datasets.

**Phase 1** delivers dataset upload, multi-tool profiling, comparative dashboards, and report export.

## Quick start

```bash
conda create -n data-profiling python=3.10 -y
conda activate data-profiling
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Full instructions: [docs/SETUP.md](docs/SETUP.md)

## Documentation

| Document | Description |
|----------|-------------|
| [docs/INDEX.md](docs/INDEX.md) | Documentation index |
| [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) | Project purpose and scope |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical architecture |
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | How to use the dashboard |
| [docs/COMPARISON_METHODOLOGY.md](docs/COMPARISON_METHODOLOGY.md) | Metrics and scoring framework |
| [docs/PHASE1_DELIVERABLES.md](docs/PHASE1_DELIVERABLES.md) | Phase 1 deliverables summary |
| [docs/SETUP.md](docs/SETUP.md) | Installation and troubleshooting |

## Profiling tools

- **ydata-profiling** — statistical summaries and HTML reports
- **Sweetviz** — visual exploratory data analysis
- **Great Expectations** — data validation and expectation suites

## Project structure

```
├── app/                  # Application code
│   ├── pages/            # Streamlit pages
│   ├── components/       # UI components
│   ├── profiling/        # Tool adapters
│   ├── comparison/       # Comparison engine
│   ├── services/         # Orchestration layer
│   └── utils/            # Shared utilities
├── datasets/             # Sample datasets (optional)
├── reports/              # Generated reports (runtime output)
├── docs/                 # Project documentation
├── streamlit_app.py      # Application entrypoint
├── requirements.txt
└── environment.yml
```

## Python version

**Python 3.10 – 3.13** required. See `pyproject.toml` for the formal constraint.
