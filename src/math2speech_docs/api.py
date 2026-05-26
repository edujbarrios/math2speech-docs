from __future__ import annotations

from pathlib import Path

from .types.models import ConversionMode, ConversionResult, LanguageCode


def generate_prompt(markdown_text: str, *, language: LanguageCode = "en") -> str:
    """Generate an LLM prompt for rewriting math into natural language."""
    return (
        "SYSTEM: You are a document accessibility assistant.\n\n"
        f"Target language: {language}\n\n"
        "Rewrite mathematical notation into natural language while preserving Markdown structure.\n"
        "Return only the rewritten document.\n\n"
        "DOCUMENT:\n"
        f"{markdown_text}\n"
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

    # MVP placeholder: in prompt mode we simply return a prompt.
    markdown_text = path.read_text(encoding="utf-8")
    prompt = generate_prompt(markdown_text, language=language)
    return ConversionResult(
        input_path=str(path),
        language=language,
        mode=mode,
        output_markdown=markdown_text,
        prompt=prompt if mode == "prompt" else None,
    )

