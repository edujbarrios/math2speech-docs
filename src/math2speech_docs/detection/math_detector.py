from __future__ import annotations

import re

from math2speech_docs.types.models import DetectionResult

_INLINE_DOLLAR = re.compile(r"\$(.+?)\$")
_BLOCK_DOLLAR = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
_PAREN_LATEX = re.compile(r"\\\((.+?)\\\)", re.DOTALL)
_BRACKET_LATEX = re.compile(r"\\\[(.+?)\\\]", re.DOTALL)
_LATEX_COMMANDS = re.compile(
    r"\\(frac|sqrt|sum|int|neq|leq|geq|alpha|beta|gamma|theta|pi)\b"
)


def extract_math_expressions(text: str) -> list[str]:
    expressions: list[str] = []
    for pattern in (_BLOCK_DOLLAR, _INLINE_DOLLAR, _PAREN_LATEX, _BRACKET_LATEX):
        expressions.extend(match.group(1).strip() for match in pattern.finditer(text))
    expressions.extend(match.group(0) for match in _LATEX_COMMANDS.finditer(text))
    return [expr for expr in expressions if expr]


def compute_math_score(text: str) -> float:
    if not text:
        return 0.0
    matches = len(extract_math_expressions(text))
    return matches / max(1, len(text) / 1000)


def detect_math(markdown_text: str, *, threshold: float = 1.0) -> DetectionResult:
    expressions = extract_math_expressions(markdown_text)
    score = compute_math_score(markdown_text)
    return DetectionResult(is_math_heavy=score >= threshold, math_score=score, expressions=expressions)

