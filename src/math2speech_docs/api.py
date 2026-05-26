from __future__ import annotations

from pathlib import Path

from .extraction.markdown import load_markdown, normalize_markdown
from .extraction.pdf import extract_pdf_to_markdown
from .extraction.text import load_text
from .prompts.renderer import PromptRenderer
from .types.models import ConversionMode, ConversionResult, DocumentType, LanguageCode, StrictnessLevel


def generate_prompt(
    markdown_text: str,
    *,
    language: LanguageCode = "en",
    strictness: StrictnessLevel = "balanced",
    document_title: str | None = None,
    include_quality_check: bool = False,
) -> str:
    """Generate an LLM prompt for rewriting math into natural language (no network calls)."""
    renderer = PromptRenderer.default()
    return renderer.render_rewrite_document(
        markdown_text=markdown_text,
        language=language,
        strictness=strictness,
        document_title=document_title,
        include_quality_check=include_quality_check,
    )


def convert_document(
    input_path: str | Path,
    *,
    language: LanguageCode = "en",
    mode: ConversionMode = "prompt",
) -> ConversionResult:
    """Convert a supported document to TTS-friendly Markdown.

    Note: the full pipeline is implemented in internal modules; this function is the stable API.
    """
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(str(path))

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        document_type: DocumentType = "pdf"
        markdown_text = extract_pdf_to_markdown(path)
    elif suffix in {".md", ".markdown"}:
        document_type = "markdown"
        markdown_text = load_markdown(path)
    else:
        document_type = "text"
        markdown_text = load_text(path)

    markdown_text = normalize_markdown(markdown_text)
    prompt = generate_prompt(markdown_text, language=language)
    return ConversionResult(
        input_path=str(path),
        document_type=document_type,
        language=language,
        mode=mode,
        output_markdown=markdown_text,
        prompt=prompt if mode == "prompt" else None,
    )
