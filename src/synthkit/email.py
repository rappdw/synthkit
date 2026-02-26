"""Markdown to clipboard email conversion."""

import platform
import subprocess
import sys
from pathlib import Path

import pyperclip

from .base import (
    build_format,
    cleanup_mermaid_err,
    config_path,
    get_pandoc_bin,
    mermaid_args,
)


def convert(path: Path, hard_breaks: bool = False, mermaid: bool = False) -> None:
    # Smart file finding: accept with or without .md extension
    if not path.is_file() and path.with_suffix(".md").is_file():
        path = path.with_suffix(".md")

    if not path.is_file():
        print(f"Error: Could not find file '{path}' or '{path.with_suffix('.md')}'")
        sys.exit(1)

    fmt = build_format(hard_breaks)

    args = [
        get_pandoc_bin(),
        str(path),
        "-f",
        fmt,
        "-t",
        "html",
        "-s",
        "--self-contained",
        *mermaid_args(mermaid),
    ]

    style = config_path("md2email", "style.css")
    if style:
        args += [f"--css={style}"]

    print(f"Converting {path} to clipboard...")
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: Pandoc failed to convert {path}")
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(1)

    html = result.stdout

    # On macOS, convert to RTF via textutil for richer paste support
    if platform.system() == "Darwin":
        try:
            rtf_result = subprocess.run(
                ["textutil", "-stdin", "-format", "html", "-convert", "rtf", "-stdout"],
                input=html,
                capture_output=True,
                text=True,
            )
            if rtf_result.returncode == 0:
                subprocess.run(["pbcopy"], input=rtf_result.stdout, text=True, check=True)
                print("Success! Formatted text copied to clipboard.")
                if mermaid:
                    cleanup_mermaid_err()
                return
        except FileNotFoundError:
            pass  # Fall through to pyperclip

    pyperclip.copy(html)
    print("Success! HTML copied to clipboard.")
    if mermaid:
        cleanup_mermaid_err()
