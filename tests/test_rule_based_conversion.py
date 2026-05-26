from math2speech_docs.conversion.rule_based import rewrite_markdown_math


def test_rule_based_conversion_english_examples():
    text = "The famous equation is $E = mc^2$."
    out = rewrite_markdown_math(text, language="en")
    assert "equals" in out
    assert "squared" in out


def test_rule_based_conversion_spanish_examples():
    text = "La famosa ecuación es $E = mc^2$."
    out = rewrite_markdown_math(text, language="es")
    assert "igual a" in out
    assert "al cuadrado" in out
