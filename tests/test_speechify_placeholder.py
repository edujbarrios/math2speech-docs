from math2speech_docs.tts import SpeechifyClient


def test_speechify_placeholder_result_fields():
    client = SpeechifyClient()
    result = client.synthesize_placeholder(text="Hello", voice="default", language="en")
    assert result.status.value == "placeholder"
    assert "placeholder connector" in result.message
