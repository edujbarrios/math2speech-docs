from __future__ import annotations

from math2speech_docs.detection.math_detector import compute_math_score, extract_math_expressions
from math2speech_docs.types.models import ChunkMetadata, DocumentChunk


def chunk_markdown(markdown_text: str, *, chunk_size: int = 3000) -> list[DocumentChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")

    paragraphs = markdown_text.split("\n\n")
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    def flush() -> None:
        nonlocal current, current_len
        if current:
            chunks.append("\n\n".join(current).strip() + "\n")
            current = []
            current_len = 0

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        candidate_len = current_len + len(paragraph) + (2 if current else 0)
        if candidate_len > chunk_size and current:
            flush()
        current.append(paragraph)
        current_len += len(paragraph) + (2 if current_len else 0)

    flush()

    result: list[DocumentChunk] = []
    for index, chunk in enumerate(chunks):
        math_score = compute_math_score(chunk)
        meta = ChunkMetadata(
            index=index,
            char_count=len(chunk),
            math_score=math_score,
        )
        result.append(DocumentChunk(metadata=meta, markdown=chunk))
    return result


def chunk_is_math_heavy(chunk: DocumentChunk, *, threshold: float = 0.01) -> bool:
    return chunk.metadata.math_score >= threshold or bool(extract_math_expressions(chunk.markdown))
