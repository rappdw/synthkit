"""Tests for synthkit.cli module."""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from synthkit.cli import main


@pytest.fixture
def runner():
    return CliRunner()


class TestMainGroup:
    def test_help(self, runner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Synthkit" in result.output
        assert "doc" in result.output
        assert "email" in result.output
        assert "html" in result.output
        assert "pdf" in result.output


class TestDocSubcommand:
    def test_help(self, runner):
        result = runner.invoke(main, ["doc", "--help"])
        assert result.exit_code == 0
        assert "--hard-breaks" in result.output
        assert "--mermaid" in result.output

    @patch("synthkit.cli.batch_convert")
    def test_invokes_batch_convert(self, mock_batch, runner, tmp_md):
        runner.invoke(main, ["doc", str(tmp_md)])
        mock_batch.assert_called_once()
        args = mock_batch.call_args
        assert str(tmp_md) in args[0][0]  # files tuple
        assert args[0][1] is False  # hard_breaks
        assert args[0][2] is False  # mermaid

    @patch("synthkit.cli.batch_convert")
    def test_hard_breaks_flag(self, mock_batch, runner, tmp_md):
        runner.invoke(main, ["doc", "--hard-breaks", str(tmp_md)])
        assert mock_batch.call_args[0][1] is True

    @patch("synthkit.cli.batch_convert")
    def test_mermaid_flag(self, mock_batch, runner, tmp_md):
        runner.invoke(main, ["doc", "--mermaid", str(tmp_md)])
        assert mock_batch.call_args[0][2] is True


class TestEmailSubcommand:
    def test_help(self, runner):
        result = runner.invoke(main, ["email", "--help"])
        assert result.exit_code == 0
        assert "--hard-breaks" in result.output
        assert "--mermaid" in result.output

    @patch("synthkit.cli.email.convert")
    def test_invokes_convert(self, mock_convert, runner, tmp_md):
        runner.invoke(main, ["email", str(tmp_md)])
        mock_convert.assert_called_once()
        call_args = mock_convert.call_args[0]
        assert str(call_args[0]).endswith("test.md")
        assert call_args[1] is False  # hard_breaks
        assert call_args[2] is False  # mermaid

    @patch("synthkit.cli.email.convert")
    def test_flags(self, mock_convert, runner, tmp_md):
        runner.invoke(main, ["email", "--hard-breaks", "--mermaid", str(tmp_md)])
        call_args = mock_convert.call_args[0]
        assert call_args[1] is True
        assert call_args[2] is True

    def test_requires_file_argument(self, runner):
        result = runner.invoke(main, ["email"])
        assert result.exit_code != 0


class TestHtmlSubcommand:
    def test_help(self, runner):
        result = runner.invoke(main, ["html", "--help"])
        assert result.exit_code == 0
        assert "--hard-breaks" in result.output
        assert "--mermaid" in result.output

    @patch("synthkit.cli.batch_convert")
    def test_invokes_batch_convert(self, mock_batch, runner, tmp_md):
        runner.invoke(main, ["html", str(tmp_md)])
        mock_batch.assert_called_once()


class TestPdfSubcommand:
    def test_help(self, runner):
        result = runner.invoke(main, ["pdf", "--help"])
        assert result.exit_code == 0
        assert "--hard-breaks" in result.output
        assert "--mermaid" in result.output

    @patch("synthkit.cli.batch_convert")
    def test_invokes_batch_convert(self, mock_batch, runner, tmp_md):
        runner.invoke(main, ["pdf", str(tmp_md)])
        mock_batch.assert_called_once()


class TestIntegration:
    """Integration tests that run actual pandoc (bundled via pypandoc_binary)."""

    @patch("synthkit.html.config_path", return_value=None)
    def test_html_end_to_end(self, mock_config, tmp_md, monkeypatch):
        monkeypatch.chdir(tmp_md.parent)
        from synthkit.html import convert

        convert(tmp_md)
        output = tmp_md.parent / "test.html"
        assert output.exists()
        content = output.read_text()
        assert "<html" in content
        assert "Hello" in content

    @patch("synthkit.doc.config_path", return_value=None)
    def test_doc_end_to_end(self, mock_config, tmp_md, monkeypatch):
        monkeypatch.chdir(tmp_md.parent)
        from synthkit.doc import convert

        convert(tmp_md)
        output = tmp_md.parent / "test.docx"
        assert output.exists()
        assert output.stat().st_size > 0
