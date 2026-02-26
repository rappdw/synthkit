"""Tests for synthkit.html module."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from synthkit.base import BASE_FORMAT, ConversionError
from synthkit.html import convert


class TestHtmlConvert:
    @patch("synthkit.html.config_path", return_value=None)
    @patch("synthkit.html.run_pandoc")
    def test_basic_conversion(self, mock_pandoc, mock_config, tmp_md, capsys):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md)
        args = mock_pandoc.call_args[0][0]
        assert str(tmp_md) in args
        assert "-t" in args
        assert "html" in args
        assert "-s" in args
        assert "-o" in args
        assert "test.html" in args
        assert "--filter" not in args

    @patch("synthkit.html.config_path", return_value=None)
    @patch("synthkit.html.run_pandoc")
    def test_hard_breaks(self, mock_pandoc, mock_config, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md, hard_breaks=True)
        args = mock_pandoc.call_args[0][0]
        assert f"{BASE_FORMAT}+hard_line_breaks" in args

    @patch("synthkit.html.config_path", return_value=None)
    @patch("synthkit.html.run_pandoc")
    def test_mermaid_flag(self, mock_pandoc, mock_config, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md, mermaid=True)
        args = mock_pandoc.call_args[0][0]
        assert "--filter" in args
        assert "mermaid-filter" in args

    @patch("synthkit.html.config_path")
    @patch("synthkit.html.run_pandoc")
    def test_with_style_css(self, mock_pandoc, mock_config, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        style = Path("/home/user/.config/md2html/style.css")
        mock_config.return_value = style
        convert(tmp_md)
        args = mock_pandoc.call_args[0][0]
        assert f"--css={style}" in args
        assert "--self-contained" in args

    @patch("synthkit.html.config_path", return_value=None)
    @patch("synthkit.html.run_pandoc")
    def test_no_self_contained_without_css(self, mock_pandoc, mock_config, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md)
        args = mock_pandoc.call_args[0][0]
        assert "--self-contained" not in args

    @patch("synthkit.html.config_path", return_value=None)
    @patch("synthkit.html.run_pandoc")
    def test_raises_on_failure(self, mock_pandoc, mock_config, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 1)
        with pytest.raises(ConversionError, match="Pandoc failed"):
            convert(tmp_md)
