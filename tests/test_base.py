"""Tests for synthkit.base module."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from synthkit.base import (
    BASE_FORMAT,
    ConversionError,
    batch_convert,
    build_format,
    cleanup_mermaid_err,
    config_path,
    mermaid_args,
    run_pandoc,
)


class TestBuildFormat:
    def test_default_format(self):
        assert build_format() == "markdown+lists_without_preceding_blankline"

    def test_hard_breaks_false(self):
        assert build_format(hard_breaks=False) == BASE_FORMAT

    def test_hard_breaks_true(self):
        result = build_format(hard_breaks=True)
        assert result == f"{BASE_FORMAT}+hard_line_breaks"
        assert result.endswith("+hard_line_breaks")


class TestConfigPath:
    def test_returns_none_when_missing(self, tmp_path):
        with patch("synthkit.base.Path.home", return_value=tmp_path):
            assert config_path("md2doc", "reference.docx") is None

    def test_returns_path_when_exists(self, tmp_path):
        cfg = tmp_path / ".config" / "md2doc"
        cfg.mkdir(parents=True)
        ref = cfg / "reference.docx"
        ref.write_bytes(b"fake docx")
        with patch("synthkit.base.Path.home", return_value=tmp_path):
            result = config_path("md2doc", "reference.docx")
            assert result == ref

    def test_returns_none_for_directory(self, tmp_path):
        cfg = tmp_path / ".config" / "md2html" / "style.css"
        cfg.mkdir(parents=True)  # style.css is a dir, not a file
        with patch("synthkit.base.Path.home", return_value=tmp_path):
            assert config_path("md2html", "style.css") is None


class TestMermaidArgs:
    def test_mermaid_false(self):
        assert mermaid_args(False) == []

    def test_mermaid_true(self):
        assert mermaid_args(True) == ["--filter", "mermaid-filter"]


class TestCleanupMermaidErr:
    def test_removes_empty_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        err = tmp_path / "mermaid-filter.err"
        err.write_text("")
        cleanup_mermaid_err()
        assert not err.exists()

    def test_keeps_nonempty_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        err = tmp_path / "mermaid-filter.err"
        err.write_text("some error")
        cleanup_mermaid_err()
        assert err.exists()

    def test_noop_when_no_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        cleanup_mermaid_err()  # Should not raise


class TestRunPandoc:
    @patch("synthkit.base.get_pandoc_bin", return_value="/usr/bin/pandoc")
    @patch("synthkit.base.subprocess.run")
    def test_calls_pandoc_with_args(self, mock_run, mock_bin):
        mock_run.return_value = subprocess.CompletedProcess([], 0)
        run_pandoc(["-f", "markdown", "-t", "html"])
        mock_run.assert_called_once_with(
            ["/usr/bin/pandoc", "-f", "markdown", "-t", "html"],
            capture_output=False,
            env=None,
        )


class TestBatchConvert:
    def test_exits_with_no_files(self):
        with pytest.raises(SystemExit) as exc_info:
            batch_convert((), False, False, lambda *a: None)
        assert exc_info.value.code == 1

    def test_skips_non_md_files(self, non_md_file, capsys):
        converter = MagicMock()
        batch_convert((str(non_md_file),), False, False, converter)
        converter.assert_not_called()
        out = capsys.readouterr().out
        assert "Skipping non-markdown file" in out

    def test_reports_missing_files(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            batch_convert(("/nonexistent/file.md",), False, False, lambda *a: None)
        assert exc_info.value.code == 1
        out = capsys.readouterr().out
        assert "not found" in out

    def test_successful_conversion(self, tmp_md, capsys):
        converter = MagicMock()
        batch_convert((str(tmp_md),), False, False, converter)
        converter.assert_called_once_with(tmp_md, False, False)
        out = capsys.readouterr().out
        assert "1 succeeded, 0 failed" in out

    def test_failed_conversion(self, tmp_md, capsys):
        def failing_converter(path, hard_breaks, mermaid):
            raise ConversionError("pandoc exploded")

        with pytest.raises(SystemExit) as exc_info:
            batch_convert((str(tmp_md),), False, False, failing_converter)
        assert exc_info.value.code == 1
        out = capsys.readouterr().out
        assert "0 succeeded, 1 failed" in out
        assert "pandoc exploded" in out

    def test_passes_hard_breaks_and_mermaid(self, tmp_md):
        converter = MagicMock()
        batch_convert((str(tmp_md),), True, True, converter)
        converter.assert_called_once_with(tmp_md, True, True)

    def test_batch_multiple_files(self, multiple_md, capsys):
        converter = MagicMock()
        files = tuple(str(multiple_md / f) for f in ("a.md", "b.md", "c.md"))
        batch_convert(files, False, False, converter)
        assert converter.call_count == 3
        out = capsys.readouterr().out
        assert "3 succeeded, 0 failed" in out

    def test_cleans_mermaid_err_when_mermaid_enabled(self, tmp_md, monkeypatch):
        monkeypatch.chdir(tmp_md.parent)
        err = tmp_md.parent / "mermaid-filter.err"
        err.write_text("")
        batch_convert((str(tmp_md),), False, True, MagicMock())
        assert not err.exists()

    def test_no_mermaid_cleanup_when_disabled(self, tmp_md, monkeypatch):
        monkeypatch.chdir(tmp_md.parent)
        err = tmp_md.parent / "mermaid-filter.err"
        err.write_text("")
        batch_convert((str(tmp_md),), False, False, MagicMock())
        assert err.exists()
