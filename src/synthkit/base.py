"""Base converter with shared logic for all Synthkit converters."""

import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pypandoc

BASE_FORMAT = "markdown+lists_without_preceding_blankline"


def build_format(hard_breaks: bool = False) -> str:
    fmt = BASE_FORMAT
    if hard_breaks:
        fmt += "+hard_line_breaks"
    return fmt


def config_path(tool_name: str, filename: str) -> Path | None:
    p = Path.home() / ".config" / tool_name / filename
    return p if p.is_file() else None


def bundled_style_css() -> Path:
    return Path(__file__).parent.parent.parent / "style.css"


def cleanup_mermaid_err() -> None:
    err = Path("mermaid-filter.err")
    if err.is_file() and err.stat().st_size == 0:
        err.unlink()


def get_pandoc_bin() -> str:
    return str(pypandoc.get_pandoc_path())


def run_pandoc(args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run([get_pandoc_bin(), *args], capture_output=False)


def mermaid_args(mermaid: bool) -> list[str]:
    if mermaid:
        return ["--filter", "mermaid-filter"]
    return []


def batch_convert(
    files: tuple[str, ...],
    hard_breaks: bool,
    mermaid: bool,
    convert_one: Callable[[Path, bool, bool], None],
) -> None:
    if not files:
        print("No input files provided.", file=sys.stderr)
        sys.exit(1)

    success = 0
    fail = 0

    for filepath in files:
        path = Path(filepath)
        if path.suffix != ".md":
            print(f"Skipping non-markdown file: {filepath}")
            continue
        if not path.is_file():
            print(f"Warning: File '{filepath}' not found, skipping.")
            fail += 1
            continue

        try:
            convert_one(path, hard_breaks, mermaid)
            success += 1
        except ConversionError as e:
            print(f"Error: {e}")
            fail += 1

    if mermaid:
        cleanup_mermaid_err()
    print(f"\nDone: {success} succeeded, {fail} failed.")
    if fail > 0:
        sys.exit(1)


class ConversionError(Exception):
    pass
