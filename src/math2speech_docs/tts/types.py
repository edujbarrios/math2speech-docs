from __future__ import annotations

from pydantic import BaseModel

from math2speech_docs.types.models import LanguageCode, PlaceholderStatus


class SpeechifySynthesisResult(BaseModel):
    status: PlaceholderStatus = PlaceholderStatus.placeholder
    message: str
    input_text: str
    voice: str
    language: LanguageCode
