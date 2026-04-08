"""
Testes para agents/model_factory.py
"""

from unittest.mock import patch

from agents.model_factory import get_model


class TestGetModelGroq:
    def test_default_provider_returns_groq(self, monkeypatch):
        """Sem LLM_PROVIDER definido, retorna instância Groq."""
        monkeypatch.delenv("LLM_PROVIDER", raising=False)
        with patch("agno.models.groq.Groq") as mock_groq:
            result = get_model()
            mock_groq.assert_called_once_with(id="llama-3.3-70b-versatile")
            assert result == mock_groq.return_value

    def test_explicit_groq_provider(self, monkeypatch):
        """LLM_PROVIDER=groq retorna Groq."""
        monkeypatch.setenv("LLM_PROVIDER", "groq")
        with patch("agno.models.groq.Groq") as mock_groq:
            result = get_model()
            mock_groq.assert_called_once_with(id="llama-3.3-70b-versatile")
            assert result == mock_groq.return_value

    def test_groq_provider_case_insensitive(self, monkeypatch):
        """LLM_PROVIDER=GROQ (maiúsculo) retorna Groq."""
        monkeypatch.setenv("LLM_PROVIDER", "GROQ")
        with patch("agno.models.groq.Groq") as mock_groq:
            result = get_model()
            mock_groq.assert_called_once_with(id="llama-3.3-70b-versatile")

    def test_unknown_provider_falls_back_to_groq(self, monkeypatch):
        """Provedor desconhecido cai no fallback Groq."""
        monkeypatch.setenv("LLM_PROVIDER", "unknown_provider")
        with patch("agno.models.groq.Groq") as mock_groq:
            result = get_model()
            mock_groq.assert_called_once_with(id="llama-3.3-70b-versatile")


class TestGetModelOpenAI:
    def test_openai_provider_returns_openai_chat(self, monkeypatch):
        """LLM_PROVIDER=openai retorna OpenAIChat."""
        monkeypatch.setenv("LLM_PROVIDER", "openai")
        with patch("agno.models.openai.OpenAIChat") as mock_openai:
            result = get_model()
            mock_openai.assert_called_once_with(id="gpt-4o-mini")
            assert result == mock_openai.return_value

    def test_openai_provider_case_insensitive(self, monkeypatch):
        """LLM_PROVIDER=OPENAI (maiúsculo) retorna OpenAIChat."""
        monkeypatch.setenv("LLM_PROVIDER", "OPENAI")
        with patch("agno.models.openai.OpenAIChat") as mock_openai:
            result = get_model()
            mock_openai.assert_called_once_with(id="gpt-4o-mini")
