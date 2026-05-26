from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

LanguageCode = Literal["en", "es"]
ConversionMode = Literal["prompt", "rule-based", "llm"]


@dataclass(frozen=True)
class ConversionResult:
    input_path: str
    language: LanguageCode
    mode: ConversionMode
    output_markdown: str
    prompt: str | None = None

