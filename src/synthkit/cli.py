"""Click CLI for Synthkit."""

from pathlib import Path

import click

from . import doc, email, html, pdf
from .base import batch_convert

_MERMAID_HELP = "Enable Mermaid diagram rendering (requires mermaid-filter)."


@click.group()
def main() -> None:
    """Synthkit: Convert AI-generated Markdown into production-ready documents."""


@main.command("doc")
@click.option("--hard-breaks", is_flag=True, help="Preserve line breaks in source.")
@click.option("--mermaid", is_flag=True, help=_MERMAID_HELP)
@click.argument("files", nargs=-1, type=click.Path())
def doc_subcmd(hard_breaks: bool, mermaid: bool, files: tuple[str, ...]) -> None:
    """Convert Markdown to Word (.docx)."""
    batch_convert(files, hard_breaks, mermaid, doc.convert)


@main.command("email")
@click.option("--hard-breaks", is_flag=True, help="Preserve line breaks in source.")
@click.option("--mermaid", is_flag=True, help=_MERMAID_HELP)
@click.argument("file", type=click.Path())
def email_subcmd(hard_breaks: bool, mermaid: bool, file: str) -> None:
    """Convert Markdown to clipboard-ready email."""
    email.convert(Path(file), hard_breaks, mermaid)


@main.command("html")
@click.option("--hard-breaks", is_flag=True, help="Preserve line breaks in source.")
@click.option("--mermaid", is_flag=True, help=_MERMAID_HELP)
@click.argument("files", nargs=-1, type=click.Path())
def html_subcmd(hard_breaks: bool, mermaid: bool, files: tuple[str, ...]) -> None:
    """Convert Markdown to HTML."""
    batch_convert(files, hard_breaks, mermaid, html.convert)


@main.command("pdf")
@click.option("--hard-breaks", is_flag=True, help="Preserve line breaks in source.")
@click.option("--mermaid", is_flag=True, help=_MERMAID_HELP)
@click.argument("files", nargs=-1, type=click.Path())
def pdf_subcmd(hard_breaks: bool, mermaid: bool, files: tuple[str, ...]) -> None:
    """Convert Markdown to PDF."""
    batch_convert(files, hard_breaks, mermaid, pdf.convert)


# Backward-compatible standalone entry points


def md2doc_cmd() -> None:
    """Standalone md2doc entry point."""

    @click.command()
    @click.option("--hard-breaks", is_flag=True, help="Preserve line breaks in source.")
    @click.option("--mermaid", is_flag=True, help=_MERMAID_HELP)
    @click.argument("files", nargs=-1, type=click.Path())
    def _cmd(hard_breaks: bool, mermaid: bool, files: tuple[str, ...]) -> None:
        batch_convert(files, hard_breaks, mermaid, doc.convert)

    _cmd()


def md2email_cmd() -> None:
    """Standalone md2email entry point."""

    @click.command()
    @click.option("--hard-breaks", is_flag=True, help="Preserve line breaks in source.")
    @click.option("--mermaid", is_flag=True, help=_MERMAID_HELP)
    @click.argument("file", type=click.Path())
    def _cmd(hard_breaks: bool, mermaid: bool, file: str) -> None:
        email.convert(Path(file), hard_breaks, mermaid)

    _cmd()


def md2html_cmd() -> None:
    """Standalone md2html entry point."""

    @click.command()
    @click.option("--hard-breaks", is_flag=True, help="Preserve line breaks in source.")
    @click.option("--mermaid", is_flag=True, help=_MERMAID_HELP)
    @click.argument("files", nargs=-1, type=click.Path())
    def _cmd(hard_breaks: bool, mermaid: bool, files: tuple[str, ...]) -> None:
        batch_convert(files, hard_breaks, mermaid, html.convert)

    _cmd()


def md2pdf_cmd() -> None:
    """Standalone md2pdf entry point."""

    @click.command()
    @click.option("--hard-breaks", is_flag=True, help="Preserve line breaks in source.")
    @click.option("--mermaid", is_flag=True, help=_MERMAID_HELP)
    @click.argument("files", nargs=-1, type=click.Path())
    def _cmd(hard_breaks: bool, mermaid: bool, files: tuple[str, ...]) -> None:
        batch_convert(files, hard_breaks, mermaid, pdf.convert)

    _cmd()
