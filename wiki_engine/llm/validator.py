from __future__ import annotations

import json
import re

from wiki_engine.wiki.page import WikiPage, ValidationError, ConsistencyError

from .client import get_client

FIDELITY_SYSTEM = """\
You are a data-accuracy auditor for a wiki system. Given the source data and a generated wiki page,
determine whether the wiki page faithfully and accurately represents the source data.

Respond with ONLY valid JSON in this exact format:
{"passed": true|false, "score": 0.0-1.0, "issues": ["issue description", ...]}

Rules:
- "passed" is true if score >= 0.85 and there are no critical errors.
- "score" is a float from 0.0 (completely wrong) to 1.0 (perfect).
- "issues" lists specific inaccuracies, omissions, or fabrications. Empty array if none.
- Be strict: hallucinated data, wrong numbers, or missing columns must lower the score.
"""

CONSISTENCY_SYSTEM = """\
You are a consistency auditor for a wiki knowledge base. Given a new draft wiki page and a set of
existing related wiki pages, identify any factual contradictions.

Respond with ONLY valid JSON in this exact format:
{"passed": true|false, "contradictions": [{"draft_claim": "...", "existing_page": "slug", "existing_claim": "...", "explanation": "..."}]}

Rules:
- "passed" is true if there are NO contradictions.
- List only genuine factual contradictions, not stylistic differences.
- "existing_page" should be the slug (filename without .md) of the contradicting page.
"""


def _strip_json_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def check_fidelity(page: WikiPage) -> dict:
    """Check that the wiki page faithfully represents the source data. Returns fidelity result dict."""
    from wiki_engine.config import get_settings
    settings = get_settings()

    client = get_client()
    user_msg = (
        f"## Source Data\n{page.source_section.raw_text}\n\n"
        f"## Generated Wiki Page\n{page.content}"
    )
    response = client.messages.create(
        model=settings.validation_model,
        max_tokens=1024,
        temperature=0.0,
        system=FIDELITY_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = _strip_json_fences(response.content[0].text)
    result = json.loads(raw)
    return result


def check_consistency(page: WikiPage, similar_pages: list[WikiPage]) -> dict:
    """Check the draft page for contradictions against existing pages."""
    from wiki_engine.config import get_settings
    settings = get_settings()

    if not similar_pages:
        return {"passed": True, "contradictions": []}

    client = get_client()
    existing_section = "\n\n".join(
        f"### Page: {p.slug}\n{p.content[:2000]}" for p in similar_pages
    )
    user_msg = (
        f"## New Draft Page (slug: {page.slug})\n{page.content}\n\n"
        f"## Existing Related Pages\n{existing_section}"
    )
    response = client.messages.create(
        model=settings.validation_model,
        max_tokens=1024,
        temperature=0.0,
        system=CONSISTENCY_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = _strip_json_fences(response.content[0].text)
    result = json.loads(raw)
    return result
