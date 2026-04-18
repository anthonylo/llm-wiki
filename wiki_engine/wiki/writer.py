from __future__ import annotations

from pathlib import Path

from .page import WikiPage


def write(page: WikiPage, wiki_dir: Path) -> Path:
    """Write the wiki page to disk, injecting the Related Pages section."""
    wiki_dir.mkdir(parents=True, exist_ok=True)
    out_path = wiki_dir / f"{page.slug}.md"

    content = page.content

    # Inject Related Pages section if there are links
    if page.links:
        related = "\n\n## Related Pages\n"
        for link in page.links:
            slug = link["slug"]
            reason = link.get("reason", "")
            related += f"- [{slug}]({slug}.md) — {reason}\n"
        content = content.rstrip() + related

    out_path.write_text(content, encoding="utf-8")
    return out_path
