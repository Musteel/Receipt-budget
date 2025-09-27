import pytest
from app.parser import parse_receipt_text

dummy_text = """
Coffee Shop Receipt
Latte        3.50
Bread        2.00
Banana       1.20
Netflix      12.99
Total:      19.69
"""

def test_parser_excludes_total():
    items = parse_receipt_text(dummy_text)
    # Should parse 4 real items, not 5
    assert len(items) == 4

def test_item_descriptions_and_prices():
    items = parse_receipt_text(dummy_text)
    expected = {
        "Latte": 3.50,
        "Bread": 2.00,
        "Banana": 1.20,
        "Netflix": 12.99,
    }
    for it in items:
        desc = it["desc"]
        price = it["price"]
        assert desc in expected
        assert abs(price - expected[desc]) < 1e-6