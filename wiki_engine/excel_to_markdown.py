from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import openpyxl

MAX_PREVIEW_ROWS = 5


def _slugify(text: str) -> str:
    text = text.strip().lower().replace(" ", "-")
    text = re.sub(r"[^a-z0-9\-]", "", text)
    return text or "sheet"


def _render_markdown_table(header: list[str], rows: list[list[str]]) -> str:
    if not header:
        return ""

    lines = ["| " + " | ".join(header) + " |"]
    lines.append("| " + " | ".join("---" for _ in header) + " |")
    for row in rows:
        normalized = [str(cell or "") for cell in row]
        while len(normalized) < len(header):
            normalized.append("")
        lines.append("| " + " | ".join(normalized[: len(header)]) + " |")
    return "\n".join(lines)


def _format_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _read_sheet_data(sheet) -> tuple[list[str], list[list[str]]]:
    rows = [list(row) for row in sheet.iter_rows(values_only=True)]
    non_empty = [row for row in rows if any(cell is not None and str(cell).strip() != "" for cell in row)]
    if not non_empty:
        return [], []

    header = [str(cell).strip() if cell is not None else "" for cell in non_empty[0]]
    data_rows = [[_format_value(cell) for cell in row] for row in non_empty[1:]]
    return header, data_rows


def dump_excel_to_markdown(
    file_path: Path,
    wiki_dir: Path,
    sheet_name: str | None = None,
    max_preview_rows: int = MAX_PREVIEW_ROWS,
) -> Path:
    """Read an Excel workbook and write a markdown summary page to the wiki."""
    workbook = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    workbook_name = file_path.stem
    workbook_slug = _slugify(workbook_name)

    sections: list[str] = []
    sheet_names: list[str] = []

    for name in workbook.sheetnames:
        if sheet_name is not None and name != sheet_name:
            continue
        header, data_rows = _read_sheet_data(workbook[name])
        if not header:
            continue

        sheet_slug = _slugify(name)
        sheet_names.append(name)
        total_rows = len(data_rows)
        preview_rows = data_rows[:max_preview_rows]

        sections.append(f"### {name}\n")
        sections.append(f"- **Rows**: {total_rows}")
        sections.append(f"- **Columns**: {len(header)}")
        sections.append(f"- **Column names**: {', '.join(header) if header else 'None'}\n")

        if preview_rows:
            sections.append("#### Data preview\n")
            sections.append(_render_markdown_table(header, preview_rows))
            sections.append("\n")

        if total_rows > max_preview_rows:
            sections.append(f"[Note: Showing first {max_preview_rows} of {total_rows} rows.]\n")

    workbook.close()

    if not sections:
        raise ValueError(f"No non-empty sheets found in {file_path}")

    tags = ["excel", workbook_slug]
    if sheet_name:
        tags.append(_slugify(sheet_name))

    content_lines = [
        "---",
        f"title: {workbook_name}",
        f"tags: [{', '.join(tags)}]",
        "sources:",
        f"  - \"{file_path.name}\"",
        "---",
        "",
        "## Summary",
        "",
        f"This page summarizes the workbook `{file_path.name}` and its sheet data in markdown form.",
        "",
        "## Explanation",
        "",
        f"The workbook contains {len(sheet_names)} sheet(s): {', '.join(sheet_names)}.",
        "",
        *sections,
        "## Related Pages",
        "",
        "- [[excel]] — Excel workbook and sheet summaries",
        "",
        "## Contradictions",
        "",
        "- None noted.",
    ]

    output_dir = wiki_dir / "excel"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{workbook_slug}.md"
    output_path.write_text("\n".join(content_lines).strip() + "\n", encoding="utf-8")

    return output_path
