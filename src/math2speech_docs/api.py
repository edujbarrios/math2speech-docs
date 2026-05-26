from __future__ import annotations

from pathlib import Path

from .extraction.markdown import load_markdown, normalize_markdown
from .extraction.pdf import extract_pdf_to_markdown
from .extraction.text import load_text
from .prompts.renderer import PromptRenderer
from .chunking.chunker import chunk_markdown
from .conversion.postprocess import postprocess_markdown
from .conversion.rule_based import rewrite_markdown_math
from .llm.openai_compatible import OpenAICompatibleClient
from .types.models import (
    ConversionMode,
    ConversionResult,
    DocumentType,
    LanguageCode,
    StrictnessLevel,
)


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
    chunk_size: int = 3000,
    strictness: StrictnessLevel = "balanced",
    document_title: str | None = None,
    include_quality_check: bool = False,
    api_base_url: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
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

    chunks = chunk_markdown(markdown_text, chunk_size=chunk_size)
    prompt = generate_prompt(
        markdown_text,
        language=language,
        strictness=strictness,
        document_title=document_title,
        include_quality_check=include_quality_check,
    )

    if mode == "rule-based":
        output = rewrite_markdown_math(markdown_text, language=language)
        output = postprocess_markdown(output)
    elif mode == "llm":
        renderer = PromptRenderer.default()
        system = renderer.render_system(language=language, strictness=strictness)
        base_url = api_base_url or "https://api.llm7.io/v1"
        client = OpenAICompatibleClient(api_base_url=base_url, api_key=api_key, model=model)
        rewritten_chunks: list[str] = []
        for chunk in chunks:
            user = renderer.env.get_template("rewrite_chunk.j2").render(
                chunk_index=chunk.metadata.index,
                chunk_markdown=chunk.markdown,
            )
            rewritten_chunks.append(client.rewrite_markdown(system_prompt=system, user_prompt=user))
        output = postprocess_markdown("\n\n".join(rewritten_chunks))
    else:
        output = markdown_text

    return ConversionResult(
        input_path=str(path),
        document_type=document_type,
        language=language,
        mode=mode,
        output_markdown=output,
        prompt=prompt if mode == "prompt" else None,
        chunks=chunks,
    )
