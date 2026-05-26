from __future__ import annotations

import types

import pytest

from math2speech_docs.llm.openai_compatible import MissingAPIKeyError, OpenAICompatibleClient


def test_openai_client_missing_key_raises():
    client = OpenAICompatibleClient(api_base_url="https://example.com/v1", api_key=None, model="m")
    with pytest.raises(MissingAPIKeyError):
        client.rewrite_markdown(system_prompt="s", user_prompt="u")


def test_openai_client_happy_path_with_fake_openai(monkeypatch: pytest.MonkeyPatch):
    class _FakeMessage:
        def __init__(self, content: str):
            self.content = content

    class _FakeChoice:
        def __init__(self, content: str):
            self.message = _FakeMessage(content)

    class _FakeCompletions:
        def create(self, model, messages):
            return types.SimpleNamespace(choices=[_FakeChoice("OK")])

    class _FakeChat:
        def __init__(self):
            self.completions = _FakeCompletions()

    class _FakeOpenAI:
        def __init__(self, base_url, api_key):
            self.chat = _FakeChat()

    monkeypatch.setitem(
        __import__("sys").modules, "openai", types.SimpleNamespace(OpenAI=_FakeOpenAI)
    )

    client = OpenAICompatibleClient(api_base_url="https://example.com/v1", api_key="k", model="m")
    assert client.rewrite_markdown(system_prompt="s", user_prompt="u") == "OK"
