from __future__ import annotations

import types
from pathlib import Path

import pytest

from math2speech_docs.extraction.pdf import extract_pdf_to_markdown


def test_pdf_extraction_wrapper_calls_pymupdf4llm(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    pdf_path = tmp_path / "doc.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%fake\n")

    def _to_markdown(path: str) -> str:
        assert path.endswith("doc.pdf")
        return "# Extracted\n\n$E = mc^2$\n"

    monkeypatch.setitem(
        __import__("sys").modules,
        "pymupdf4llm",
        types.SimpleNamespace(to_markdown=_to_markdown),
    )

    md = extract_pdf_to_markdown(pdf_path)
    assert "Extracted" in md

