"""Markdown to PDF conversion via weasyprint."""

import platform
import shutil
import subprocess
from pathlib import Path

from .base import ConversionError, build_format, config_path, mermaid_args, run_pandoc

_SYSTEM_DEPS_HELP = {
    "Darwin": (
        "On macOS, install them with:\n"
        "  brew install pango"
    ),
    "Linux": (
        "On Ubuntu/Debian, install them with:\n"
        "  sudo apt install libpango1.0-dev libcairo2-dev libgdk-pixbuf2.0-dev\n"
        "On Fedora/RHEL:\n"
        "  sudo dnf install pango-devel cairo-devel gdk-pixbuf2-devel"
    ),
}


def _check_weasyprint_deps() -> None:
    """Verify that weasyprint's system dependencies are available."""
    try:
        result = subprocess.run(
            ["weasyprint", "--info"],
            capture_output=True,
            timeout=10,
        )
        if result.returncode != 0:
            stderr = result.stderr.decode(errors="replace")
            if "gobject" in stderr or "pango" in stderr or "cairo" in stderr:
                system = platform.system()
                hint = _SYSTEM_DEPS_HELP.get(system, "")
                msg = (
                    "weasyprint is installed but its system dependencies "
                    "(pango, cairo, gobject) are missing.\n"
                )
                if hint:
                    msg += f"\n{hint}\n"
                msg += (
                    "\nFor full details see: "
                    "https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation"
                )
                raise ConversionError(msg)
    except FileNotFoundError:
        pass  # handled by the shutil.which check below
    except subprocess.TimeoutExpired:
        pass  # let pandoc attempt it


def convert(path: Path, hard_breaks: bool = False, mermaid: bool = False) -> None:
    output = path.with_suffix(".pdf").name
    fmt = build_format(hard_breaks)

    if not shutil.which("weasyprint"):
        raise ConversionError(
            "weasyprint not found on PATH. Install it with: pip install weasyprint"
        )

    _check_weasyprint_deps()

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
        system = platform.system()
        hint = _SYSTEM_DEPS_HELP.get(system, "")
        msg = f"Pandoc failed to generate {output}"
        if hint:
            msg += (
                "\n\nThis may be caused by missing system dependencies for weasyprint.\n"
                f"{hint}\n"
                "\nFor full details see: "
                "https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation"
            )
        raise ConversionError(msg)
    print(f"Successfully created: {output}")
