from __future__ import annotations

from pathlib import Path

import typer

from math2speech_docs import convert_document, generate_prompt
from math2speech_docs.detection.math_detector import detect_math
from math2speech_docs.tts import SpeechifyClient
from math2speech_docs.types.models import ConversionMode, LanguageCode, StrictnessLevel

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def convert(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    language: LanguageCode = typer.Option("en", "--language"),
    mode: ConversionMode = typer.Option("prompt", "--mode"),
    output: Path | None = typer.Option(None, "--output"),
    chunk_size: int = typer.Option(3000, "--chunk-size"),
    strictness: StrictnessLevel = typer.Option("balanced", "--strictness"),
    document_title: str | None = typer.Option(None, "--document-title"),
    include_quality_check: bool = typer.Option(False, "--include-quality-check"),
    api_base_url: str | None = typer.Option(None, "--api-base-url"),
    api_key: str | None = typer.Option(None, "--api-key"),
    model: str | None = typer.Option(None, "--model"),
) -> None:
    """Convert a document to TTS-friendly Markdown (or emit a prompt in prompt mode)."""
    result = convert_document(
        input_path,
        language=language,
        mode=mode,
        chunk_size=chunk_size,
        strictness=strictness,
        document_title=document_title,
        include_quality_check=include_quality_check,
        api_base_url=api_base_url,
        api_key=api_key,
        model=model,
    )
    out_path = output or input_path.with_suffix(f".{language}.tts.md")
    out_path.write_text(
        result.prompt if mode == "prompt" else result.output_markdown, encoding="utf-8"
    )
    typer.echo(str(out_path))


@app.command()
def prompt(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    language: LanguageCode = typer.Option("en", "--language"),
    output: Path | None = typer.Option(None, "--output"),
    strictness: StrictnessLevel = typer.Option("balanced", "--strictness"),
    document_title: str | None = typer.Option(None, "--document-title"),
    include_quality_check: bool = typer.Option(False, "--include-quality-check"),
) -> None:
    """Generate an LLM prompt for rewriting formulas (no network calls)."""
    markdown_text = input_path.read_text(encoding="utf-8")
    prompt_text = generate_prompt(
        markdown_text,
        language=language,
        strictness=strictness,
        document_title=document_title,
        include_quality_check=include_quality_check,
    )
    out_path = output or input_path.with_suffix(".prompt.md")
    out_path.write_text(prompt_text, encoding="utf-8")
    typer.echo(str(out_path))


@app.command()
def detect(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
) -> None:
    """Detect math-heavy sections and print a simple report."""
    text = input_path.read_text(encoding="utf-8")
    result = detect_math(text)
    typer.echo(result.model_dump_json(indent=2))


@app.command(name="speechify-preview")
def speechify_preview(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    language: LanguageCode = typer.Option("en", "--language"),
    voice: str = typer.Option("default", "--voice"),
) -> None:
    """Preview a future TTS synthesis step (placeholder)."""
    text = input_path.read_text(encoding="utf-8")
    client = SpeechifyClient()
    preview = client.synthesize_placeholder(text=text, voice=voice, language=language)
    typer.echo(preview.model_dump_json(indent=2))
