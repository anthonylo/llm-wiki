from __future__ import annotations

import time
from pathlib import Path

from rich.console import Console
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileMovedEvent
from watchdog.observers import Observer

from wiki_engine import pipeline

console = Console()

SUPPORTED_EXTENSIONS = {".csv", ".tsv", ".xlsx", ".xls", ".json", ".pdf"}
MAX_INBOX_FILE_BYTES = 100 * 1024 * 1024  # 100 MB


def _validate_inbox_file(path: Path) -> str | None:
    """Return an error message if the file should be rejected, else None."""
    if path.is_symlink():
        return f"{path.name} is a symbolic link and will not be processed."
    try:
        size = path.stat().st_size
    except OSError as exc:
        return f"Could not stat {path.name}: {exc}"
    if size > MAX_INBOX_FILE_BYTES:
        return (
            f"{path.name} is {size / 1_048_576:.1f} MB, "
            f"exceeding the {MAX_INBOX_FILE_BYTES // 1_048_576} MB inbox limit."
        )
    return None


class InboxHandler(FileSystemEventHandler):
    def _process(self, path: Path) -> None:
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return
        error = _validate_inbox_file(path)
        if error:
            console.print(f"[yellow]Skipped:[/yellow] {error}")
            return
        try:
            results = pipeline.run(path)
            _summarize(results)
        except Exception as exc:
            console.print(f"[red]Error processing {path.name}:[/red] {exc}")

    def on_created(self, event: FileCreatedEvent) -> None:
        if event.is_directory:
            return
        path = Path(event.src_path)
        console.print(f"\n[bold cyan]Inbox:[/bold cyan] New file detected: {path.name}")
        self._process(path)

    def on_moved(self, event: FileMovedEvent) -> None:
        path = Path(event.dest_path)
        console.print(f"\n[bold cyan]Inbox:[/bold cyan] File moved in: {path.name}")
        self._process(path)


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
