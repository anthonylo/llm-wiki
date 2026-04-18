from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from rich.console import Console

from wiki_engine.config import get_settings
from wiki_engine.ingest import get_adapter
from wiki_engine.ingest.base import SourceSection
from wiki_engine.llm import generator, validator, linker
from wiki_engine.embeddings import store as emb_store
from wiki_engine.wiki import writer, index, changelog
from wiki_engine.wiki.page import WikiPage, ProcessingResult, ValidationError, ConsistencyError

console = Console()


def _compute_hash(file_path: Path) -> str:
    h = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _hash_path(file_path: Path, processed_dir: Path) -> Path:
    return processed_dir / f"{file_path.name}.hash"


def _is_processed(file_path: Path, processed_dir: Path) -> bool:
    hp = _hash_path(file_path, processed_dir)
    if not hp.exists():
        return False
    stored = hp.read_text().strip()
    current = _compute_hash(file_path)
    return stored == current


def _mark_processed(file_path: Path, processed_dir: Path) -> None:
    processed_dir.mkdir(parents=True, exist_ok=True)
    _hash_path(file_path, processed_dir).write_text(_compute_hash(file_path))


def _load_similar_pages(similar_data: list[dict], wiki_dir: Path) -> list[WikiPage]:
    """Load WikiPage stubs from similar page metadata returned by embedding store."""
    from wiki_engine.ingest.base import SourceSection as SS
    pages = []
    for item in similar_data:
        stub_section = SS(
            source_file=Path(item["slug"]),
            section_name=item["slug"],
            content_type="existing",
            raw_text="",
        )
        pages.append(WikiPage(
            slug=item["slug"],
            title=item["title"],
            source_section=stub_section,
            content=item["content"],
        ))
    return pages


def _archive_file(file_path: Path, archive_dir: Path) -> None:
    """Move a source file to the archive directory after successful processing."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / file_path.name
    if dest.exists():
        # If a file with same name already exists, suffix with a counter
        stem, suffix = file_path.stem, file_path.suffix
        counter = 1
        while dest.exists():
            dest = archive_dir / f"{stem}.{counter}{suffix}"
            counter += 1
    shutil.move(str(file_path), dest)
    console.print(f"  [dim]Archived[/dim] {file_path.name} → {dest}")


def run(file_path: Path, force: bool = False) -> list[ProcessingResult]:
    """Run the full ingestion pipeline for a single file. Returns one result per section."""
    settings = get_settings()
    settings.wiki_dir.mkdir(parents=True, exist_ok=True)
    settings.store_dir.mkdir(parents=True, exist_ok=True)
    settings.processed_dir.mkdir(parents=True, exist_ok=True)
    settings.archive_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Deduplication
    if not force and _is_processed(file_path, settings.processed_dir):
        console.print(f"[yellow]SKIP[/yellow] {file_path.name} (already processed; use --force to re-ingest)")
        return [ProcessingResult(slug=file_path.stem, status="skipped")]

    # Step 2: Parse
    console.print(f"[cyan]Parsing[/cyan] {file_path.name}…")
    adapter = get_adapter(file_path)
    sections = adapter.parse()
    console.print(f"  → {len(sections)} section(s) found")

    results: list[ProcessingResult] = []

    for section in sections:
        result = _process_section(section, settings)
        results.append(result)

    # Mark file as processed and archive only if no blocking errors occurred
    statuses = {r.status for r in results}
    if "blocked" not in statuses and "error" not in statuses:
        _mark_processed(file_path, settings.processed_dir)
        _archive_file(file_path, settings.archive_dir)

    # Update INDEX.md
    index.update(settings.wiki_dir)
    return results


def _process_section(section: SourceSection, settings) -> ProcessingResult:
    slug = section.slug
    console.print(f"  [bold]Section:[/bold] {section.section_name} → {slug}")

    # Step 3: Generate
    console.print(f"    [dim]Generating markdown…[/dim]")
    page = generator.generate(section)

    # Step 4: Fidelity check
    console.print(f"    [dim]Validating fidelity…[/dim]")
    fidelity = validator.check_fidelity(page)
    if not fidelity.get("passed", False):
        issues = fidelity.get("issues", [])
        feedback = "\n".join(f"- {i}" for i in issues)
        console.print(f"    [yellow]Fidelity failed (score={fidelity.get('score', 0):.2f}), regenerating…[/yellow]")

        # Regenerate once with feedback
        page = generator.generate(section, feedback=feedback)
        fidelity2 = validator.check_fidelity(page)
        if not fidelity2.get("passed", False):
            issues2 = fidelity2.get("issues", [])
            score2 = fidelity2.get("score", 0.0)
            console.print(f"    [red]REJECTED[/red] {slug} (score={score2:.2f})")
            changelog.append(
                settings.wiki_dir,
                slug=slug,
                status="rejected",
                source_file=section.source_file.name,
                detail=f"score={score2:.2f}; " + "; ".join(issues2[:3]),
            )
            return ProcessingResult(
                slug=slug,
                status="rejected",
                fidelity_score=score2,
                issues=issues2,
            )
        fidelity = fidelity2

    # Step 5: Query similar pages
    similar_data = emb_store.query_similar(
        content=page.content,
        top_k=5,
        store_dir=settings.store_dir,
        exclude_slug=slug,
    )
    similar_pages = _load_similar_pages(similar_data, settings.wiki_dir)

    # Step 6: Consistency check
    console.print(f"    [dim]Checking consistency ({len(similar_pages)} similar pages)…[/dim]")
    consistency = validator.check_consistency(page, similar_pages)
    if not consistency.get("passed", True):
        contradictions = consistency.get("contradictions", [])
        console.print(f"    [red]BLOCKED[/red] {slug} ({len(contradictions)} contradiction(s))")
        detail = "; ".join(
            f"[{c.get('existing_page')}] {c.get('explanation', '')}"
            for c in contradictions[:2]
        )
        changelog.append(
            settings.wiki_dir,
            slug=slug,
            status="blocked",
            source_file=section.source_file.name,
            detail=detail,
        )
        return ProcessingResult(
            slug=slug,
            status="blocked",
            contradictions=contradictions,
        )

    # Step 7: Classify category
    console.print(f"    [dim]Classifying category…[/dim]")
    page.category = section.category or linker.classify_category(page)
    console.print(f"    [dim]Category:[/dim] {page.category}")

    # Step 7b: Cross-links
    console.print(f"    [dim]Finding cross-links…[/dim]")
    links = linker.find_links(page, similar_pages)
    page.links = links

    # Step 8: Write wiki page
    out_path = writer.write(page, settings.wiki_dir)
    console.print(f"    [green]WRITTEN[/green] {out_path}")

    # Step 9: Upsert embeddings
    emb_store.upsert(
        slug=slug,
        title=page.title,
        content=page.content,
        store_dir=settings.store_dir,
    )

    # Step 10: Changelog
    changelog.append(
        settings.wiki_dir,
        slug=slug,
        status="ok",
        source_file=section.source_file.name,
        detail=f"fidelity={fidelity.get('score', 1.0):.2f}; links={len(links)}",
    )

    return ProcessingResult(
        slug=slug,
        status="ok",
        wiki_path=str(out_path),
        fidelity_score=fidelity.get("score", 1.0),
    )
