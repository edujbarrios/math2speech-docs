from math2speech_docs.detection.math_detector import detect_math, extract_math_expressions


def test_detect_math_finds_inline_and_commands():
    text = "A: $x^2 + y^2 = z^2$ and also \\\\frac{a}{b}."
    expressions = extract_math_expressions(text)
    assert any("x^2" in e for e in expressions)
    assert any("\\frac" in e for e in expressions)

    result = detect_math(text)
    assert result.math_score > 0

