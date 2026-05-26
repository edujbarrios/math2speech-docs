from __future__ import annotations

from dataclasses import dataclass


class MissingAPIKeyError(ValueError):
    pass


@dataclass(frozen=True)
class OpenAICompatibleClient:
    api_base_url: str
    api_key: str | None
    model: str | None

    def rewrite_markdown(self, *, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise MissingAPIKeyError(
                "Missing API key for LLM mode. Set MATH2SPEECH_API_KEY or pass --api-key."
            )
        if not self.model:
            raise ValueError("Missing model name for LLM mode. Set MATH2SPEECH_MODEL or pass --model.")

        try:
            from openai import OpenAI  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise ImportError("LLM mode requires the OpenAI Python SDK. Install with `pip install -e '.[llm]'`.") from exc

        client = OpenAI(base_url=self.api_base_url, api_key=self.api_key)
        completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        message = completion.choices[0].message.content
        if not message:
            raise RuntimeError("LLM returned empty content.")
        return message

