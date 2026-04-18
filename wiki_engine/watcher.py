from __future__ import annotations

import time
from pathlib import Path

from rich.console import Console
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileMovedEvent
from watchdog.observers import Observer

from wiki_engine import pipeline

console = Console()

SUPPORTED_EXTENSIONS = {".csv", ".tsv", ".xlsx", ".xls", ".json", ".pdf"}


class InboxHandler(FileSystemEventHandler):
    def on_created(self, event: FileCreatedEvent) -> None:
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            console.print(f"\n[bold cyan]Inbox:[/bold cyan] New file detected: {path.name}")
            try:
                results = pipeline.run(path)
                _summarize(results)
            except Exception as exc:
                console.print(f"[red]Error processing {path.name}:[/red] {exc}")

    def on_moved(self, event: FileMovedEvent) -> None:
        # Handle files moved into the inbox
        path = Path(event.dest_path)
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            console.print(f"\n[bold cyan]Inbox:[/bold cyan] File moved in: {path.name}")
            try:
                results = pipeline.run(path)
                _summarize(results)
            except Exception as exc:
                console.print(f"[red]Error processing {path.name}:[/red] {exc}")


def _summarize(results) -> None:
    ok = sum(1 for r in results if r.status == "ok")
    console.print(f"  Done: {ok}/{len(results)} section(s) written successfully.")


def start(inbox_dir: Path) -> None:
    inbox_dir.mkdir(parents=True, exist_ok=True)
    observer = Observer()
    observer.schedule(InboxHandler(), str(inbox_dir), recursive=False)
    observer.start()
    console.print(f"[bold green]Watching[/bold green] {inbox_dir.resolve()} — drop files to auto-ingest. Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
