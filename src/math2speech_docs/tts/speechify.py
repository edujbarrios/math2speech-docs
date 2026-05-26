from __future__ import annotations

from dataclasses import dataclass

from math2speech_docs.tts.types import SpeechifySynthesisResult
from math2speech_docs.types.models import LanguageCode


@dataclass(frozen=True)
class SpeechifyClient:
    """Placeholder connector for a future Speechify TTS backend.

    This client never performs network calls and never requires an API key.
    """

    def synthesize_placeholder(
        self,
        *,
        text: str,
        voice: str = "default",
        language: LanguageCode = "en",
    ) -> SpeechifySynthesisResult:
        return SpeechifySynthesisResult(
            message=(
                "Speechify support is currently implemented as a placeholder connector. "
                "It does not require an API key and does not perform real API calls yet."
            ),
            input_text=text,
            voice=voice,
            language=language,
        )
