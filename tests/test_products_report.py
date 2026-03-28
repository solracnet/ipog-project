"""
Testes para agents/products_report.py
"""

import pytest

from agents.products_report import (
    get_sales_by_category,
    get_sales_by_subcategory,
    get_loss_making_products,
    get_discount_by_category,
    get_top_profitable_subcategories,
    get_category_profitability_ranking,
    get_category_by_region,
    get_shipping_by_category,
    get_shipping_profitability,
    get_product_volume_vs_profit,
)

FILENAME = "SampleSuperstore.csv"


class TestGetSalesByCategory:
    def test_returns_string(self):
        result = get_sales_by_category(FILENAME)
        assert isinstance(result, str)

    def test_contains_categories(self):
        result = get_sales_by_category(FILENAME)
        assert "Furniture" in result or "Technology" in result or "Office Supplies" in result

    def test_contains_margin(self):
        result = get_sales_by_category(FILENAME)
        assert "Margem" in result


class TestGetSalesBySubcategory:
    def test_returns_string(self):
        result = get_sales_by_subcategory(FILENAME)
        assert isinstance(result, str)

    def test_contains_subcategory_column(self):
        result = get_sales_by_subcategory(FILENAME)
        assert "Sub-Category" in result

    def test_contains_discount(self):
        result = get_sales_by_subcategory(FILENAME)
        assert "Desconto" in result


class TestGetLossMakingProducts:
    def test_returns_string(self):
        result = get_loss_making_products(FILENAME)
        assert isinstance(result, str)

    def test_returns_either_losses_or_none_message(self):
        result = get_loss_making_products(FILENAME)
        assert "Prejuízo" in result or "Nenhuma" in result

    def test_loss_entries_have_negative_profit(self):
        result = get_loss_making_products(FILENAME)
        # Se encontrou perdas, deve conter o sinal de negativo
        if "Nenhuma" not in result:
            assert "-" in result


class TestGetDiscountByCategory:
    def test_returns_string(self):
        result = get_discount_by_category(FILENAME)
        assert isinstance(result, str)

    def test_contains_discount_column(self):
        result = get_discount_by_category(FILENAME)
        assert "Desconto" in result

    def test_contains_margin_column(self):
        result = get_discount_by_category(FILENAME)
        assert "Margem" in result


class TestGetTopProfitableSubcategories:
    def test_returns_string(self):
        result = get_top_profitable_subcategories(FILENAME)
        assert isinstance(result, str)

    def test_default_n_is_5(self):
        result = get_top_profitable_subcategories(FILENAME)
        assert "Top 5" in result

    def test_custom_n(self):
        result = get_top_profitable_subcategories(FILENAME, n=3)
        assert "Top 3" in result

    def test_accepts_n_as_string(self):
        result = get_top_profitable_subcategories(FILENAME, n="3")
        assert isinstance(result, str)


class TestGetCategoryProfitabilityRanking:
    def test_returns_string(self):
        result = get_category_profitability_ranking(FILENAME)
        assert isinstance(result, str)

    def test_contains_classification(self):
        result = get_category_profitability_ranking(FILENAME)
        assert "Classificacao" in result or "Excelente" in result or "Prejuízo" in result

    def test_contains_margin(self):
        result = get_category_profitability_ranking(FILENAME)
        assert "Margem" in result


class TestGetCategoryByRegion:
    def test_returns_string(self):
        result = get_category_by_region(FILENAME)
        assert isinstance(result, str)

    def test_contains_region(self):
        result = get_category_by_region(FILENAME)
        assert "Region" in result

    def test_contains_category(self):
        result = get_category_by_region(FILENAME)
        assert "Category" in result


class TestGetShippingByCategory:
    def test_returns_string(self):
        result = get_shipping_by_category(FILENAME)
        assert isinstance(result, str)

    def test_contains_ship_mode(self):
        result = get_shipping_by_category(FILENAME)
        assert "Ship Mode" in result

    def test_contains_margin(self):
        result = get_shipping_by_category(FILENAME)
        assert "Margem" in result


class TestGetShippingProfitability:
    def test_returns_string(self):
        result = get_shipping_profitability(FILENAME)
        assert isinstance(result, str)

    def test_contains_ship_mode(self):
        result = get_shipping_profitability(FILENAME)
        assert "Ship Mode" in result

    def test_contains_margin(self):
        result = get_shipping_profitability(FILENAME)
        assert "Margem" in result


class TestGetProductVolumeVsProfit:
    def test_returns_string(self):
        result = get_product_volume_vs_profit(FILENAME)
        assert isinstance(result, str)

    def test_contains_quantity(self):
        result = get_product_volume_vs_profit(FILENAME)
        assert "Qty" in result or "Quantity" in result

    def test_contains_profit_per_unit(self):
        result = get_product_volume_vs_profit(FILENAME)
        assert "Lucro_por_Unidade" in result

    def test_contains_revenue_per_unit(self):
        result = get_product_volume_vs_profit(FILENAME)
        assert "Receita_por_Unidade" in result
