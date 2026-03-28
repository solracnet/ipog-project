"""
Testes para agents/excel_analyst.py
"""

from unittest.mock import patch
import pandas as pd
import pytest

from agents.excel_analyst import (
    _load_file,
    _df_to_markdown,
    list_available_files,
    get_file_schema,
    get_data_sample,
    get_statistical_summary,
    get_unique_values,
    aggregate_data,
    filter_data,
    search_in_data,
)

FILENAME = "SampleSuperstore.csv"


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

class TestLoadFile:
    def test_loads_csv_successfully(self):
        df = _load_file(FILENAME)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_raises_for_missing_file(self):
        with pytest.raises(FileNotFoundError):
            _load_file("nao_existe.csv")

    def test_raises_for_unsupported_format(self, tmp_path):
        fake = tmp_path / "file.json"
        fake.write_text("{}")
        with patch("agents.excel_analyst.DATA_DIR", tmp_path):
            with pytest.raises(ValueError, match="não suportado"):
                _load_file("file.json")


class TestDfToMarkdown:
    def test_returns_string(self, sample_df):
        result = _df_to_markdown(sample_df)
        assert isinstance(result, str)

    def test_respects_max_rows(self, sample_df):
        result = _df_to_markdown(sample_df, max_rows=2)
        assert "exibindo 2 de 4 linhas" in result

    def test_no_footer_when_under_limit(self, sample_df):
        result = _df_to_markdown(sample_df, max_rows=10)
        assert "exibindo" not in result


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

class TestListAvailableFiles:
    def test_returns_string(self):
        result = list_available_files()
        assert isinstance(result, str)

    def test_includes_csv_filename(self):
        result = list_available_files()
        assert "SampleSuperstore.csv" in result


class TestGetFileSchema:
    def test_returns_string(self):
        result = get_file_schema(FILENAME)
        assert isinstance(result, str)

    def test_contains_column_names(self):
        result = get_file_schema(FILENAME)
        assert "Sales" in result
        assert "Profit" in result
        assert "Region" in result

    def test_contains_row_count(self):
        result = get_file_schema(FILENAME)
        assert "Linhas" in result


class TestGetDataSample:
    def test_returns_string(self):
        result = get_data_sample(FILENAME)
        assert isinstance(result, str)

    def test_respects_n_rows_as_int(self):
        result = get_data_sample(FILENAME, n_rows=3)
        assert isinstance(result, str)

    def test_accepts_n_rows_as_string(self):
        # Simula o comportamento do LLM passando string
        result = get_data_sample(FILENAME, n_rows="3")
        assert isinstance(result, str)


class TestGetStatisticalSummary:
    def test_returns_string(self):
        result = get_statistical_summary(FILENAME)
        assert isinstance(result, str)

    def test_contains_numeric_stats(self):
        result = get_statistical_summary(FILENAME)
        assert "Sales" in result or "Profit" in result


class TestGetUniqueValues:
    def test_returns_string(self):
        result = get_unique_values(FILENAME, "Region")
        assert isinstance(result, str)

    def test_contains_region_values(self):
        result = get_unique_values(FILENAME, "Region")
        assert "West" in result or "East" in result

    def test_invalid_column_returns_error_message(self):
        result = get_unique_values(FILENAME, "ColunaInexistente")
        assert "não encontrada" in result


class TestAggregateData:
    def test_sum_by_region(self):
        result = aggregate_data(FILENAME, "Region", "Sales", "sum")
        assert isinstance(result, str)
        assert "Sales" in result or "sum" in result

    def test_mean_operation(self):
        result = aggregate_data(FILENAME, "Category", "Profit", "mean")
        assert isinstance(result, str)

    def test_invalid_group_by_returns_error(self):
        result = aggregate_data(FILENAME, "ColunaErrada", "Sales")
        assert "não encontrada" in result

    def test_invalid_agg_column_returns_error(self):
        result = aggregate_data(FILENAME, "Region", "ColunaErrada")
        assert "não encontrada" in result

    def test_invalid_operation_returns_error(self):
        result = aggregate_data(FILENAME, "Region", "Sales", "invalid_op")
        assert "inválida" in result


class TestFilterData:
    def test_filter_by_existing_value(self):
        result = filter_data(FILENAME, "Region", "West")
        assert isinstance(result, str)
        assert "encontrada" in result

    def test_filter_case_insensitive(self):
        result_lower = filter_data(FILENAME, "Region", "west")
        result_upper = filter_data(FILENAME, "Region", "West")
        assert "encontrada" in result_lower
        assert "encontrada" in result_upper

    def test_filter_nonexistent_value(self):
        result = filter_data(FILENAME, "Region", "Marte")
        assert "Nenhuma" in result

    def test_invalid_column_returns_error(self):
        result = filter_data(FILENAME, "ColunaErrada", "West")
        assert "não encontrada" in result

    def test_n_rows_as_string(self):
        result = filter_data(FILENAME, "Region", "West", n_rows="5")
        assert isinstance(result, str)


class TestSearchInData:
    def test_partial_search(self):
        result = search_in_data(FILENAME, "Sub-Category", "Chair")
        assert isinstance(result, str)
        assert "encontrada" in result

    def test_case_insensitive_search(self):
        result = search_in_data(FILENAME, "Sub-Category", "chair")
        assert "encontrada" in result

    def test_no_results(self):
        result = search_in_data(FILENAME, "Sub-Category", "xyzzy_nao_existe")
        assert "Nenhum resultado" in result

    def test_invalid_column_returns_error(self):
        result = search_in_data(FILENAME, "ColunaInexistente", "test")
        assert "não encontrada" in result

    def test_n_rows_as_string(self):
        result = search_in_data(FILENAME, "Category", "Tech", n_rows="5")
        assert isinstance(result, str)
