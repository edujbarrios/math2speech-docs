from __future__ import annotations

from dataclasses import dataclass

from jinja2 import Environment, PackageLoader, StrictUndefined

from math2speech_docs.types.models import LanguageCode, StrictnessLevel


@dataclass(frozen=True)
class PromptRenderer:
    env: Environment

    @classmethod
    def default(cls) -> "PromptRenderer":
        env = Environment(
            loader=PackageLoader("math2speech_docs", "prompts/templates"),
            autoescape=False,
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        return cls(env=env)

    def render_system(self, *, language: LanguageCode, strictness: StrictnessLevel) -> str:
        return self.env.get_template("system_prompt.j2").render(
            language=language,
            strictness=strictness,
        )

    def render_rewrite_document(
        self,
        *,
        markdown_text: str,
        language: LanguageCode,
        strictness: StrictnessLevel,
        document_title: str | None = None,
        include_quality_check: bool = False,
    ) -> str:
        return self.env.get_template("rewrite_document.j2").render(
            system_prompt=self.render_system(language=language, strictness=strictness),
            markdown_text=markdown_text,
            language=language,
            strictness=strictness,
            document_title=document_title,
            include_quality_check=include_quality_check,
        )

