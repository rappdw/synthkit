"""Markdown to PDF conversion via weasyprint."""

import os
import platform
import shutil
import subprocess
from pathlib import Path

from .base import ConversionError, build_format, config_path, mermaid_args, run_pandoc

_INSTALL_HELP = {
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

_WEASYPRINT_DOCS = (
    "https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation"
)


def _brew_lib_path() -> str | None:
    """Return Homebrew lib directory if available."""
    try:
        result = subprocess.run(
            ["brew", "--prefix"], capture_output=True, timeout=5
        )
        if result.returncode == 0:
            prefix = result.stdout.decode().strip()
            lib_dir = os.path.join(prefix, "lib")
            if os.path.isdir(lib_dir):
                return lib_dir
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def _weasyprint_env() -> dict[str, str] | None:
    """Build environment with library paths for weasyprint on macOS."""
    if platform.system() != "Darwin":
        return None
    brew_lib = _brew_lib_path()
    if not brew_lib:
        return None
    env = os.environ.copy()
    existing = env.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    if brew_lib not in existing:
        env["DYLD_FALLBACK_LIBRARY_PATH"] = (
            f"{brew_lib}:{existing}" if existing else brew_lib
        )
    return env


def _check_weasyprint_deps() -> dict[str, str] | None:
    """Verify weasyprint's system deps are available. Returns env dict if needed."""
    env = None
    try:
        result = subprocess.run(
            ["weasyprint", "--info"], capture_output=True, timeout=10,
        )
        if result.returncode != 0:
            stderr = result.stderr.decode(errors="replace")
            if "gobject" in stderr or "pango" in stderr or "cairo" in stderr:
                # Try again with Homebrew library path on macOS
                env = _weasyprint_env()
                if env:
                    retry = subprocess.run(
                        ["weasyprint", "--info"],
                        capture_output=True, timeout=10, env=env,
                    )
                    if retry.returncode == 0:
                        return env  # libs found with env fix

                # Still broken — report helpful error
                system = platform.system()
                hint = _INSTALL_HELP.get(system, "")
                msg = (
                    "weasyprint is installed but cannot find its system libraries "
                    "(pango, cairo, gobject).\n"
                )
                if hint:
                    msg += f"\n{hint}\n"
                msg += f"\nFor full details see: {_WEASYPRINT_DOCS}"
                raise ConversionError(msg)
    except FileNotFoundError:
        pass  # handled by the shutil.which check below
    except subprocess.TimeoutExpired:
        pass  # let pandoc attempt it
    return env


def convert(path: Path, hard_breaks: bool = False, mermaid: bool = False) -> None:
    output = path.with_suffix(".pdf").name
    fmt = build_format(hard_breaks)

    if not shutil.which("weasyprint"):
        raise ConversionError(
            "weasyprint not found on PATH. Install it with: pip install weasyprint"
        )

    env = _check_weasyprint_deps()

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
    result = run_pandoc(args, env=env)
    if result.returncode != 0:
        system = platform.system()
        hint = _INSTALL_HELP.get(system, "")
        msg = f"Pandoc failed to generate {output}"
        if hint:
            msg += (
                "\n\nThis may be caused by missing system dependencies for weasyprint.\n"
                f"{hint}\n"
                f"\nFor full details see: {_WEASYPRINT_DOCS}"
            )
        raise ConversionError(msg)
    print(f"Successfully created: {output}")
