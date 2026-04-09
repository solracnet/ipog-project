"""
Testes para agents/agno_teams.py
"""

from unittest.mock import MagicMock, patch

import pytest

from agno.team.team import TeamMode


class TestAgnoTeamsInstantiation:
    def test_instantiates_with_default_model(self):
        """agno_teams instancia sem erros usando o modelo padrão."""
        from agents.agno_teams import agno_teams
        t = agno_teams()
        assert t.team is not None

    def test_instantiates_with_explicit_groq_model(self):
        """agno_teams aceita um modelo Groq explícito."""
        from agno.models.groq import Groq
        from agents.agno_teams import agno_teams
        t = agno_teams(model=Groq(id="llama-3.3-70b-versatile"))
        assert t.team is not None

    def test_team_name(self):
        from agents.agno_teams import agno_teams
        t = agno_teams()
        assert t.team.name == "IPOG Analytics Team"

    def test_team_mode_is_coordinate(self):
        from agents.agno_teams import agno_teams
        t = agno_teams()
        assert t.team.mode == TeamMode.coordinate

    def test_team_role_is_set(self):
        from agents.agno_teams import agno_teams
        t = agno_teams()
        assert t.team.role is not None
        assert len(t.team.role) > 0

    def test_team_has_five_members(self):
        from agents.agno_teams import agno_teams
        t = agno_teams()
        assert len(t.team.members) == 5

    def test_team_markdown_enabled(self):
        from agents.agno_teams import agno_teams
        t = agno_teams()
        assert t.team.markdown is True


class TestAgnoTeamsMembers:
    @pytest.fixture
    def teams(self):
        from agents.agno_teams import agno_teams
        return agno_teams()

    def test_data_analyst_exists(self, teams):
        assert teams.data_analyst is not None
        assert teams.data_analyst.name == "Analista de Dados"

    def test_metrics_analyst_exists(self, teams):
        assert teams.metrics_analyst is not None
        assert teams.metrics_analyst.name == "Analista de Métricas"

    def test_ceo_analyst_exists(self, teams):
        assert teams.ceo_analyst is not None
        assert teams.ceo_analyst.name == "Analista Executivo"

    def test_sales_analyst_exists(self, teams):
        assert teams.sales_analyst is not None
        assert teams.sales_analyst.name == "Analista de Vendas"

    def test_products_analyst_exists(self, teams):
        assert teams.products_analyst is not None
        assert teams.products_analyst.name == "Analista de Produtos"

    def test_member_names_in_team(self, teams):
        names = [m.name for m in teams.team.members]
        assert "Analista de Dados" in names
        assert "Analista de Métricas" in names
        assert "Analista Executivo" in names
        assert "Analista de Vendas" in names
        assert "Analista de Produtos" in names

    def test_each_member_has_role(self, teams):
        for member in teams.team.members:
            assert member.role is not None and len(member.role) > 0

    def test_each_member_has_tools(self, teams):
        for member in teams.team.members:
            assert member.tools is not None and len(member.tools) > 0

    def test_each_member_has_instructions(self, teams):
        for member in teams.team.members:
            assert member.instructions is not None

    def test_each_member_has_markdown_enabled(self, teams):
        for member in teams.team.members:
            assert member.markdown is True

    def test_data_analyst_tool_count(self, teams):
        from agents.excel_analyst import EXCEL_TOOLS
        assert len(teams.data_analyst.tools) == len(EXCEL_TOOLS)

    def test_metrics_analyst_tool_count(self, teams):
        from agents.metrics_agent import METRICS_TOOLS
        assert len(teams.metrics_analyst.tools) == len(METRICS_TOOLS)

    def test_ceo_analyst_tool_count(self, teams):
        from agents.ceo_report import CEO_REPORT_TOOLS
        assert len(teams.ceo_analyst.tools) == len(CEO_REPORT_TOOLS)

    def test_sales_analyst_tool_count(self, teams):
        from agents.sales_report import SALES_REPORT_TOOLS
        assert len(teams.sales_analyst.tools) == len(SALES_REPORT_TOOLS)

    def test_products_analyst_tool_count(self, teams):
        from agents.products_report import PRODUCTS_REPORT_TOOLS
        assert len(teams.products_analyst.tools) == len(PRODUCTS_REPORT_TOOLS)
