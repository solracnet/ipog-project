"""
Fixtures compartilhadas entre todos os testes.
"""

import pytest
import pandas as pd

FILENAME = "SampleSuperstore.csv"

@pytest.fixture
def sample_df():
    """DataFrame mínimo com a estrutura do SampleSuperstore para testes unitários."""
    return pd.DataFrame({
        "Ship Mode":    ["Second Class", "First Class", "Standard Class", "Same Day"],
        "Segment":      ["Consumer", "Corporate", "Home Office", "Consumer"],
        "Country":      ["United States"] * 4,
        "City":         ["New York", "Los Angeles", "Chicago", "Houston"],
        "State":        ["New York", "California", "Illinois", "Texas"],
        "Postal Code":  [10001, 90001, 60601, 77001],
        "Region":       ["East", "West", "Central", "South"],
        "Category":     ["Furniture", "Technology", "Office Supplies", "Technology"],
        "Sub-Category": ["Chairs", "Phones", "Paper", "Accessories"],
        "Sales":        [500.0, 1200.0, 80.0, 300.0],
        "Quantity":     [2, 3, 5, 1],
        "Discount":     [0.0, 0.2, 0.0, 0.1],
        "Profit":       [100.0, -50.0, 20.0, 60.0],
    })
