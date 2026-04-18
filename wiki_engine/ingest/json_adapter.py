import json
from pathlib import Path

from .base import IngestAdapter, SourceSection

MAX_ROWS = 200


def _format_value(v, max_rows: int = MAX_ROWS) -> tuple[str, int]:
    """Return (formatted_text, row_count) for a JSON value."""
    if isinstance(v, list):
        total = len(v)
        capped = v[:max_rows]
        note = f"\n\n[Note: Showing first {max_rows} of {total} items.]" if total > max_rows else ""
        if capped and isinstance(capped[0], dict):
            # Table-like: extract header from union of all keys
            keys: list[str] = []
            for row in capped:
                for k in row.keys():
                    if k not in keys:
                        keys.append(k)
            lines = ["\t".join(keys)]
            for row in capped:
                lines.append("\t".join(str(row.get(k, "")) for k in keys))
            return "\n".join(lines) + note, total
        else:
            lines = [str(item) for item in capped]
            return "\n".join(lines) + note, total
    elif isinstance(v, dict):
        lines = [f"{k}: {json.dumps(val, ensure_ascii=False)}" for k, val in v.items()]
        return "\n".join(lines), len(v)
    else:
        return str(v), 1


class JSONAdapter(IngestAdapter):
    """Adapter for JSON files."""

    def parse(self) -> list[SourceSection]:
        data = json.loads(self.file_path.read_text(encoding="utf-8"))
        sections: list[SourceSection] = []

        if isinstance(data, list):
            raw_text, row_count = _format_value(data)
            sections.append(SourceSection(
                source_file=self.file_path,
                section_name=self.file_path.stem,
                content_type="json",
                raw_text=raw_text,
                row_count=row_count,
                column_names=[],
            ))
        elif isinstance(data, dict):
            for key, value in data.items():
                raw_text, row_count = _format_value(value)
                sections.append(SourceSection(
                    source_file=self.file_path,
                    section_name=key,
                    content_type="json",
                    raw_text=raw_text,
                    row_count=row_count,
                    column_names=[],
                    metadata={"top_level_key": key},
                ))
        else:
            # Scalar — treat whole file as one section
            sections.append(SourceSection(
                source_file=self.file_path,
                section_name=self.file_path.stem,
                content_type="json",
                raw_text=str(data),
                row_count=1,
            ))

        return sections
