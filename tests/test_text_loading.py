from pathlib import Path

from math2speech_docs.extraction.text import load_text


def test_load_text_reads_file(tmp_path: Path):
    path = tmp_path / "doc.txt"
    path.write_text("hello\n", encoding="utf-8")
    assert load_text(path).strip() == "hello"


def test_load_text_with_title_wraps_markdown(tmp_path: Path):
    path = tmp_path / "doc.txt"
    path.write_text("hello\n", encoding="utf-8")
    md = load_text(path, document_title="Title")
    assert md.startswith("# Title")

