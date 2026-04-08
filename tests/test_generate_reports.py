"""
Testes para generate_reports.py
"""

from pathlib import Path
from unittest.mock import MagicMock, patch


class TestRunAgent:
    def test_stores_response_content(self):
        """_run_agent armazena o conteúdo da resposta no dict result."""
        from generate_reports import _run_agent

        mock_response = MagicMock()
        mock_response.content = "Relatório gerado"

        mock_agent = MagicMock()
        mock_agent.run.return_value = mock_response

        config = {
            "tools": [],
            "instructions": "instrução",
            "prompt": "gere o relatório",
        }
        result = {}

        with patch("generate_reports.Agent", return_value=mock_agent):
            with patch("generate_reports.get_model"):
                _run_agent(config, result)

        assert result["content"] == "Relatório gerado"

    def test_stores_empty_string_when_content_is_none(self):
        """_run_agent armazena string vazia quando response.content é None."""
        from generate_reports import _run_agent

        mock_response = MagicMock()
        mock_response.content = None

        mock_agent = MagicMock()
        mock_agent.run.return_value = mock_response

        config = {
            "tools": [],
            "instructions": "instrução",
            "prompt": "gere o relatório",
        }
        result = {}

        with patch("generate_reports.Agent", return_value=mock_agent):
            with patch("generate_reports.get_model"):
                _run_agent(config, result)

        assert result["content"] == ""

    def test_agent_created_with_markdown_true(self):
        """Agent é sempre instanciado com markdown=True."""
        from generate_reports import _run_agent

        mock_agent = MagicMock()
        mock_agent.run.return_value = MagicMock(content="ok")

        config = {
            "tools": [],
            "instructions": "instrução",
            "prompt": "prompt",
        }

        with patch("generate_reports.Agent", return_value=mock_agent) as mock_cls:
            with patch("generate_reports.get_model"):
                _run_agent(config, {})

        _, kwargs = mock_cls.call_args
        assert kwargs.get("markdown") is True


class TestRunReport:
    def test_writes_content_to_output_file(self, tmp_path):
        """run_report salva o conteúdo gerado pelo agente no arquivo de saída."""
        from generate_reports import run_report

        output_file = tmp_path / "report.md"
        config = {
            "label": "Teste",
            "tools": [],
            "instructions": "instrução",
            "prompt": "prompt",
            "output": output_file,
        }

        with patch("generate_reports.Agent") as mock_cls:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="# Relatório Teste")
            mock_cls.return_value = mock_agent
            with patch("generate_reports.get_model"):
                run_report(config, 1, 1)

        assert output_file.read_text(encoding="utf-8") == "# Relatório Teste"

    def test_returns_elapsed_time(self, tmp_path):
        """run_report retorna o tempo decorrido como float."""
        from generate_reports import run_report

        output_file = tmp_path / "report.md"
        config = {
            "label": "Teste",
            "tools": [],
            "instructions": "instrução",
            "prompt": "prompt",
            "output": output_file,
        }

        with patch("generate_reports.Agent") as mock_cls:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="conteúdo")
            mock_cls.return_value = mock_agent
            with patch("generate_reports.get_model"):
                elapsed = run_report(config, 1, 3)

        assert isinstance(elapsed, float)
        assert elapsed >= 0

    def test_writes_empty_string_when_content_missing(self, tmp_path):
        """run_report grava string vazia se o agente não retornar conteúdo."""
        from generate_reports import run_report

        output_file = tmp_path / "report.md"
        config = {
            "label": "Teste",
            "tools": [],
            "instructions": "instrução",
            "prompt": "prompt",
            "output": output_file,
        }

        with patch("generate_reports.Agent") as mock_cls:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content=None)
            mock_cls.return_value = mock_agent
            with patch("generate_reports.get_model"):
                run_report(config, 1, 1)

        assert output_file.read_text(encoding="utf-8") == ""
