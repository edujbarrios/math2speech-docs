from math2speech_docs.chunking.chunker import chunk_markdown


def test_chunk_markdown_splits_into_multiple_chunks():
    text = "\n\n".join([f"Paragraph {i}: $x^2$" for i in range(30)])
    chunks = chunk_markdown(text, chunk_size=200)
    assert len(chunks) > 1
    assert all(chunk.metadata.char_count > 0 for chunk in chunks)

