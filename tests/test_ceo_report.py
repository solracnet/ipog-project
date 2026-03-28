"""
Testes para agents/ceo_report.py
"""

import pytest

from agents.ceo_report import (
    get_executive_summary,
    get_revenue_by_region_and_segment,
    get_top_states,
    get_strategic_kpis,
    get_pareto_analysis,
    get_business_health_indicators,
)

FILENAME = "SampleSuperstore.csv"


class TestGetExecutiveSummary:
    def test_returns_string(self):
        result = get_executive_summary(FILENAME)
        assert isinstance(result, str)

    def test_contains_financial_section(self):
        result = get_executive_summary(FILENAME)
        assert "Financeiro" in result

    def test_contains_operational_section(self):
        result = get_executive_summary(FILENAME)
        assert "Indicadores Operacionais" in result

    def test_contains_key_kpis(self):
        result = get_executive_summary(FILENAME)
        assert "Receita Total" in result
        assert "Lucro Total" in result
        assert "Margem" in result


class TestGetRevenueByRegionAndSegment:
    def test_returns_string(self):
        result = get_revenue_by_region_and_segment(FILENAME)
        assert isinstance(result, str)

    def test_contains_region_and_segment(self):
        result = get_revenue_by_region_and_segment(FILENAME)
        assert "Region" in result or "Segment" in result

    def test_contains_margin(self):
        result = get_revenue_by_region_and_segment(FILENAME)
        assert "Margem" in result


class TestGetTopStates:
    def test_returns_string(self):
        result = get_top_states(FILENAME)
        assert isinstance(result, str)

    def test_default_n_is_10(self):
        result = get_top_states(FILENAME)
        assert "Top 10" in result

    def test_custom_n(self):
        result = get_top_states(FILENAME, n=5)
        assert "Top 5" in result

    def test_accepts_n_as_string(self):
        result = get_top_states(FILENAME, n="5")
        assert isinstance(result, str)

    def test_contains_state_column(self):
        result = get_top_states(FILENAME)
        assert "State" in result


class TestGetStrategicKpis:
    def test_returns_string(self):
        result = get_strategic_kpis(FILENAME)
        assert isinstance(result, str)

    def test_contains_coverage_section(self):
        result = get_strategic_kpis(FILENAME)
        assert "Abrangência" in result or "Portfólio" in result

    def test_contains_concentration_section(self):
        result = get_strategic_kpis(FILENAME)
        assert "Concentração" in result or "Risco" in result

    def test_contains_efficiency_section(self):
        result = get_strategic_kpis(FILENAME)
        assert "Eficiência" in result

    def test_contains_geographic_kpis(self):
        result = get_strategic_kpis(FILENAME)
        assert "Estados" in result or "Regiões" in result


class TestGetParetoAnalysis:
    def test_default_dimension_subcategory(self):
        result = get_pareto_analysis(FILENAME)
        assert isinstance(result, str)
        assert "Pareto" in result

    def test_by_state(self):
        result = get_pareto_analysis(FILENAME, "State")
        assert isinstance(result, str)

    def test_by_category(self):
        result = get_pareto_analysis(FILENAME, "Category")
        assert isinstance(result, str)

    def test_invalid_dimension_returns_error(self):
        result = get_pareto_analysis(FILENAME, "ColunaInexistente")
        assert "não encontrada" in result

    def test_contains_80_percent_reference(self):
        result = get_pareto_analysis(FILENAME)
        assert "80" in result


class TestGetBusinessHealthIndicators:
    def test_returns_string(self):
        result = get_business_health_indicators(FILENAME)
        assert isinstance(result, str)

    def test_contains_margin_distribution(self):
        result = get_business_health_indicators(FILENAME)
        assert "Margem" in result

    def test_contains_category_profit(self):
        result = get_business_health_indicators(FILENAME)
        assert "Categoria" in result or "Category" in result

    def test_contains_discount_dependency(self):
        result = get_business_health_indicators(FILENAME)
        assert "Desconto" in result or "Segmento" in result
