from app.models import FinancialData


def test_financial_data_model() -> None:
    data = FinancialData(
        ticker="CVX",
        company_name="Chevron",
        price=150.00,
        provider="TEST",
    )

    assert data.ticker == "CVX"
    assert data.company_name == "Chevron"
    assert data.price == 150.00
    assert data.provider == "TEST"