# Product Requirements Document (PRD)

# Project Title

Evaluation of Freely Available Data Profiling Tools for Health Data Research Application: A Functional Evaluation Review

---

# 1. Project Overview

The objective of this project is to design and develop a Python-based application for evaluating and comparing freely available data profiling and data quality assessment tools using real-world datasets, with a focus on healthcare and noisy datasets.

The system will provide a unified interface for running multiple profiling tools on uploaded datasets and comparing their outputs based on data quality detection, reporting capability, usability, and visualization quality.

The project also supports a dissertation/research use case where comparative analysis, experimental evaluation, and literature-backed findings are required.

---

# 2. Problem Statement

Modern datasets, especially healthcare datasets, often contain:

* Missing values
* Duplicates
* Invalid formats
* Inconsistent entries
* Outliers
* Data quality issues

Multiple open-source data profiling tools exist, but there is limited comparative evaluation regarding:

* Accuracy
* Visualization capability
* Ease of use
* Reporting quality
* Suitability for healthcare research applications

This project aims to create a comparative evaluation framework and dashboard to analyze the effectiveness of these tools.

---

# 3. Goals and Objectives

## Primary Goals

1. Evaluate multiple open-source data profiling tools
2. Compare generated profiling outputs
3. Build a unified dashboard for dataset profiling
4. Generate comparative reports and visualizations
5. Support research/dissertation experimentation

## Secondary Goals

1. Automate report generation
2. Improve accessibility of profiling outputs
3. Provide reusable evaluation workflows
4. Support multiple dataset types

---

# 4. Scope of Work

## In Scope

* Dataset upload and processing
* Integration with multiple profiling tools
* Automated report generation
* Comparative visualization dashboards
* Data quality metrics evaluation
* Exportable profiling summaries
* Streamlit-based frontend dashboard
* Python backend implementation

## Out of Scope

* Distributed big data processing
* Enterprise authentication systems
* Cloud deployment optimization
* Real-time streaming data profiling
* Machine learning model training
* Production-scale healthcare compliance systems

---

# 5. Proposed Technical Stack

## Backend

* Python 3.x

## Data Processing

* Pandas
* NumPy

## Data Profiling Tools

* ydata-profiling (Pandas Profiling)
* Sweetviz
* DataPrep
* Great Expectations

## Visualization

* Matplotlib
* Plotly

## Frontend/UI

* Streamlit

## Report Handling

* HTML Reports
* JSON summaries
* CSV exports

---

# 6. System Architecture

## High-Level Workflow

User Uploads Dataset
↓
Dataset Validation
↓
Profiling Engine
↓
Run Multiple Profiling Tools
↓
Generate Individual Reports
↓
Extract Metrics and Summaries
↓
Comparative Evaluation Layer
↓
Dashboard Visualization
↓
Export Reports

---

# 7. Functional Requirements

# 7.1 Dataset Upload Module

## Features

* Upload CSV files
* Upload Excel files (optional)
* Preview uploaded dataset
* Display dataset metadata

## Validations

* File type validation
* Empty dataset handling
* Unsupported format handling

---

# 7.2 Profiling Engine

The system should support running multiple profiling tools independently.

## Supported Tools

### 1. ydata-profiling

Capabilities:

* Missing value analysis
* Correlation analysis
* Statistical summaries
* Duplicate detection
* HTML report generation

### 2. Sweetviz

Capabilities:

* EDA visualizations
* Feature comparison
* Target analysis
* Visual summaries

### 3. DataPrep

Capabilities:

* Automated profiling
* Data quality summaries
* Distribution analysis

### 4. Great Expectations

Capabilities:

* Data validation
* Rule-based checks
* Expectation suite generation

---

# 7.3 Comparative Evaluation Module

The application should compare tools using common evaluation metrics.

## Comparison Metrics

| Metric                  | Description                     |
| ----------------------- | ------------------------------- |
| Missing Value Detection | Ability to identify null values |
| Duplicate Detection     | Duplicate row identification    |
| Outlier Detection       | Statistical anomaly detection   |
| Visualization Quality   | Usefulness of generated charts  |
| Ease of Interpretation  | Human readability               |
| Runtime Performance     | Execution speed                 |
| Report Completeness     | Depth of generated insights     |
| Usability               | Ease of execution/setup         |

---

# 7.4 Dashboard Module

## Features

