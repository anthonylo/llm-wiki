from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wiki_engine.ingest.base import SourceSection


@dataclass
class WikiPage:
    slug: str
    title: str
    source_section: "SourceSection"
    content: str                    # Full Markdown content
    links: list[dict] = field(default_factory=list)  # [{slug, reason}]


@dataclass
class ProcessingResult:
    slug: str
    status: str                     # "ok", "rejected", "blocked", "skipped", "error"
    wiki_path: str | None = None
    fidelity_score: float | None = None
    issues: list[str] = field(default_factory=list)
    contradictions: list[dict] = field(default_factory=list)
    error: str | None = None


class ValidationError(Exception):
    """Raised when fidelity validation fails after regeneration."""
    def __init__(self, slug: str, score: float, issues: list[str]) -> None:
        self.slug = slug
        self.score = score
        self.issues = issues
        super().__init__(f"Fidelity validation failed for '{slug}': score={score:.2f}, issues={issues}")


class ConsistencyError(Exception):
    """Raised when a consistency contradiction is found."""
    def __init__(self, slug: str, contradictions: list[dict]) -> None:
        self.slug = slug
        self.contradictions = contradictions
        super().__init__(f"Consistency check failed for '{slug}': {len(contradictions)} contradiction(s)")
