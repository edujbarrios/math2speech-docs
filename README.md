# math2speech-docs

Convert math-heavy PDFs and Markdown documents into TTS-friendly Markdown for accessibility and AI workflows.

Created by edujbarrios - Eduardo J. Barrios.

## Motivation

Screen readers, TTS engines, audiobook workflows, and AI/LLM preprocessing often struggle with raw mathematical notation (LaTeX, inline formulas, and dense symbolic expressions). This project keeps your document structure intact while rewriting formulas into natural language.

## What It Does

`math2speech-docs` is a local-first document accessibility pipeline:

PDF / Markdown / TXT  
→ extract or load document  
→ normalize to Markdown  
→ split into chunks  
→ detect math-heavy sections  
→ generate Jinja2 prompt for formula rewriting  
→ optionally send prompt to an OpenAI-compatible API  
→ optionally apply a simple offline rule-based fallback  
→ export TTS-friendly Markdown

## Architecture (High Level)

```
src/math2speech_docs/
  extraction/   (pdf, markdown, text)
  chunking/     (chunker)
  detection/    (math detector)
  prompts/      (Jinja2 templates + renderer)
  conversion/   (rule-based + postprocess)
  llm/          (OpenAI-compatible client)
  tts/          (Speechify placeholder connector)
  evaluation/   (simple metrics)
  cli/          (Typer commands)
```

## Features

- PDF → Markdown extraction via `pymupdf4llm` (PyMuPDF4LLM)
- Markdown and plain text input support
- Chunking for long documents
- Math expression detection
- Prompt generation (offline) using Jinja2 templates
- Optional OpenAI-compatible LLM mode (provider-agnostic)
- Offline rule-based fallback for common expressions
- English and Spanish output modes
- Speechify connector placeholder + `speechify-preview` command
- Simple evaluation metrics module

## Install

```bash
git clone https://github.com/edujbarrios/math2speech-docs.git
cd math2speech-docs
pip install -e .
```

Development install:

```bash
pip install -e ".[dev]"
```

Optional extras:

```bash
pip install -e ".[pdf]"   # PDF extraction dependency
pip install -e ".[llm]"   # OpenAI Python SDK for LLM mode
```

## CLI Usage

Convert documents:

```bash
math2speech-docs convert input.pdf --language en --output output.md
math2speech-docs convert notes.md --language es --output notes.tts.md
```

Generate a prompt (offline, no API calls):

```bash
math2speech-docs prompt input.md --language en --output prompt.md
```

Detect math:

```bash
math2speech-docs detect input.md
```

LLM mode (requires a valid OpenAI-compatible endpoint + key + model):

```bash
math2speech-docs convert input.pdf --language en --mode llm --output output.md
```

Speechify placeholder preview:

```bash
math2speech-docs speechify-preview output.md --language en
```

### CLI Options

- `--language` `en|es`
- `--mode` `prompt|rule-based|llm`
- `--output` output path
- `--chunk-size` chunk size in characters
- `--strictness` `conservative|balanced|aggressive`
- `--document-title` optional title (used in prompts)
- `--include-quality-check` add a self-check section to prompts
- `--api-base-url`, `--api-key`, `--model` (LLM mode)

## Python API

```python
from math2speech_docs import convert_document, generate_prompt

result = convert_document(
    "paper.pdf",
    language="en",
    mode="prompt",
)

prompt = generate_prompt(
    "The famous equation is $E = mc^2$.",
    language="es",
)

result = convert_document(
    "paper.pdf",
    language="en",
    mode="llm",
    api_base_url="https://api.llm7.io/v1",
    api_key="replace-me",
    model="replace-me",
)
```

## Configuration (.env placeholders)

Copy `.env.example` to `.env` and adjust:

```env
MATH2SPEECH_API_BASE_URL=https://api.llm7.io/v1
MATH2SPEECH_API_KEY=replace-me
MATH2SPEECH_MODEL=replace-me

SPEECHIFY_API_KEY=replace-me
SPEECHIFY_VOICE_ID=replace-me
```

These values are placeholders only. They are not guaranteed to work; verify them with your chosen provider.

## Modes

- **Prompt mode (`prompt`)**: generates a ready-to-paste prompt (no network calls, no API key required).
- **Rule-based mode (`rule-based`)**: offline fallback that rewrites common patterns (limited coverage).
- **LLM mode (`llm`)**: uses an OpenAI-compatible provider to rewrite chunks; requires endpoint, key, and model.

## Speechify (Placeholder)

Speechify support is currently implemented as a placeholder connector. It does not require an API key and does not perform real API calls yet. The goal is to reserve a clean integration point for future document-to-audio workflows.

## Examples

Input (inline math):

`The famous equation is $E = mc^2$.`

English output:

`The famous equation is E equals m c squared.`

Spanish output:

`La famosa ecuación es E igual a m c al cuadrado.`

See `examples/` for sample inputs and expected outputs.

## Supported Inputs

- PDF (`.pdf`)
- Markdown (`.md`, `.markdown`)
- Plain text (`.txt`, other extensions treated as text)

## Supported Languages

- English (`en`)
- Spanish (`es`)

## Supported Math Notation (MVP)

- Inline math (`$...$`) and block math (`$$...$$`)
- Powers like `x^2`, `x^3`, `x^n`
- Subscripts like `x_i`
- `\\frac{a}{b}`, `\\sqrt{x}`
- Common comparisons `\\neq`, `\\leq`, `\\geq`
- Greek letters `\\alpha`, `\\beta`, `\\gamma`, `\\theta`, `\\pi`

## Limitations

- Complex formulas may require manual review.
- Rule-based mode is intentionally limited.
- Prompt mode only generates prompts (no conversion is performed automatically).
- LLM mode requires a valid OpenAI-compatible API endpoint and key.
- No API keys are included in this repository.
- Output quality depends on the chosen LLM and prompt adherence.
- Scanned PDFs may require OCR before extraction.
- PyMuPDF4LLM extraction quality depends on the PDF structure.
- Speechify integration is currently a placeholder.

## Roadmap

- Better provider integrations
- Local LLM support
- Web UI
- Batch processing
- OCR pipeline
- Word document support
- MathML support
- Richer formula parser
- Multilingual expansion
- Screen-reader presets
- Evaluation benchmark set
- Real Speechify integration
- Audio export pipeline

## Contributing

Issues and PRs are welcome:

- Keep changes modular and testable.
- Avoid committing secrets (API keys, tokens).
- Add/adjust tests for behavior changes.

## Acknowledgements

For this project I used LLM7.io as the default OpenAI-compatible API placeholder. All credit for that huge work goes to @chigwell. Any OpenAI-compatible API is supported; just replace the API endpoint, API key, and model name.

## License

Apache-2.0 (see `LICENSE`).
