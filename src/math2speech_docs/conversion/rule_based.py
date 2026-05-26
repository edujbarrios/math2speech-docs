from __future__ import annotations

import re

from math2speech_docs.types.models import LanguageCode

_INLINE_DOLLAR = re.compile(r"\$(.+?)\$")
_BLOCK_DOLLAR = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
_FRAC = re.compile(r"\\frac\{([^{}]+)\}\{([^{}]+)\}")
_SQRT = re.compile(r"\\sqrt\{([^{}]+)\}")
_POWER = re.compile(r"([A-Za-z0-9]+)\^(\{[^{}]+\}|[0-9]+|[A-Za-z])")
_SUBSCRIPT = re.compile(r"([A-Za-z0-9]+)_\{?([A-Za-z0-9]+)\}?")

_GREEK = {
    "\\alpha": ("alpha", "alfa"),
    "\\beta": ("beta", "beta"),
    "\\gamma": ("gamma", "gamma"),
    "\\theta": ("theta", "theta"),
    "\\pi": ("pi", "pi"),
}

_OPS = {
    "+": ("plus", "más"),
    "-": ("minus", "menos"),
    "=": ("equals", "igual a"),
}

_LATEX_OPS = {
    "\\neq": ("not equal to", "no es igual a"),
    "\\leq": ("less than or equal to", "menor o igual que"),
    "\\geq": ("greater than or equal to", "mayor o igual que"),
}


def _lang(lang: LanguageCode, en: str, es: str) -> str:
    return en if lang == "en" else es


def rewrite_math_expression(expr: str, *, language: LanguageCode) -> str:
    text = expr.strip()

    for latex, (en_word, es_word) in _GREEK.items():
        text = text.replace(latex, _lang(language, en_word, es_word))

    for latex, (en_word, es_word) in _LATEX_OPS.items():
        text = text.replace(latex, _lang(language, en_word, es_word))

    text = _FRAC.sub(
        lambda m: f"{m.group(1)} {_lang(language, 'divided by', 'dividido entre')} {m.group(2)}",
        text,
    )
    text = _SQRT.sub(
        lambda m: f"{_lang(language, 'the square root of', 'la raíz cuadrada de')} {m.group(1)}",
        text,
    )

    def pow_repl(m: re.Match[str]) -> str:
        base = m.group(1)
        exp = m.group(2)
        exp = exp[1:-1] if exp.startswith("{") and exp.endswith("}") else exp
        if exp == "2":
            return f"{base} {_lang(language, 'squared', 'al cuadrado')}"
        if exp == "3":
            return f"{base} {_lang(language, 'cubed', 'al cubo')}"
        return f"{base} {_lang(language, 'to the power of', 'a la potencia')} {exp}"

    text = _POWER.sub(pow_repl, text)
    text = _SUBSCRIPT.sub(lambda m: f"{m.group(1)} sub {m.group(2)}", text)

    # Token-level replacements for common operators.
    for symbol, (en_word, es_word) in _OPS.items():
        text = text.replace(symbol, f" {_lang(language, en_word, es_word)} ")

    # Light cleanup
    text = re.sub(r"\s+", " ", text).strip()
    return text


def rewrite_markdown_math(markdown_text: str, *, language: LanguageCode) -> str:
    def block_repl(m: re.Match[str]) -> str:
        return rewrite_math_expression(m.group(1), language=language)

    def inline_repl(m: re.Match[str]) -> str:
        return rewrite_math_expression(m.group(1), language=language)

    out = _BLOCK_DOLLAR.sub(block_repl, markdown_text)
    out = _INLINE_DOLLAR.sub(inline_repl, out)
    return out
