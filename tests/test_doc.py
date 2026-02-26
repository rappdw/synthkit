"""Tests for synthkit.doc module."""

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from synthkit.base import BASE_FORMAT, ConversionError
from synthkit.doc import convert


class TestDocConvert:
    @patch("synthkit.doc.config_path", return_value=None)
    @patch("synthkit.doc.run_pandoc")
    def test_basic_conversion(self, mock_pandoc, mock_config, tmp_md, capsys):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md)
        args = mock_pandoc.call_args[0][0]
        assert str(tmp_md) in args
        assert "-f" in args
        assert BASE_FORMAT in args
        assert "-t" in args
        assert "docx" in args
        assert "-o" in args
        assert "test.docx" in args
        # mermaid filter should NOT be present by default
        assert "--filter" not in args

    @patch("synthkit.doc.config_path", return_value=None)
    @patch("synthkit.doc.run_pandoc")
    def test_hard_breaks(self, mock_pandoc, mock_config, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md, hard_breaks=True)
        args = mock_pandoc.call_args[0][0]
        assert f"{BASE_FORMAT}+hard_line_breaks" in args

    @patch("synthkit.doc.config_path", return_value=None)
    @patch("synthkit.doc.run_pandoc")
    def test_mermaid_flag(self, mock_pandoc, mock_config, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md, mermaid=True)
        args = mock_pandoc.call_args[0][0]
        assert "--filter" in args
        assert "mermaid-filter" in args

    @patch("synthkit.doc.config_path")
    @patch("synthkit.doc.run_pandoc")
    def test_reference_doc(self, mock_pandoc, mock_config, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        ref_path = Path("/home/user/.config/md2doc/reference.docx")
        mock_config.return_value = ref_path
        convert(tmp_md)
        args = mock_pandoc.call_args[0][0]
        assert f"--reference-doc={ref_path}" in args

    @patch("synthkit.doc.config_path", return_value=None)
    @patch("synthkit.doc.run_pandoc")
    def test_raises_on_failure(self, mock_pandoc, mock_config, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 1)
        with pytest.raises(ConversionError, match="Pandoc failed"):
            convert(tmp_md)

    @patch("synthkit.doc.config_path", return_value=None)
    @patch("synthkit.doc.run_pandoc")
    def test_output_filename(self, mock_pandoc, mock_config, tmp_md):
        mock_pandoc.return_value = subprocess.CompletedProcess([], 0)
        convert(tmp_md)
        args = mock_pandoc.call_args[0][0]
        idx = args.index("-o")
        assert args[idx + 1] == "test.docx"
