from __future__ import annotations

from pathlib import Path

import typer

from math2speech_docs import convert_document, generate_prompt
from math2speech_docs.types.models import ConversionMode, LanguageCode

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def convert(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    language: LanguageCode = typer.Option("en", "--language"),
    mode: ConversionMode = typer.Option("prompt", "--mode"),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Convert a document to TTS-friendly Markdown (or emit a prompt in prompt mode)."""
    result = convert_document(input_path, language=language, mode=mode)
    out_path = output or input_path.with_suffix(f".{language}.tts.md")
    out_path.write_text(result.prompt if mode == "prompt" else result.output_markdown, encoding="utf-8")
    typer.echo(str(out_path))


@app.command()
def prompt(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    language: LanguageCode = typer.Option("en", "--language"),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Generate an LLM prompt for rewriting formulas (no network calls)."""
    markdown_text = input_path.read_text(encoding="utf-8")
    prompt_text = generate_prompt(markdown_text, language=language)
    out_path = output or input_path.with_suffix(".prompt.md")
    out_path.write_text(prompt_text, encoding="utf-8")
    typer.echo(str(out_path))


@app.command()
def detect(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
) -> None:
    """Detect whether the document appears math-heavy (placeholder)."""
    text = input_path.read_text(encoding="utf-8")
    has_dollars = "$" in text or "\\frac" in text or "\\sqrt" in text
    typer.echo("math-heavy" if has_dollars else "no-math-detected")


@app.command(name="speechify-preview")
def speechify_preview(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    language: LanguageCode = typer.Option("en", "--language"),
) -> None:
    """Preview a future TTS synthesis step (placeholder)."""
    text = input_path.read_text(encoding="utf-8")
    typer.echo(f"placeholder speechify preview ({language}): {len(text)} chars")

