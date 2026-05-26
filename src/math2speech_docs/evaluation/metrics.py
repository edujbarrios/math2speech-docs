from __future__ import annotations

import re

from math2speech_docs.detection.math_detector import extract_math_expressions


def formula_replacement_count(original_markdown: str, rewritten_markdown: str) -> int:
    """Approximate count of math expressions that were present then removed."""
    before = len(extract_math_expressions(original_markdown))
    after = len(extract_math_expressions(rewritten_markdown))
    return max(0, before - after)


def unchanged_text_ratio(original_markdown: str, rewritten_markdown: str) -> float:
    """Approximate ratio of unchanged non-math text.

    MVP metric: remove math delimiters and normalize whitespace, then compare prefix overlap.
    """

    def normalize(s: str) -> str:
        s = re.sub(r"\$\$.*?\$\$", " ", s, flags=re.DOTALL)
        s = re.sub(r"\$.*?\$", " ", s)
        s = re.sub(r"\\\(.+?\\\)", " ", s, flags=re.DOTALL)
        s = re.sub(r"\\\[.+?\\\]", " ", s, flags=re.DOTALL)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    a = normalize(original_markdown)
    b = normalize(rewritten_markdown)
    if not a:
        return 1.0 if not b else 0.0
    common = 0
    for ca, cb in zip(a, b, strict=False):
        if ca == cb:
            common += 1
        else:
            break
    return common / max(1, len(a))


def detected_math_expressions(markdown_text: str) -> list[str]:
    return extract_math_expressions(markdown_text)


def readability_length_change(original_markdown: str, rewritten_markdown: str) -> int:
    return len(rewritten_markdown) - len(original_markdown)
