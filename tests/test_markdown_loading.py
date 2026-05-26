from pathlib import Path

from math2speech_docs.extraction.markdown import load_markdown, normalize_markdown


def test_load_markdown_reads_file(tmp_path: Path):
    path = tmp_path / "doc.md"
    path.write_text("# Title\n\nText\n", encoding="utf-8")
    assert load_markdown(path).startswith("# Title")


def test_normalize_markdown_normalizes_newlines():
    assert normalize_markdown("a\r\nb\r\n") == "a\nb\n"
