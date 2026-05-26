from __future__ import annotations

from pathlib import Path


class PDFExtractionError(RuntimeError):
    pass


def extract_pdf_to_markdown(path: str | Path) -> str:
    pdf_path = Path(path)
    try:
        import pymupdf4llm  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "PDF extraction requires pymupdf4llm. Install with `pip install -e '.[pdf]'`."
        ) from exc

    if not pdf_path.exists():
        raise FileNotFoundError(str(pdf_path))

    try:
        to_md = getattr(pymupdf4llm, "to_markdown")
    except AttributeError as exc:  # pragma: no cover
        raise PDFExtractionError("pymupdf4llm is installed but missing to_markdown().") from exc

    try:
        md = to_md(str(pdf_path))
    except Exception as exc:  # pragma: no cover
        raise PDFExtractionError(f"Failed to extract PDF: {pdf_path}") from exc

    return str(md).replace("\r\n", "\n")

