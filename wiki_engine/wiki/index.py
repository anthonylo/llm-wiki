from __future__ import annotations

from pathlib import Path


def update(wiki_dir: Path) -> None:
    """Rebuild INDEX.md from all .md files in wiki_dir."""
    pages = sorted(p for p in wiki_dir.glob("*.md") if p.name not in ("INDEX.md", "CHANGELOG.md"))
    lines = [
        "# Wiki Index",
        "",
        f"Total pages: {len(pages)}",
        "",
        "| Page | File |",
        "|------|------|",
    ]
    for page_path in pages:
        title = _extract_title(page_path)
        lines.append(f"| {title} | [{page_path.name}]({page_path.name}) |")

    index_path = wiki_dir / "INDEX.md"
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _extract_title(page_path: Path) -> str:
    """Try to read the title from YAML front-matter or first H1."""
    try:
        text = page_path.read_text(encoding="utf-8")
    except OSError:
        return page_path.stem

    lines = text.splitlines()
    in_frontmatter = False
    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter and line.startswith("title:"):
            return line.split("title:", 1)[1].strip()
        if not in_frontmatter and line.startswith("# "):
            return line[2:].strip()

    return page_path.stem
