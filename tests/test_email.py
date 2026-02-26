"""Tests for synthkit.email module."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from synthkit.base import BASE_FORMAT
from synthkit.email import convert

_OK_HTML = subprocess.CompletedProcess([], 0, stdout="<html>test</html>", stderr="")
_OK_EMPTY = subprocess.CompletedProcess([], 0, stdout="<html></html>", stderr="")


class TestEmailConvert:
    @patch("synthkit.email.platform.system", return_value="Linux")
    @patch("synthkit.email.pyperclip.copy")
    @patch("synthkit.email.config_path", return_value=None)
    @patch("synthkit.email.subprocess.run")
    def test_basic_conversion(
        self, mock_run, mock_config, mock_copy, mock_platform, tmp_md, capsys
    ):
        mock_run.return_value = _OK_HTML
        convert(tmp_md)
        call_args = mock_run.call_args[0][0]
        assert "-t" in call_args
        assert "html" in call_args
        assert "-s" in call_args
        assert "--self-contained" in call_args
        assert "--filter" not in call_args
        mock_copy.assert_called_once_with("<html>test</html>")
        out = capsys.readouterr().out
        assert "HTML copied to clipboard" in out

    @patch("synthkit.email.platform.system", return_value="Linux")
    @patch("synthkit.email.pyperclip.copy")
    @patch("synthkit.email.config_path", return_value=None)
    @patch("synthkit.email.subprocess.run")
    def test_hard_breaks(self, mock_run, mock_config, mock_copy, mock_platform, tmp_md):
        mock_run.return_value = _OK_EMPTY
        convert(tmp_md, hard_breaks=True)
        call_args = mock_run.call_args[0][0]
        assert f"{BASE_FORMAT}+hard_line_breaks" in call_args

    @patch("synthkit.email.platform.system", return_value="Linux")
    @patch("synthkit.email.pyperclip.copy")
    @patch("synthkit.email.config_path", return_value=None)
    @patch("synthkit.email.subprocess.run")
    def test_mermaid_flag(self, mock_run, mock_config, mock_copy, mock_platform, tmp_md):
        mock_run.return_value = _OK_EMPTY
        convert(tmp_md, mermaid=True)
        call_args = mock_run.call_args[0][0]
        assert "--filter" in call_args
        assert "mermaid-filter" in call_args

    def test_smart_file_finding(self, tmp_md_no_ext):
        """Test that email converter finds files without .md extension."""
        with (
            patch("synthkit.email.platform.system", return_value="Linux"),
            patch("synthkit.email.pyperclip.copy"),
            patch("synthkit.email.config_path", return_value=None),
            patch("synthkit.email.subprocess.run") as mock_run,
        ):
            mock_run.return_value = _OK_EMPTY
            convert(tmp_md_no_ext)
            call_args = mock_run.call_args[0][0]
            resolved = [a for a in call_args if "note.md" in str(a)]
            assert len(resolved) > 0

    def test_file_not_found(self, tmp_path):
        with pytest.raises(SystemExit):
            convert(tmp_path / "nonexistent")

    @patch("synthkit.email.config_path", return_value=None)
    @patch("synthkit.email.subprocess.run")
    def test_pandoc_failure(self, mock_run, mock_config, tmp_md):
        mock_run.return_value = subprocess.CompletedProcess([], 1, stdout="", stderr="error msg")
        with pytest.raises(SystemExit):
            convert(tmp_md)

    @patch("synthkit.email.platform.system", return_value="Linux")
    @patch("synthkit.email.pyperclip.copy")
    @patch("synthkit.email.config_path")
    @patch("synthkit.email.subprocess.run")
    def test_with_style_css(self, mock_run, mock_config, mock_copy, mock_platform, tmp_md):
        mock_run.return_value = _OK_EMPTY
        style = Path("/home/user/.config/md2email/style.css")
        mock_config.return_value = style
        convert(tmp_md)
        call_args = mock_run.call_args[0][0]
        assert f"--css={style}" in call_args

    @patch("synthkit.email.platform.system", return_value="Darwin")
    @patch("synthkit.email.config_path", return_value=None)
    @patch("synthkit.email.subprocess.run")
    def test_macos_rtf_path(self, mock_run, mock_config, mock_platform, tmp_md, capsys):
        mock_run.side_effect = [
            _OK_HTML,
            subprocess.CompletedProcess([], 0, stdout="rtf content", stderr=""),
            subprocess.CompletedProcess([], 0),
        ]
        convert(tmp_md)
        assert mock_run.call_count == 3
        textutil_args = mock_run.call_args_list[1][0][0]
        assert "textutil" in textutil_args
        out = capsys.readouterr().out
        assert "Formatted text copied to clipboard" in out

    @patch("synthkit.email.platform.system", return_value="Darwin")
    @patch("synthkit.email.pyperclip.copy")
    @patch("synthkit.email.config_path", return_value=None)
    @patch("synthkit.email.subprocess.run")
    def test_macos_fallback_to_pyperclip(
        self, mock_run, mock_config, mock_copy, mock_platform, tmp_md
    ):
        mock_run.side_effect = [
            _OK_HTML,
            FileNotFoundError("textutil not found"),
        ]
        convert(tmp_md)
        mock_copy.assert_called_once_with("<html>test</html>")
