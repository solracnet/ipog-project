"""
Testes para agents/sales_report.py
"""

import pytest

from agents.sales_report import (
    get_sales_by_region,
    get_sales_by_segment,
    get_sales_by_shipping_mode,
    get_discount_impact_on_sales,
    get_region_segment_ranking,
    get_regional_performance_detail,
    get_city_performance,
    get_segment_deep_dive,
    get_sales_by_period,
    get_sales_by_salesperson,
)

FILENAME = "SampleSuperstore.csv"


class TestGetSalesByRegion:
    def test_returns_string(self):
        result = get_sales_by_region(FILENAME)
        assert isinstance(result, str)

    def test_contains_region_column(self):
        result = get_sales_by_region(FILENAME)
        assert "Region" in result

    def test_contains_margin(self):
        result = get_sales_by_region(FILENAME)
        assert "Margem" in result


class TestGetSalesBySegment:
    def test_returns_string(self):
        result = get_sales_by_segment(FILENAME)
        assert isinstance(result, str)

    def test_contains_segment_values(self):
        result = get_sales_by_segment(FILENAME)
        assert "Consumer" in result or "Corporate" in result

    def test_contains_ticket_medio(self):
        result = get_sales_by_segment(FILENAME)
        assert "Ticket" in result


class TestGetSalesByShippingMode:
    def test_returns_string(self):
        result = get_sales_by_shipping_mode(FILENAME)
        assert isinstance(result, str)

    def test_contains_ship_mode_values(self):
        result = get_sales_by_shipping_mode(FILENAME)
        assert "Class" in result or "Same Day" in result

    def test_contains_discount(self):
        result = get_sales_by_shipping_mode(FILENAME)
        assert "Desconto" in result


class TestGetDiscountImpactOnSales:
    def test_returns_string(self):
        result = get_discount_impact_on_sales(FILENAME)
        assert isinstance(result, str)

    def test_contains_discount_bands(self):
        result = get_discount_impact_on_sales(FILENAME)
        assert "%" in result

    def test_contains_margin(self):
        result = get_discount_impact_on_sales(FILENAME)
        assert "Margem" in result


class TestGetRegionSegmentRanking:
    def test_returns_string(self):
        result = get_region_segment_ranking(FILENAME)
        assert isinstance(result, str)

    def test_contains_region_and_segment(self):
        result = get_region_segment_ranking(FILENAME)
        assert "Region" in result
        assert "Segment" in result


class TestGetRegionalPerformanceDetail:
    def test_returns_string(self):
        result = get_regional_performance_detail(FILENAME)
        assert isinstance(result, str)

    def test_contains_category(self):
        result = get_regional_performance_detail(FILENAME)
        assert "Category" in result

    def test_contains_region(self):
        result = get_regional_performance_detail(FILENAME)
        assert "Region" in result


class TestGetCityPerformance:
    def test_returns_all_cities(self):
        result = get_city_performance(FILENAME)
        assert isinstance(result, str)
        assert "City" in result

    def test_filter_by_region(self):
        result = get_city_performance(FILENAME, region="West")
        assert isinstance(result, str)
        assert "West" in result

    def test_filter_case_insensitive(self):
        result = get_city_performance(FILENAME, region="west")
        assert isinstance(result, str)

    def test_invalid_region_returns_message(self):
        result = get_city_performance(FILENAME, region="Marte")
        assert "não encontrada" in result


class TestGetSegmentDeepDive:
    def test_returns_all_segments(self):
        result = get_segment_deep_dive(FILENAME)
        assert isinstance(result, str)

    def test_filter_by_segment(self):
        result = get_segment_deep_dive(FILENAME, segment="Consumer")
        assert isinstance(result, str)
        assert "Consumer" in result

    def test_invalid_segment_returns_message(self):
        result = get_segment_deep_dive(FILENAME, segment="SegmentoInexistente")
        assert "não encontrado" in result


class TestGetSalesByPeriod:
    def test_returns_string(self):
        result = get_sales_by_period(FILENAME)
        assert isinstance(result, str)

    def test_informs_missing_date_column(self):
        # O dataset atual não possui coluna de data
        result = get_sales_by_period(FILENAME)
        assert "não encontrada" in result or "Order Date" in result


class TestGetSalesBySalesperson:
    def test_returns_string(self):
        result = get_sales_by_salesperson(FILENAME)
        assert isinstance(result, str)

    def test_informs_missing_salesperson_column(self):
        # O dataset atual não possui coluna de vendedor
        result = get_sales_by_salesperson(FILENAME)
        assert "não encontrada" in result or "Sales Rep" in result
