"""
Testes para agents/agno_workflow.py
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from agents.agno_workflow import (
    AnalyticsWorkflow,
    _contains_any,
    _prepare_input,
    _DEFAULT_FILE,
    _KEYWORDS_DADOS,
    _KEYWORDS_METRICAS,
    _KEYWORDS_CEO,
    _KEYWORDS_VENDAS,
    _KEYWORDS_PRODUTOS,
)
from agno.workflow.types import StepInput, StepOutput


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

class TestContainsAny:
    def test_matches_keyword(self):
        assert _contains_any("quero ver o arquivo csv", {"arquivo", "dados"}) is True

    def test_no_match(self):
        assert _contains_any("relatório de vendas", {"arquivo", "csv"}) is False

    def test_case_sensitive(self):
        # _contains_any não é case-insensitive — o chamador deve lower() antes
        assert _contains_any("ARQUIVO", {"arquivo"}) is False

    def test_empty_keywords(self):
        assert _contains_any("qualquer texto", set()) is False

    def test_empty_text(self):
        assert _contains_any("", {"dados"}) is False


class TestPrepareInput:
    def _make_input(self, text: str) -> StepInput:
        return StepInput(input=text)

    def test_injects_default_file_when_absent(self):
        step_input = self._make_input("mostre os dados")
        result = _prepare_input(step_input)
        assert _DEFAULT_FILE in result.content
        assert result.success is True

    def test_does_not_duplicate_when_file_already_present(self):
        text = f"analise o arquivo {_DEFAULT_FILE}"
        step_input = self._make_input(text)
        result = _prepare_input(step_input)
        assert result.content.count(_DEFAULT_FILE) == 1

    def test_does_not_inject_when_csv_extension_present(self):
        text = "carregue o arquivo dados.csv"
        step_input = self._make_input(text)
        result = _prepare_input(step_input)
        # Não deve injetar o arquivo padrão pois já há .csv na entrada
        assert _DEFAULT_FILE not in result.content

    def test_preserves_original_text(self):
        text = "pergunta qualquer"
        step_input = self._make_input(text)
        result = _prepare_input(step_input)
        assert text in result.content

    def test_empty_input_becomes_default_file_reference(self):
        step_input = self._make_input("")
        result = _prepare_input(step_input)
        assert _DEFAULT_FILE in result.content

    def test_returns_step_output_instance(self):
        step_input = self._make_input("qualquer pergunta")
        result = _prepare_input(step_input)
        assert isinstance(result, StepOutput)


# ---------------------------------------------------------------------------
# Keywords de roteamento
# ---------------------------------------------------------------------------

class TestRoutingKeywords:
    def test_dados_keywords_are_set(self):
        assert len(_KEYWORDS_DADOS) > 0

    def test_metricas_keywords_are_set(self):
        assert len(_KEYWORDS_METRICAS) > 0

    def test_ceo_keywords_are_set(self):
        assert len(_KEYWORDS_CEO) > 0

    def test_vendas_keywords_are_set(self):
        assert len(_KEYWORDS_VENDAS) > 0

    def test_produtos_keywords_are_set(self):
        assert len(_KEYWORDS_PRODUTOS) > 0

    def test_dados_detects_arquivo(self):
        assert _contains_any("arquivo csv disponível", _KEYWORDS_DADOS)

    def test_metricas_detects_kpi(self):
        assert _contains_any("mostre os kpis", _KEYWORDS_METRICAS)

    def test_ceo_detects_executivo(self):
        assert _contains_any("relatório executivo do negócio", _KEYWORDS_CEO)

    def test_vendas_detects_regiao(self):
        assert _contains_any("vendas por região", _KEYWORDS_VENDAS)

    def test_produtos_detects_categoria(self):
        assert _contains_any("análise de categoria", _KEYWORDS_PRODUTOS)


# ---------------------------------------------------------------------------
# AnalyticsWorkflow
# ---------------------------------------------------------------------------

class TestAnalyticsWorkflowInstantiation:
    @pytest.fixture(autouse=True)
    def ensure_db_dir(self, tmp_path):
        self.db_path = str(tmp_path / "history.db")

    def test_instantiates_without_error(self):
        wf = AnalyticsWorkflow(db_path=self.db_path)
        assert wf is not None

    def test_workflow_name(self):
        wf = AnalyticsWorkflow(db_path=self.db_path)
        assert wf.workflow.name == "IPOG Analytics Workflow"

    def test_workflow_description_set(self):
        wf = AnalyticsWorkflow(db_path=self.db_path)
        assert wf.workflow.description is not None
        assert len(wf.workflow.description) > 0

    def test_workflow_has_two_steps(self):
        wf = AnalyticsWorkflow(db_path=self.db_path)
        assert len(wf.workflow.steps) == 2

    def test_first_step_is_preparacao(self):
        wf = AnalyticsWorkflow(db_path=self.db_path)
        assert wf.workflow.steps[0].name == "Preparação"

    def test_second_step_is_router(self):
        wf = AnalyticsWorkflow(db_path=self.db_path)
        assert wf.workflow.steps[1].name == "Roteador de Intenção"

    def test_router_has_six_choices(self):
        wf = AnalyticsWorkflow(db_path=self.db_path)
        router = wf.workflow.steps[1]
        assert len(router.choices) == 6

    def test_router_choice_names(self):
        wf = AnalyticsWorkflow(db_path=self.db_path)
        router = wf.workflow.steps[1]
        names = [c.name for c in router.choices]
        assert "Dados" in names
        assert "Métricas" in names
        assert "Executivo" in names
        assert "Vendas" in names
        assert "Produtos" in names
        assert "Team Completo" in names

    def test_exposes_teams_instance(self):
        from agents.agno_teams import agno_teams
        wf = AnalyticsWorkflow(db_path=self.db_path)
        assert isinstance(wf._teams, agno_teams)


class TestAnalyticsWorkflowRouting:
    """Testa o seletor do Router diretamente, sem chamar o LLM.

    O router usa step_input.input (query original do usuário),
    NÃO previous_step_content — que contém "arquivo" e "sample"
    injetados pela etapa de Preparação, o que causaria falso-positivo
    em _KEYWORDS_DADOS para toda e qualquer pergunta.
    """

    @pytest.fixture
    def workflow(self, tmp_path):
        return AnalyticsWorkflow(db_path=str(tmp_path / "history.db"))

    def _make_input(self, input_text: str = "", previous_content: str = "") -> StepInput:
        si = StepInput(input=input_text)
        si.previous_step_content = previous_content
        return si

    def _get_selector(self, workflow):
        """Retorna a função seletora do Router."""
        return workflow.workflow.steps[1].selector

    def test_routes_to_dados_for_arquivo(self, workflow):
        selector = self._get_selector(workflow)
        result = selector(self._make_input(input_text="liste os arquivos disponíveis"))
        assert result[0].name == "Dados"

    def test_routes_to_metricas_for_kpi(self, workflow):
        selector = self._get_selector(workflow)
        result = selector(self._make_input(input_text="quero ver os kpis do dataset"))
        assert result[0].name == "Métricas"

    def test_routes_to_executivo_for_ceo(self, workflow):
        selector = self._get_selector(workflow)
        result = selector(self._make_input(input_text="gere o relatório executivo para o ceo"))
        assert result[0].name == "Executivo"

    def test_routes_to_vendas_for_regiao(self, workflow):
        selector = self._get_selector(workflow)
        result = selector(self._make_input(input_text="análise de vendas por região"))
        assert result[0].name == "Vendas"

    def test_routes_to_produtos_for_subcategoria(self, workflow):
        selector = self._get_selector(workflow)
        result = selector(self._make_input(input_text="análise de subcategoria e portfólio"))
        assert result[0].name == "Produtos"

    def test_routes_to_team_completo_for_unknown(self, workflow):
        selector = self._get_selector(workflow)
        result = selector(self._make_input(input_text="quero uma análise completa geral"))
        assert result[0].name == "Team Completo"

    def test_previous_content_with_arquivo_does_not_override_routing(self, workflow):
        """Bug original: previous_content com 'arquivo' desviava toda query para step_dados."""
        selector = self._get_selector(workflow)
        # Simula exatamente o que a etapa de Preparação injeta
        enriched = "gere o relatório do ceo\n\n> **arquivo:** samplesuperstore.csv"
        # Com o fix, o router usa input_text, não previous_content
        result = selector(self._make_input(
            input_text="gere o relatório do ceo",
            previous_content=enriched,
        ))
        assert result[0].name == "Executivo"  # deve rotear para CEO, não para Dados

    def test_sample_keyword_in_filename_does_not_override_routing(self, workflow):
        """Bug original: 'sample' em SampleSuperstore.csv desviava para step_dados."""
        selector = self._get_selector(workflow)
        enriched = "gere relatório de vendas\n\n> **arquivo:** samplesuperstore.csv"
        result = selector(self._make_input(
            input_text="gere relatório de vendas",
            previous_content=enriched,
        ))
        assert result[0].name == "Vendas"  # deve rotear para Vendas, não para Dados

    def test_selector_always_returns_list(self, workflow):
        selector = self._get_selector(workflow)
        queries = [
            "liste os arquivos",
            "mostre os kpis",
            "relatório para o ceo",
            "análise de vendas",
            "portfólio de produtos",
            "pergunta aleatória",
        ]
        for text in queries:
            result = selector(self._make_input(input_text=text))
            assert isinstance(result, list)
            assert len(result) == 1
