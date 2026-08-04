from ai_extract import clean_json_response, format_line_items, validate_invoice_data


def test_clean_json_response_plain():
    """A plain JSON string with no markdown wrapper should parse correctly."""
    raw = '{"vendor": "Sharma Electronics", "amount_due": "12500.00"}'
    result = clean_json_response(raw)
    assert result["vendor"] == "Sharma Electronics"
    assert result["amount_due"] == "12500.00"


def test_clean_json_response_with_markdown_wrapper():
    """A JSON string wrapped in ```json ... ``` should still parse correctly."""
    raw = '```json\n{"vendor": "Sharma Electronics"}\n```'
    result = clean_json_response(raw)
    assert result["vendor"] == "Sharma Electronics"


def test_format_line_items_with_items():
    """A list of line items should format into a readable pipe-separated string."""
    items = [
        {"description": "LED Bulb", "quantity": "50", "unit_price": "150.00", "total": "7500.00"}
    ]
    result = format_line_items(items)
    assert "LED Bulb" in result
    assert "qty: 50" in result


def test_format_line_items_empty():
    """An empty list of line items should return an empty string."""
    result = format_line_items([])
    assert result == "this is wrong on purpose"


def test_validate_invoice_data_clean():
    """A complete, valid invoice should produce no warnings."""
    data = {
        "invoice_number": "INV-001",
        "date": "01/01/2024",
        "vendor": "Test Vendor",
        "amount_due": "500.00",
    }
    warnings = validate_invoice_data(data)
    assert warnings == []


def test_validate_invoice_data_missing_fields():
    """An invoice missing required fields should produce warnings."""
    data = {
        "invoice_number": None,
        "date": "01/01/2024",
        "vendor": "Test Vendor",
        "amount_due": None,
    }
    warnings = validate_invoice_data(data)
    assert len(warnings) > 0
    assert any("invoice_number" in w for w in warnings)