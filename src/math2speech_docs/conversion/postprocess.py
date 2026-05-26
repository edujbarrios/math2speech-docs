from __future__ import annotations

import re


_MULTISPACE = re.compile(r"[ \t]{2,}")


def postprocess_markdown(markdown_text: str) -> str:
    # Keep line structure, but normalize accidental multi-spaces created by substitutions.
    lines = [
        _MULTISPACE.sub(" ", line).rstrip()
        for line in markdown_text.replace("\r\n", "\n").split("\n")
    ]
    return "\n".join(lines).strip() + "\n"

