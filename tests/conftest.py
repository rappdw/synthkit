"""Shared fixtures for Synthkit tests."""

import pytest


@pytest.fixture
def tmp_md(tmp_path):
    """Create a temporary markdown file and return its path."""
    md = tmp_path / "test.md"
    md.write_text("# Hello\n\nThis is a **test** document.\n")
    return md


@pytest.fixture
def tmp_md_no_ext(tmp_path):
    """Create a markdown file and return a path without the .md extension."""
    md = tmp_path / "note.md"
    md.write_text("# Note\n\nSome content.\n")
    return tmp_path / "note"


@pytest.fixture
def multiple_md(tmp_path):
    """Create multiple markdown files."""
    for name in ("a.md", "b.md", "c.md"):
        (tmp_path / name).write_text(f"# {name}\n\nContent of {name}.\n")
    return tmp_path


@pytest.fixture
def non_md_file(tmp_path):
    """Create a non-markdown file."""
    txt = tmp_path / "notes.txt"
    txt.write_text("not markdown")
    return txt
