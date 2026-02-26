"""Markdown to HTML conversion."""

from pathlib import Path

from .base import ConversionError, build_format, config_path, mermaid_args, run_pandoc


def convert(path: Path, hard_breaks: bool = False, mermaid: bool = False) -> None:
    output = path.with_suffix(".html").name
    fmt = build_format(hard_breaks)

    args = [str(path), "-f", fmt, "-t", "html", "-s", *mermaid_args(mermaid)]

    style = config_path("md2html", "style.css")
    if style:
        args += [f"--css={style}", "--self-contained"]

    args += ["-o", output]

    print(f"Converting {path} to {output}...")
    result = run_pandoc(args)
    if result.returncode != 0:
        raise ConversionError(f"Pandoc failed to generate {output}")
    print(f"Successfully created: {output}")
