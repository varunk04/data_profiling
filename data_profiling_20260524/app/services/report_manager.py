"""Report saving and export utilities."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd

from app.comparison.metrics_normalizer import metrics_to_csv_rows
from app.profiling.base_profiler import ProfilingResult
from app.utils.constants import REPORTS_DIR


class ReportManager:
    """Manage report persistence and export."""

    def __init__(self, reports_dir: Path | None = None) -> None:
        self.reports_dir = reports_dir or REPORTS_DIR
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def export_metrics_csv(self, results: dict[str, ProfilingResult]) -> bytes:
        """Export normalized metrics as CSV bytes."""
        df = metrics_to_csv_rows(results)
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue()

    def export_metrics_json(self, results: dict[str, ProfilingResult]) -> bytes:
        """Export metrics summary as JSON bytes."""
        payload: dict[str, Any] = {}
        for tool_key, result in results.items():
            payload[tool_key] = {
                "success": result.success,
                "error_message": result.error_message,
                "metrics": result.metrics.to_dict(),
            }
        return json.dumps(payload, indent=2, default=str).encode("utf-8")

    def export_comparison_json(self, comparison: dict[str, Any]) -> bytes:
        """Export comparison results as JSON bytes."""
        serializable: dict[str, Any] = {}
        for key, value in comparison.items():
            if isinstance(value, pd.DataFrame):
                serializable[key] = value.to_dict(orient="records")
            else:
                serializable[key] = value
        return json.dumps(serializable, indent=2, default=str).encode("utf-8")

    def read_report_file(self, path: str | Path) -> bytes | None:
        """Read a report file for download."""
        file_path = Path(path)
        if file_path.exists() and file_path.is_file():
            return file_path.read_bytes()
        return None

    def list_reports_for_tool(self, tool_key: str) -> list[Path]:
        """List saved reports for a given tool."""
        tool_dir = self.reports_dir / tool_key
        if not tool_dir.exists():
            return []
        return sorted(tool_dir.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
