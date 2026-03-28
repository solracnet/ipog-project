"""
Testes para agents/metrics_agent.py
"""

import pytest

from agents.metrics_agent import (
    identify_available_kpis,
    get_kpi_dashboard,
    get_margin_by_dimension,
    get_top_performers,
    get_bottom_performers,
    detect_loss_makers,
    get_discount_impact,
)

FILENAME = "SampleSuperstore.csv"


class TestIdentifyAvailableKpis:
    def test_returns_string(self):
        result = identify_available_kpis(FILENAME)
        assert isinstance(result, str)

    def test_contains_kpi_section(self):
        result = identify_available_kpis(FILENAME)
        assert "KPI" in result

    def test_lists_financial_kpis(self):
        result = identify_available_kpis(FILENAME)
        assert "Sales" in result
        assert "Profit" in result


class TestGetKpiDashboard:
    def test_returns_string(self):
        result = get_kpi_dashboard(FILENAME)
        assert isinstance(result, str)

    def test_contains_financial_section(self):
        result = get_kpi_dashboard(FILENAME)
        assert "Financeiro" in result

    def test_contains_volume_section(self):
        result = get_kpi_dashboard(FILENAME)
        assert "Volume" in result

    def test_shows_total_sales(self):
        result = get_kpi_dashboard(FILENAME)
        assert "Receita Total" in result


class TestGetMarginByDimension:
    def test_by_region(self):
        result = get_margin_by_dimension(FILENAME, "Region")
        assert isinstance(result, str)
        assert "Margem" in result

    def test_by_category(self):
        result = get_margin_by_dimension(FILENAME, "Category")
        assert isinstance(result, str)

    def test_by_segment(self):
        result = get_margin_by_dimension(FILENAME, "Segment")
        assert isinstance(result, str)

    def test_invalid_dimension_returns_error(self):
        result = get_margin_by_dimension(FILENAME, "ColunaInexistente")
        assert "não encontrada" in result


class TestGetTopPerformers:
    def test_returns_string(self):
        result = get_top_performers(FILENAME, "Sub-Category", "Profit", 5)
        assert isinstance(result, str)

    def test_respects_n(self):
        result = get_top_performers(FILENAME, "Sub-Category", "Profit", 3)
        assert "Top 3" in result

    def test_accepts_n_as_string(self):
        result = get_top_performers(FILENAME, "Region", "Sales", "5")
        assert isinstance(result, str)

    def test_invalid_dimension_returns_error(self):
        result = get_top_performers(FILENAME, "ColunaErrada", "Sales", 5)
        assert "não encontrada" in result

    def test_invalid_metric_returns_error(self):
        result = get_top_performers(FILENAME, "Region", "MetricaErrada", 5)
        assert "não encontrada" in result


class TestGetBottomPerformers:
    def test_returns_string(self):
        result = get_bottom_performers(FILENAME, "Sub-Category", "Profit", 5)
        assert isinstance(result, str)

    def test_accepts_n_as_string(self):
        result = get_bottom_performers(FILENAME, "Region", "Sales", "3")
        assert isinstance(result, str)

    def test_invalid_dimension_returns_error(self):
        result = get_bottom_performers(FILENAME, "ColunaErrada", "Profit", 5)
        assert "não encontrada" in result


class TestDetectLossMakers:
    def test_returns_string(self):
        result = detect_loss_makers(FILENAME)
        assert isinstance(result, str)

    def test_default_dimension_is_subcategory(self):
        result = detect_loss_makers(FILENAME)
        assert "Sub-Category" in result or "Prejuízo" in result or "encontrado" in result

    def test_by_region(self):
        result = detect_loss_makers(FILENAME, "Region")
        assert isinstance(result, str)

    def test_invalid_dimension_returns_error(self):
        result = detect_loss_makers(FILENAME, "ColunaInexistente")
        assert "não encontrada" in result


class TestGetDiscountImpact:
    def test_returns_string(self):
        result = get_discount_impact(FILENAME)
        assert isinstance(result, str)

    def test_contains_discount_bands(self):
        result = get_discount_impact(FILENAME)
        assert "Desconto" in result

    def test_contains_margin(self):
        result = get_discount_impact(FILENAME)
        assert "Margem" in result
