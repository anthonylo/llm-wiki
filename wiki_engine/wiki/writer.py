from __future__ import annotations

from pathlib import Path

from .page import WikiPage


def write(page: WikiPage, wiki_dir: Path) -> Path:
    """Write the wiki page to disk, injecting the Related Pages section.

    If page.category is set, writes to wiki/{category}/{slug}.md.
    Otherwise falls back to wiki/{slug}.md.
    """
    target_dir = wiki_dir / page.category if page.category else wiki_dir
    # Resolve to absolute paths and confirm target_dir is inside wiki_dir
    try:
        resolved_target = target_dir.resolve()
        resolved_wiki = wiki_dir.resolve()
        resolved_target.relative_to(resolved_wiki)
    except ValueError:
        raise ValueError(
            f"Unsafe page category {page.category!r} would write outside wiki directory."
        )
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / f"{page.slug}.md"

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
