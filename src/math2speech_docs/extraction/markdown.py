from __future__ import annotations

from pathlib import Path


def load_markdown(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def normalize_markdown(markdown_text: str) -> str:
    # MVP: keep as-is; postprocessing hooks can be added later.
    return markdown_text.replace("\r\n", "\n")
