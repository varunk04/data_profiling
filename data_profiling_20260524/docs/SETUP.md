# Setup Guide

## Requirements

| Requirement | Detail |
|-------------|--------|
| Python | **3.10, 3.11, 3.12, or 3.13** |
| Package manager | pip (included with Python or conda) |
| Optional | Anaconda / Miniconda |

Formal constraint in `pyproject.toml`:

```toml
requires-python = ">=3.10,<3.14"
```

---

## Option A — Conda (recommended)

```bash
conda create -n data-profiling python=3.10 -y
conda activate data-profiling
cd path/to/data_profiling_20260524
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Alternative:** create from `environment.yml`:

```bash
conda env create -f environment.yml
conda activate data-profiling
streamlit run streamlit_app.py
```

---

## Option B — venv (existing Python 3.10–3.13)

```bash
cd path/to/data_profiling_20260524
python --version          # must show 3.10.x – 3.13.x
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Windows — specific Python version:**

```bash
py -0p
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Verify installation

```bash
python --version
python -c "import streamlit, pandas, ydata_profiling, sweetviz; print('OK')"
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| streamlit | Dashboard UI |
| pandas, numpy | Data processing |
| plotly, matplotlib | Charts |
| ydata-profiling | Statistical profiling |
| sweetviz | Visual EDA |
| great-expectations | Data validation |
| setuptools (<82) | Required by ydata-profiling (`pkg_resources`) |
| openpyxl | Excel file support |

---

## Troubleshooting

### `No module named 'pkg_resources'`

setuptools **82+** removed `pkg_resources`. Install a compatible version:

```bash
pip install "setuptools>=65.0.0,<82.0.0"
pip install -r requirements.txt
```

### `No matching distribution found for ydata-profiling`

Your Python version is likely **3.14+**. Use Python 3.10–3.13 (conda or venv).

### NumPy build errors on Windows

Usually caused by Python 3.14 pulling source builds. Switch to Python 3.10–3.13.

### Profiling page dependency warning

The Profiling Execution page checks runtime dependencies before running. Follow the pip command shown in the UI.

---

## Project layout after setup

```
reports/          ← generated at runtime (gitignored)
datasets/         ← optional sample CSV files
app/              ← application source code
docs/             ← documentation
```

---

## Remove environment

**Conda:**

```bash
conda deactivate
conda env remove -n data-profiling
```

**venv:** delete the `.venv` folder.

---

## Next steps

- Read [USER_GUIDE.md](USER_GUIDE.md) for dashboard usage
- Read [COMPARISON_METHODOLOGY.md](COMPARISON_METHODOLOGY.md) for scoring details
