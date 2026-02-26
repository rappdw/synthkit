"""Markdown to PDF conversion via weasyprint."""

import shutil
from pathlib import Path

from .base import ConversionError, build_format, config_path, mermaid_args, run_pandoc


def convert(path: Path, hard_breaks: bool = False, mermaid: bool = False) -> None:
    output = path.with_suffix(".pdf").name
    fmt = build_format(hard_breaks)

    if not shutil.which("weasyprint"):
        raise ConversionError(
            "weasyprint not found on PATH. Install it with: pip install weasyprint"
        )

    args = [
        str(path),
        "-f",
        fmt,
        "-t",
        "html",
        "--pdf-engine=weasyprint",
        *mermaid_args(mermaid),
    ]

    style = config_path("md2pdf", "style.css")
    if style:
        args += [f"--css={style}"]

    args += ["-o", output]

    print(f"Converting {path} to {output}...")
    result = run_pandoc(args)
    if result.returncode != 0:
        raise ConversionError(f"Pandoc failed to generate {output}")
    print(f"Successfully created: {output}")
