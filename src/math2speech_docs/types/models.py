from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field

LanguageCode = Literal["en", "es"]
ConversionMode = Literal["prompt", "rule-based", "llm"]
DocumentType = Literal["pdf", "markdown", "text"]
StrictnessLevel = Literal["conservative", "balanced", "aggressive"]


class ChunkMetadata(BaseModel):
    index: int = Field(ge=0)
    char_count: int = Field(ge=0)
    math_score: float = Field(ge=0.0)


class DocumentChunk(BaseModel):
    metadata: ChunkMetadata
    markdown: str


class DetectionResult(BaseModel):
    is_math_heavy: bool
    math_score: float = Field(ge=0.0)
    expressions: list[str] = Field(default_factory=list)


class LLMProviderSettings(BaseModel):
    api_base_url: str
    api_key: str | None = None
    model: str | None = None


class TTSProviderSettings(BaseModel):
    speechify_api_key: str | None = None
    speechify_voice_id: str | None = None


class ConversionResult(BaseModel):
    input_path: str
    document_type: DocumentType
    language: LanguageCode
    mode: ConversionMode
    output_markdown: str
    prompt: str | None = None
    chunks: list[DocumentChunk] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class PlaceholderStatus(StrEnum):
    placeholder = "placeholder"
