from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SourceSection:
    """A logical section of source data to be converted into a wiki page."""
    source_file: Path
    section_name: str          # e.g. sheet name, "root", top-level key
    content_type: str          # "csv", "tsv", "excel", "json"
    raw_text: str              # Pre-formatted text representation of the data
    row_count: int = 0
    column_names: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    @property
    def slug(self) -> str:
        """Generate a URL-safe slug for this section."""
        base = self.source_file.stem
        name = self.section_name.lower().replace(" ", "-")
        # Remove non-alphanumeric chars except hyphens
        import re
        name = re.sub(r"[^a-z0-9\-]", "", name)
        base = re.sub(r"[^a-z0-9\-]", "", base.lower().replace(" ", "-"))
        if name and name != base:
            return f"{base}-{name}"
        return base


class IngestAdapter(ABC):
    """Abstract base class for all file ingest adapters."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    @abstractmethod
    def parse(self) -> list[SourceSection]:
        """Parse the file and return a list of SourceSection objects."""
        ...
