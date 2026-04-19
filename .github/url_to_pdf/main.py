from __future__ import annotations

import argparse
from pathlib import Path

from wiki_engine.config import get_settings
from wiki_engine.url_to_pdf import download_url_as_pdf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download a URL as a PDF and save it to the inbox directory."
    )
    parser.add_argument("url", help="URL to download")
    parser.add_argument(
        "--inbox-dir",
        type=Path,
        default=None,
        help="Destination directory (default: INBOX_DIR from .env or inbox/).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = get_settings()
    inbox_dir = args.inbox_dir or settings.inbox_dir

    print(f"Downloading {args.url} → {inbox_dir}/")
    dest = download_url_as_pdf(args.url, inbox_dir)
    print(f"Saved: {dest.resolve()}")


if __name__ == "__main__":
    main()
