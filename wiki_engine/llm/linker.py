from __future__ import annotations

import json
import re

from wiki_engine.wiki.page import WikiPage

from .client import get_client

LINKING_SYSTEM = """\
You are a wiki cross-linking assistant. Given a new wiki page and a list of existing related pages,
identify which existing pages should be linked from the new page.

Respond with ONLY valid JSON — an array of objects:
[{"slug": "page-slug", "reason": "brief reason for the link"}]

Rules:
- Only include links that are genuinely relevant — shared topics, referenced entities, or dependencies.
- Maximum 5 links.
- Return an empty array [] if no links are appropriate.
- "slug" must exactly match one of the provided existing page slugs.
"""


def _strip_json_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def find_links(page: WikiPage, similar_pages: list[WikiPage]) -> list[dict]:
    """Return list of {slug, reason} dicts for cross-links to inject."""
    from wiki_engine.config import get_settings
    settings = get_settings()

    if not similar_pages:
        return []

    client = get_client()
    existing_list = "\n".join(f"- {p.slug}: {p.title}" for p in similar_pages)
    user_msg = (
        f"## New Page (slug: {page.slug})\nTitle: {page.title}\n\n{page.content[:1500]}\n\n"
        f"## Existing Related Pages\n{existing_list}"
    )
    response = client.messages.create(
        model=settings.linking_model,
        max_tokens=512,
        temperature=0.0,
        system=LINKING_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = _strip_json_fences(response.content[0].text)
    result = json.loads(raw)
    if not isinstance(result, list):
        return []
    # Validate slugs
    valid_slugs = {p.slug for p in similar_pages}
    return [item for item in result if isinstance(item, dict) and item.get("slug") in valid_slugs]
