from math2speech_docs import generate_prompt


def test_generate_prompt_includes_required_sections():
    prompt = generate_prompt("The famous equation is $E = mc^2$.\n", language="en")
    assert "SYSTEM" in prompt
    assert "USER" in prompt
    assert "Return only the rewritten document" in prompt
