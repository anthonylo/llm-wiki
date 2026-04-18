from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from wiki_engine import pipeline
from wiki_engine.config import get_settings
from wiki_engine.excel_to_markdown import dump_excel_to_markdown
from wiki_engine.csv_to_markdown import dump_csv_to_markdown

app = typer.Typer(
    name="wiki",
    help="LLM Wiki — auto-evolving wiki powered by Claude",
    add_completion=False,
)
console = Console()


@app.command()
def ingest(
    file: Path = typer.Argument(..., help="Path to the file to ingest (CSV, TSV, XLSX, XLS, JSON)"),
    force: bool = typer.Option(False, "--force", "-f", help="Re-ingest even if already processed"),
) -> None:
    """Ingest a structured data file and generate wiki pages."""
    if not file.exists():
        console.print(f"[red]Error:[/red] File not found: {file}")
        raise typer.Exit(1)

    console.print(f"\n[bold]LLM Wiki — Ingesting:[/bold] {file.resolve()}\n")

    try:
        results = pipeline.run(file, force=force)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)

    _print_results(results)


@app.command()
def watch(
    inbox: Optional[Path] = typer.Option(None, "--inbox", help="Directory to watch (default: inbox/)"),
) -> None:
    """Watch the inbox directory for new files and auto-ingest them."""
    from wiki_engine import watcher
    settings = get_settings()
    watch_dir = inbox or settings.inbox_dir
    watcher.start(watch_dir)


@app.command("excel-to-markdown")
def excel_to_markdown(
    file: Path = typer.Argument(..., help="Path to the Excel workbook to convert"),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", help="Wiki output directory (default: WIKI_DIR)."),
    sheet: Optional[str] = typer.Option(None, "--sheet", help="Optional sheet name to export."),
) -> None:
    """Convert an Excel workbook into a markdown wiki page."""
    if not file.exists():
        console.print(f"[red]Error:[/red] File not found: {file}")
        raise typer.Exit(1)

    settings = get_settings()
    wiki_dir = output_dir or settings.wiki_dir

    console.print(f"\n[bold]LLM Wiki — Excel to Markdown:[/bold] {file.resolve()}\n")
    try:
        output_path = dump_excel_to_markdown(file, wiki_dir, sheet_name=sheet)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)

    console.print(f"\n[green]Done:[/green] wrote markdown to {output_path.resolve()}\n")


@app.command("csv-to-markdown")
def csv_to_markdown(
    file: Path = typer.Argument(..., help="Path to the CSV file to convert"),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", help="Wiki output directory (default: WIKI_DIR)."),
) -> None:
    """Convert a CSV file into markdown wiki pages (one per row)."""
    if not file.exists():
        console.print(f"[red]Error:[/red] File not found: {file}")
        raise typer.Exit(1)

    settings = get_settings()
    wiki_dir = output_dir or settings.wiki_dir

    console.print(f"\n[bold]LLM Wiki — CSV to Markdown:[/bold] {file.resolve()}\n")
    try:
        output_paths = dump_csv_to_markdown(file, wiki_dir)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)

    if output_paths:
        console.print(f"\n[green]Done:[/green] wrote {len(output_paths)} markdown pages:")
        for path in output_paths:
            console.print(f"  {path.resolve()}")
    else:
        console.print(f"\n[yellow]Warning:[/yellow] No valid rows found in {file}\n")


def _print_results(results) -> None:
    table = Table(title="Ingest Results", show_header=True, header_style="bold magenta")
    table.add_column("Slug", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details")

    for r in results:
        status_color = {
            "ok": "green",
            "rejected": "red",
            "blocked": "yellow",
            "skipped": "dim",
            "error": "red",
        }.get(r.status, "white")

        details = ""
        if r.status == "ok":
            details = f"fidelity={r.fidelity_score:.2f}" if r.fidelity_score else ""
        elif r.status == "rejected":
            details = "; ".join(r.issues[:2])
        elif r.status == "blocked":
            details = f"{len(r.contradictions)} contradiction(s)"
        elif r.status == "error":
            details = r.error or ""

        table.add_row(r.slug, f"[{status_color}]{r.status.upper()}[/{status_color}]", details)

    console.print(table)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
