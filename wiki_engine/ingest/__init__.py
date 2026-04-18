from pathlib import Path

from .base import IngestAdapter
from .csv_adapter import CSVAdapter
from .excel_adapter import ExcelAdapter
from .json_adapter import JSONAdapter


def get_adapter(file_path: Path) -> IngestAdapter:
    """Return the appropriate adapter based on file extension."""
    suffix = file_path.suffix.lower()
    if suffix in (".csv", ".tsv"):
        return CSVAdapter(file_path)
    elif suffix in (".xlsx", ".xls"):
        return ExcelAdapter(file_path)
    elif suffix == ".json":
        return JSONAdapter(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


__all__ = ["get_adapter", "IngestAdapter", "CSVAdapter", "ExcelAdapter", "JSONAdapter"]
