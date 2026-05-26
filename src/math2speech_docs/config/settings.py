from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MATH2SPEECH_", env_file=".env", extra="ignore")

    api_base_url: str = "https://api.llm7.io/v1"
    api_key: str | None = None
    model: str | None = None

    # Speechify placeholders (env vars live outside MATH2SPEECH_ prefix)
    speechify_api_key: str | None = None
    speechify_voice_id: str | None = None

    @classmethod
    def from_env(cls) -> Settings:
        # Allow SPEECHIFY_* vars while still supporting MATH2SPEECH_* for core settings.
        base = cls()
        # Pydantic-settings doesn't support multiple prefixes cleanly; read these manually.
        import os

        base.speechify_api_key = os.getenv("SPEECHIFY_API_KEY")
        base.speechify_voice_id = os.getenv("SPEECHIFY_VOICE_ID")
        return base
