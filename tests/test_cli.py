from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from math2speech_docs.cli.main import app


def test_cli_prompt_writes_output(tmp_path: Path):
    runner = CliRunner()
    input_path = tmp_path / "sample.md"
    input_path.write_text("The famous equation is $E = mc^2$.\n", encoding="utf-8")

    out_path = tmp_path / "prompt.md"
    result = runner.invoke(app, ["prompt", str(input_path), "--output", str(out_path), "--language", "en"])
    assert result.exit_code == 0
    assert out_path.exists()
    assert "Rewrite the following Markdown document" in out_path.read_text(encoding="utf-8")


def test_cli_convert_rule_based(tmp_path: Path):
    runner = CliRunner()
    input_path = tmp_path / "sample.md"
    input_path.write_text("The famous equation is $E = mc^2$.\n", encoding="utf-8")

    out_path = tmp_path / "out.md"
    result = runner.invoke(
        app,
        ["convert", str(input_path), "--mode", "rule-based", "--language", "en", "--output", str(out_path)],
    )
    assert result.exit_code == 0
    assert "equals" in out_path.read_text(encoding="utf-8")


def test_cli_speechify_preview_outputs_json(tmp_path: Path):
    runner = CliRunner()
    input_path = tmp_path / "out.md"
    input_path.write_text("E equals m c squared.\n", encoding="utf-8")

    result = runner.invoke(app, ["speechify-preview", str(input_path), "--language", "en"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "placeholder"

