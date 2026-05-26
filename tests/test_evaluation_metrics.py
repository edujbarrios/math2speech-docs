from math2speech_docs.evaluation.metrics import (
    detected_math_expressions,
    formula_replacement_count,
    readability_length_change,
    unchanged_text_ratio,
)


def test_metrics_basic_behavior():
    original = "The famous equation is $E = mc^2$."
    rewritten = "The famous equation is E equals m c squared."
    assert detected_math_expressions(original)
    assert formula_replacement_count(original, rewritten) >= 1
    assert readability_length_change(original, rewritten) != 0
    assert 0.0 <= unchanged_text_ratio(original, rewritten) <= 1.0
