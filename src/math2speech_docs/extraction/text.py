from __future__ import annotations

from pathlib import Path


def load_text(path: str | Path, *, document_title: str | None = None) -> str:
    text = Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")
    if document_title:
        return f"# {document_title}\n\n{text}\n"
    return text
