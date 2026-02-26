"""Tests for synthkit.pdf module."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from synthkit.base import BASE_FORMAT, ConversionError
from synthkit.pdf import convert


def _no_dep_check():
    """Patch target for skipping _check_weasyprint_deps in unit tests."""
    return None


class TestPdfConvert:
    @patch("synthkit.pdf._check_weasyprint_deps", _no_dep_check)
    @patch("synthkit.pdf.shutil.which", return_value="/usr/bin/weasyprint")
    @patch("synthkit.pdf.config_path", return_value=None)
    @patch("synthkit.pdf.run_pandoc")
    def test_basic_conversion(self, mock_pandoc, mock_config, mock_which, tmp_md, capsys):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md)
        args = mock_pandoc.call_args[0][0]
        assert str(tmp_md) in args
        assert "--pdf-engine=weasyprint" in args
        assert "-t" in args
        assert "html" in args
        assert "-o" in args
        assert "test.pdf" in args
        assert "--filter" not in args

    @patch("synthkit.pdf._check_weasyprint_deps", _no_dep_check)
    @patch("synthkit.pdf.shutil.which", return_value="/usr/bin/weasyprint")
    @patch("synthkit.pdf.config_path", return_value=None)
    @patch("synthkit.pdf.run_pandoc")
    def test_hard_breaks(self, mock_pandoc, mock_config, mock_which, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md, hard_breaks=True)
        args = mock_pandoc.call_args[0][0]
        assert f"{BASE_FORMAT}+hard_line_breaks" in args

    @patch("synthkit.pdf._check_weasyprint_deps", _no_dep_check)
    @patch("synthkit.pdf.shutil.which", return_value="/usr/bin/weasyprint")
    @patch("synthkit.pdf.config_path", return_value=None)
    @patch("synthkit.pdf.run_pandoc")
    def test_mermaid_flag(self, mock_pandoc, mock_config, mock_which, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md, mermaid=True)
        args = mock_pandoc.call_args[0][0]
        assert "--filter" in args
        assert "mermaid-filter" in args

    @patch("synthkit.pdf._check_weasyprint_deps", _no_dep_check)
    @patch("synthkit.pdf.shutil.which", return_value=None)
    def test_raises_when_weasyprint_missing(self, mock_which, tmp_md):
        with pytest.raises(ConversionError, match="weasyprint not found"):
            convert(tmp_md)

    @patch("synthkit.pdf._check_weasyprint_deps", _no_dep_check)
    @patch("synthkit.pdf.shutil.which", return_value="/usr/bin/weasyprint")
    @patch("synthkit.pdf.config_path")
    @patch("synthkit.pdf.run_pandoc")
    def test_with_style_css(self, mock_pandoc, mock_config, mock_which, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        style = Path("/home/user/.config/md2pdf/style.css")
        mock_config.return_value = style
        convert(tmp_md)
        args = mock_pandoc.call_args[0][0]
        assert f"--css={style}" in args

    @patch("synthkit.pdf._check_weasyprint_deps", _no_dep_check)
    @patch("synthkit.pdf.shutil.which", return_value="/usr/bin/weasyprint")
    @patch("synthkit.pdf.config_path", return_value=None)
    @patch("synthkit.pdf.run_pandoc")
    def test_raises_on_pandoc_failure(self, mock_pandoc, mock_config, mock_which, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 1)
        with pytest.raises(ConversionError, match="Pandoc failed"):
            convert(tmp_md)


class TestCheckWeasyprintDeps:
    @patch("synthkit.pdf.subprocess.run")
    def test_raises_on_missing_gobject(self, mock_run, tmp_md):
        mock_run.return_value = subprocess.CompletedProcess(
            [], 1, stdout=b"", stderr=b"cannot load library 'libgobject-2.0-0'"
        )
        with pytest.raises(ConversionError, match="system dependencies"):
            from synthkit.pdf import _check_weasyprint_deps
            _check_weasyprint_deps()

    @patch("synthkit.pdf.subprocess.run")
    def test_raises_on_missing_pango(self, mock_run, tmp_md):
        mock_run.return_value = subprocess.CompletedProcess(
            [], 1, stdout=b"", stderr=b"cannot load library 'pango'"
        )
        with pytest.raises(ConversionError, match="system dependencies"):
            from synthkit.pdf import _check_weasyprint_deps
            _check_weasyprint_deps()

    @patch("synthkit.pdf.subprocess.run")
    def test_passes_when_deps_ok(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess([], 0, stdout=b"", stderr=b"")
        from synthkit.pdf import _check_weasyprint_deps
        _check_weasyprint_deps()  # should not raise

    @patch("synthkit.pdf.subprocess.run", side_effect=FileNotFoundError)
    def test_passes_when_weasyprint_not_found(self, mock_run):
        from synthkit.pdf import _check_weasyprint_deps
        _check_weasyprint_deps()  # should not raise, handled by which check

    @patch("synthkit.pdf.subprocess.run", side_effect=subprocess.TimeoutExpired("weasyprint", 10))
    def test_passes_on_timeout(self, mock_run):
        from synthkit.pdf import _check_weasyprint_deps
        _check_weasyprint_deps()  # should not raise
