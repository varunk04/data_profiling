"""File upload validation and dataset loading."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd

from app.utils.constants import MAX_PREVIEW_ROWS, SUPPORTED_EXTENSIONS


class DatasetValidationError(Exception):
    """Raised when uploaded file fails validation."""


def validate_file_extension(filename: str) -> str:
    """Validate and return normalized file extension."""
    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise DatasetValidationError(
            f"Unsupported file type '{ext}'. Supported formats: {supported}"
        )
    return ext


def load_dataset(uploaded_file: Any) -> pd.DataFrame:
    """
    Load dataset from Streamlit uploaded file object.

    Args:
        uploaded_file: Streamlit UploadedFile instance.

    Returns:
        Loaded pandas DataFrame.

    Raises:
        DatasetValidationError: On validation or parsing failures.
    """
    if uploaded_file is None:
        raise DatasetValidationError("No file provided.")

    filename = uploaded_file.name
    ext = validate_file_extension(filename)

    try:
        file_bytes = uploaded_file.getvalue()
        if not file_bytes:
            raise DatasetValidationError("Uploaded file is empty.")

        buffer = BytesIO(file_bytes)

        if ext == ".csv":
            df = pd.read_csv(buffer)
        elif ext in {".xlsx", ".xls"}:
            df = pd.read_excel(buffer)
        else:
            raise DatasetValidationError(f"Cannot parse file type: {ext}")

    except DatasetValidationError:
        raise
    except Exception as exc:
        raise DatasetValidationError(f"Failed to parse file: {exc}") from exc

    if df.empty:
        raise DatasetValidationError("Dataset contains no rows.")

    if df.columns.empty:
        raise DatasetValidationError("Dataset contains no columns.")

    return df


def extract_dataset_metadata(df: pd.DataFrame, filename: str) -> dict[str, Any]:
    """Extract standardized metadata from a DataFrame."""
    missing_counts = df.isnull().sum()
    total_cells = df.shape[0] * df.shape[1]
    total_missing = int(missing_counts.sum())

    dtype_counts = df.dtypes.astype(str).value_counts().to_dict()

    return {
        "filename": filename,
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "total_missing": total_missing,
        "missing_percentage": round((total_missing / total_cells * 100) if total_cells else 0, 2),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "dtype_counts": dtype_counts,
        "missing_by_column": missing_counts.to_dict(),
        "null_percentage_by_column": {
            col: round((count / len(df) * 100) if len(df) else 0, 2)
            for col, count in missing_counts.items()
        },
    }


def get_preview_df(df: pd.DataFrame, n_rows: int = MAX_PREVIEW_ROWS) -> pd.DataFrame:
    """Return a preview slice of the dataset."""
    return df.head(n_rows).copy()
