from app.screening import ScreeningResult, ScreeningStatus, screen_dividend_yield
from app.screening import OverallStatus, determine_overall_status

def test_screening_result_pass():
    result = ScreeningResult(
        criterion="Debt / Equity",
        actual_value=0.42,
        requirement="< 0.50",
        status=ScreeningStatus.PASS,
        provider="FMP",
        reason="Debt-to-equity is below the selected maximum.",
    )

    assert result.criterion == "Debt / Equity"
    assert result.actual_value == 0.42
    assert result.status == ScreeningStatus.PASS
    assert result.provider == "FMP"


def test_screening_result_data_unavailable():
    result = ScreeningResult(
        criterion="Forward FCF Yield",
        actual_value=None,
        requirement="1% to 75%",
        status=ScreeningStatus.DATA_UNAVAILABLE,
        provider="FMP",
        reason="Forward free cash flow is unavailable.",
    )

    assert result.actual_value is None
    assert result.status == ScreeningStatus.DATA_UNAVAILABLE

from app.screening import screen_distance_from_52_week_low


def test_distance_from_low_pass():
    result = screen_distance_from_52_week_low(
        current_price=105.0,
        fifty_two_week_low=100.0,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.PASS
    assert result.actual_value == 0.05


def test_distance_from_low_fail():
    result = screen_distance_from_52_week_low(
        current_price=120.0,
        fifty_two_week_low=100.0,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.FAIL
    assert result.actual_value == 0.20


def test_distance_from_low_data_unavailable():
    result = screen_distance_from_52_week_low(
        current_price=None,
        fifty_two_week_low=100.0,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.DATA_UNAVAILABLE


from app.screening import screen_ev_to_fcf


def test_ev_to_fcf_pass():
    result = screen_ev_to_fcf(
        enterprise_value=43.3,
        free_cash_flow=10.0,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.PASS
    assert result.actual_value == 4.33


def test_ev_to_fcf_fail():
    result = screen_ev_to_fcf(
        enterprise_value=90.0,
        free_cash_flow=10.0,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.FAIL
    assert result.actual_value == 9.0


def test_ev_to_fcf_negative_fcf_is_unavailable():
    result = screen_ev_to_fcf(
        enterprise_value=43.3,
        free_cash_flow=-10.0,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.DATA_UNAVAILABLE
    assert result.actual_value is None


from app.screening import screen_debt_to_equity


def test_debt_to_equity_pass():
    result = screen_debt_to_equity(
        debt_to_equity=0.42,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.PASS


def test_debt_to_equity_fail():
    result = screen_debt_to_equity(
        debt_to_equity=0.60,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.FAIL


def test_debt_to_equity_unavailable():
    result = screen_debt_to_equity(
        debt_to_equity=None,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.DATA_UNAVAILABLE

from app.screening import screen_dividend_yield


def test_dividend_yield_pass():
    result = screen_dividend_yield(
        dividend_yield=0.025,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.PASS


def test_dividend_yield_fail():
    result = screen_dividend_yield(
        dividend_yield=0.01,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.FAIL


def test_dividend_yield_unavailable():
    result = screen_dividend_yield(
        dividend_yield=None,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.DATA_UNAVAILABLE

from app.screening import screen_forward_fcf_yield


def test_forward_fcf_yield_pass():
    result = screen_forward_fcf_yield(
        forward_free_cash_flow=10.0,
        enterprise_value=100.0,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.PASS
    assert result.actual_value == 0.10


def test_forward_fcf_yield_fail():
    result = screen_forward_fcf_yield(
        forward_free_cash_flow=0.5,
        enterprise_value=100.0,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.FAIL


def test_forward_fcf_yield_unavailable():
    result = screen_forward_fcf_yield(
        forward_free_cash_flow=None,
        enterprise_value=100.0,
        provider="FMP",
    )

    assert result.status == ScreeningStatus.DATA_UNAVAILABLE



def test_overall_status_qualified():
    results = [
        ScreeningResult(
            criterion="Rule 1",
            actual_value=1.0,
            requirement="test",
            status=ScreeningStatus.PASS,
            provider="TEST",
            reason="Passed.",
        ),
        ScreeningResult(
            criterion="Rule 2",
            actual_value=2.0,
            requirement="test",
            status=ScreeningStatus.PASS,
            provider="TEST",
            reason="Passed.",
        ),
    ]

    assert determine_overall_status(results) == OverallStatus.QUALIFIED


def test_overall_status_not_qualified():
    results = [
        ScreeningResult(
            criterion="Rule 1",
            actual_value=1.0,
            requirement="test",
            status=ScreeningStatus.PASS,
            provider="TEST",
            reason="Passed.",
        ),
        ScreeningResult(
            criterion="Rule 2",
            actual_value=2.0,
            requirement="test",
            status=ScreeningStatus.FAIL,
            provider="TEST",
            reason="Failed.",
        ),
    ]

    assert determine_overall_status(results) == OverallStatus.NOT_QUALIFIED


def test_overall_status_incomplete():
    results = [
        ScreeningResult(
            criterion="Rule 1",
            actual_value=1.0,
            requirement="test",
            status=ScreeningStatus.PASS,
            provider="TEST",
            reason="Passed.",
        ),
        ScreeningResult(
            criterion="Rule 2",
            actual_value=None,
            requirement="test",
            status=ScreeningStatus.DATA_UNAVAILABLE,
            provider="TEST",
            reason="Unavailable.",
        ),
    ]

    assert determine_overall_status(results) == OverallStatus.INCOMPLETE

from app.models import FinancialData
from app.screening import screen_stock


def test_screen_stock_qualified():
    data = FinancialData(
        ticker="TEST",
        company_name="Test Company",
        price=105.0,
        enterprise_value=50.0,
        free_cash_flow=10.0,
        debt_to_equity=0.40,
        dividend_yield=0.03,
        fifty_two_week_low=100.0,
        forward_free_cash_flow=8.0,
        provider="TEST",
    )

    results, overall_status = screen_stock(data)

    assert len(results) == 5
    assert overall_status == OverallStatus.QUALIFIED