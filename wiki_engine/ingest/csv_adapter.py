import csv
import io
from pathlib import Path

from .base import IngestAdapter, SourceSection

MAX_ROWS = 200
MAX_FILE_BYTES = 50 * 1024 * 1024  # 50 MB


class CSVAdapter(IngestAdapter):
    """Adapter for CSV and TSV files."""

    def parse(self) -> list[SourceSection]:
        size = self.file_path.stat().st_size
        if size > MAX_FILE_BYTES:
            raise ValueError(
                f"{self.file_path.name} is {size / 1_048_576:.1f} MB, "
                f"exceeding the {MAX_FILE_BYTES // 1_048_576} MB limit."
            )
        raw = self.file_path.read_bytes()
        text = raw.decode("utf-8-sig")  # handle BOM

        # Auto-detect delimiter
        suffix = self.file_path.suffix.lower()
        if suffix == ".tsv":
            delimiter = "\t"
        else:
            try:
                dialect = csv.Sniffer().sniff(text[:4096], delimiters=",\t|;")
                delimiter = dialect.delimiter
            except csv.Error:
                delimiter = ","

        reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
        rows = list(reader)
        columns = reader.fieldnames or []
        total_rows = len(rows)
        capped = rows[:MAX_ROWS]

        lines = [delimiter.join(str(c) for c in columns)]
        for row in capped:
            lines.append(delimiter.join(str(row.get(c, "")) for c in columns))

        note = ""
        if total_rows > MAX_ROWS:
            note = f"\n\n[Note: Showing first {MAX_ROWS} of {total_rows} rows.]"

        raw_text = "\n".join(lines) + note

        content_type = "tsv" if delimiter == "\t" else "csv"
        section = SourceSection(
            source_file=self.file_path,
            section_name=self.file_path.stem,
            content_type=content_type,
            raw_text=raw_text,
            row_count=total_rows,
            column_names=list(columns),
        )
        return [section]
