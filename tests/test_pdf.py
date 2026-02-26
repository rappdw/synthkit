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
        # env should be None when _check_weasyprint_deps returns None
        assert mock_pandoc.call_args[1].get("env") is None

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

    @patch("synthkit.pdf.shutil.which", return_value="/usr/bin/weasyprint")
    @patch("synthkit.pdf.config_path", return_value=None)
    @patch("synthkit.pdf.run_pandoc")
    def test_passes_env_from_dep_check(self, mock_pandoc, mock_config, mock_which, tmp_md):
        """When _check_weasyprint_deps returns an env dict, it's passed to run_pandoc."""
        fake_env = {"DYLD_FALLBACK_LIBRARY_PATH": "/opt/homebrew/lib"}
        with patch("synthkit.pdf._check_weasyprint_deps", return_value=fake_env):
            mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
            convert(tmp_md)
            assert mock_pandoc.call_args[1]["env"] == fake_env


class TestCheckWeasyprintDeps:
    @patch("synthkit.pdf._weasyprint_env", return_value=None)
    @patch("synthkit.pdf.subprocess.run")
    def test_raises_on_missing_gobject(self, mock_run, mock_env):
        mock_run.return_value = subprocess.CompletedProcess(
            [], 1, stdout=b"", stderr=b"cannot load library 'libgobject-2.0-0'"
        )
        from synthkit.pdf import _check_weasyprint_deps

        with pytest.raises(ConversionError, match="cannot find its system libraries"):
            _check_weasyprint_deps()

    @patch("synthkit.pdf._weasyprint_env", return_value=None)
    @patch("synthkit.pdf.subprocess.run")
    def test_raises_on_missing_pango(self, mock_run, mock_env):
        mock_run.return_value = subprocess.CompletedProcess(
            [], 1, stdout=b"", stderr=b"cannot load library 'pango'"
        )
        from synthkit.pdf import _check_weasyprint_deps

        with pytest.raises(ConversionError, match="cannot find its system libraries"):
            _check_weasyprint_deps()

    @patch("synthkit.pdf.subprocess.run")
    def test_returns_none_when_deps_ok(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess([], 0, stdout=b"", stderr=b"")
        from synthkit.pdf import _check_weasyprint_deps

        assert _check_weasyprint_deps() is None

    @patch("synthkit.pdf.subprocess.run", side_effect=FileNotFoundError)
    def test_returns_none_when_weasyprint_not_found(self, mock_run):
        from synthkit.pdf import _check_weasyprint_deps

        assert _check_weasyprint_deps() is None

    @patch("synthkit.pdf.subprocess.run", side_effect=subprocess.TimeoutExpired("weasyprint", 10))
    def test_returns_none_on_timeout(self, mock_run):
        from synthkit.pdf import _check_weasyprint_deps

        assert _check_weasyprint_deps() is None

    @patch("synthkit.pdf._weasyprint_env")
    @patch("synthkit.pdf.subprocess.run")
    def test_retries_with_brew_env_on_failure(self, mock_run, mock_env):
        """When initial check fails but retry with Homebrew env succeeds, returns env."""
        fake_env = {"DYLD_FALLBACK_LIBRARY_PATH": "/opt/homebrew/lib"}
        mock_env.return_value = fake_env
        mock_run.side_effect = [
            # First call: fails with gobject error
            subprocess.CompletedProcess(
                [], 1, stdout=b"", stderr=b"cannot load library 'libgobject-2.0-0'"
            ),
            # Second call (retry with env): succeeds
            subprocess.CompletedProcess([], 0, stdout=b"", stderr=b""),
        ]
        from synthkit.pdf import _check_weasyprint_deps

        result = _check_weasyprint_deps()
        assert result == fake_env

    @patch("synthkit.pdf._weasyprint_env")
    @patch("synthkit.pdf.subprocess.run")
    def test_raises_when_brew_env_retry_also_fails(self, mock_run, mock_env):
        """When both initial check and retry with Homebrew env fail, raises error."""
        fake_env = {"DYLD_FALLBACK_LIBRARY_PATH": "/opt/homebrew/lib"}
        mock_env.return_value = fake_env
        mock_run.side_effect = [
            subprocess.CompletedProcess(
                [], 1, stdout=b"", stderr=b"cannot load library 'libgobject-2.0-0'"
            ),
            subprocess.CompletedProcess(
                [], 1, stdout=b"", stderr=b"cannot load library 'libgobject-2.0-0'"
            ),
        ]
        from synthkit.pdf import _check_weasyprint_deps

        with pytest.raises(ConversionError, match="cannot find its system libraries"):
            _check_weasyprint_deps()
