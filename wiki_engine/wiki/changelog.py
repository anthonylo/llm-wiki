from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def append(
    wiki_dir: Path,
    slug: str,
    status: str,
    source_file: str,
    detail: str = "",
) -> None:
    """Append one entry to CHANGELOG.md."""
    changelog_path = wiki_dir / "CHANGELOG.md"

    if not changelog_path.exists():
        changelog_path.write_text("# Changelog\n\n", encoding="utf-8")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    status_upper = status.upper()
    line = f"- `{timestamp}` **{status_upper}** `{slug}` (source: `{source_file}`)"
    if detail:
        line += f" — {detail}"

    existing = changelog_path.read_text(encoding="utf-8")
    # Insert after header
    header_end = existing.find("\n\n") + 2
    new_content = existing[:header_end] + line + "\n" + existing[header_end:]
    changelog_path.write_text(new_content, encoding="utf-8")