* Dataset summary view
* Profiling results view
* Tool comparison dashboard
* Charts and visual summaries
* Metric comparison tables
* Interactive filtering

## Suggested Dashboard Sections

### Section 1 — Dataset Overview

* Number of rows
* Number of columns
* Missing values
* Data types

### Section 2 — Profiling Results

* Tool-specific reports
* Statistical summaries
* Correlation heatmaps

### Section 3 — Comparative Analysis

* Tool comparison tables
* Runtime comparison
* Data quality detection comparison

### Section 4 — Export and Downloads

* Export reports
* Download profiling outputs

---

# 8. Non-Functional Requirements

## Performance

* Handle datasets up to moderate size efficiently
* Minimize dashboard lag

## Usability

* Simple and intuitive UI
* Minimal setup complexity

## Maintainability

* Modular code structure
* Clear separation of components

## Scalability

* Easy addition of new profiling tools

---

# 9. Dataset Strategy

## Suggested Datasets

### Healthcare Dataset

* Smartwatch health dataset
* Public healthcare datasets

### Dirty Dataset

* Cafe sales dirty dataset

### General Dataset

* Netflix dataset
* LinkedIn jobs dataset

## Dataset Objectives

* Test profiling accuracy
* Evaluate tool robustness
* Simulate real-world noisy data

---

# 10. Folder Structure (Suggested)

project_root/

├── app/
│   ├── pages/
│   ├── components/
│   ├── utils/
│   ├── profiling/
│   └── comparison/
│
├── datasets/
│
├── reports/
│   ├── ydata/
│   ├── sweetviz/
│   ├── dataprep/
│   └── great_expectations/
│
├── notebooks/
│
├── docs/
│
├── requirements.txt
│
└── streamlit_app.py

---

# 11. Suggested Modules

## Module 1 — File Upload Handler

Responsibilities:

* File upload
* Validation
* Dataset preview

## Module 2 — Profiling Adapters

Responsibilities:

* Execute each profiling tool
* Standardize outputs

## Module 3 — Metrics Extractor

Responsibilities:

* Extract comparable metrics
* Normalize profiling results

## Module 4 — Visualization Engine

Responsibilities:

* Generate charts
* Build comparison dashboards

## Module 5 — Report Manager

Responsibilities:

* Save generated reports
* Export summaries

---

# 12. Research and Literature Integration

The project implementation should align with concepts from:

* Data profiling research
* Data quality evaluation
* Visualization literature
* Healthcare data management studies

The literature review should support:

* Tool selection
* Evaluation methodology
* Comparative framework definition

---

# 13. Proposed Development Plan

## Phase 1 — Research and Requirement Analysis

Duration: Initial Stage

Tasks:

* Review research papers
* Understand profiling methodologies
* Finalize evaluation criteria

---

## Phase 2 — Tool Integration

Tasks:

* Setup profiling libraries
* Build profiling adapters
* Generate sample reports

---

## Phase 3 — Dashboard Development

Tasks:

* Build Streamlit UI
* Integrate visualizations
* Add interactive components

---

## Phase 4 — Comparative Evaluation

Tasks:

* Run experiments
* Capture metrics
* Generate comparison summaries

---

## Phase 5 — Finalization

Tasks:

* Refactor code
* Add documentation
* Prepare KT sessions
* Final source code handover

---

# 14. Expected Deliverables

## Technical Deliverables

* Complete source code
* Streamlit dashboard application
* Profiling integration modules
* Comparative evaluation framework
* Documentation/setup guide

## Research Deliverables

* Comparative evaluation findings
* Experimental outputs
* Literature-backed implementation

---

# 15. Future Enhancements (Optional)

Potential future improvements:

* Support for larger datasets
* Additional profiling tools
* AI-generated profiling insights
* Automated data cleaning recommendations
* Cloud deployment
* User authentication

---

# 16. Success Criteria

The project will be considered successful if:

* Multiple profiling tools are integrated successfully
* Datasets can be profiled automatically
* Comparative evaluation is generated clearly
* Dashboard visualizations are functional
* Reports are exportable
* Research objectives are supported effectively

---

# 17. Final Notes

The implementation will prioritize:

* Simplicity
* Usability
* Clear comparative analysis
* Research-oriented experimentation
* Extensible architecture

The overall solution should function both as:

1. A practical data profiling dashboard
2. A research evaluation framework for dissertation purposes
