from dataclasses import dataclass
from enum import Enum
from typing import Optional
from app.calculations import distance_from_52_week_low, ev_to_fcf, forward_fcf_yield
from app.models import FinancialData


class ScreeningStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    DATA_UNAVAILABLE = "DATA UNAVAILABLE"


@dataclass
class ScreeningResult:
    criterion: str
    actual_value: Optional[float]
    requirement: str
    status: ScreeningStatus
    provider: Optional[str]
    reason: str

def screen_distance_from_52_week_low(
    current_price: Optional[float],
    fifty_two_week_low: Optional[float],
    max_distance: float = 0.10,
    provider: Optional[str] = None,
) -> ScreeningResult:
    distance = distance_from_52_week_low(
        current_price=current_price,
        fifty_two_week_low=fifty_two_week_low,
    )

    if distance is None:
        return ScreeningResult(
            criterion="Distance From 52-Week Low",
            actual_value=None,
            requirement=f"<= {max_distance:.0%}",
            status=ScreeningStatus.DATA_UNAVAILABLE,
            provider=provider,
            reason="Current price or 52-week low is unavailable or invalid.",
        )

    if distance <= max_distance:
        return ScreeningResult(
            criterion="Distance From 52-Week Low",
            actual_value=distance,
            requirement=f"<= {max_distance:.0%}",
            status=ScreeningStatus.PASS,
            provider=provider,
            reason="The stock is within the selected maximum distance from its 52-week low.",
        )

    return ScreeningResult(
        criterion="Distance From 52-Week Low",
        actual_value=distance,
        requirement=f"<= {max_distance:.0%}",
        status=ScreeningStatus.FAIL,
        provider=provider,
        reason="The stock is too far above its 52-week low.",
    )

def screen_ev_to_fcf(
    enterprise_value: Optional[float],
    free_cash_flow: Optional[float],
    minimum: float = 1.0,
    maximum: float = 8.0,
    provider: Optional[str] = None,
) -> ScreeningResult:
    ratio = ev_to_fcf(
        enterprise_value=enterprise_value,
        free_cash_flow=free_cash_flow,
    )

    if ratio is None:
        return ScreeningResult(
            criterion="EV / FCF",
            actual_value=None,
            requirement=f"{minimum:.1f}x to {maximum:.1f}x",
            status=ScreeningStatus.DATA_UNAVAILABLE,
            provider=provider,
            reason="Enterprise value or positive free cash flow is unavailable.",
        )

    if minimum <= ratio <= maximum:
        return ScreeningResult(
            criterion="EV / FCF",
            actual_value=ratio,
            requirement=f"{minimum:.1f}x to {maximum:.1f}x",
            status=ScreeningStatus.PASS,
            provider=provider,
            reason="EV/FCF is within the selected acceptable range.",
        )

    return ScreeningResult(
        criterion="EV / FCF",
        actual_value=ratio,
        requirement=f"{minimum:.1f}x to {maximum:.1f}x",
        status=ScreeningStatus.FAIL,
        provider=provider,
        reason="EV/FCF is outside the selected acceptable range.",
    )

def screen_debt_to_equity(
    debt_to_equity: Optional[float],
    maximum: float = 0.50,
    provider: Optional[str] = None,
) -> ScreeningResult:
    if debt_to_equity is None:
        return ScreeningResult(
            criterion="Debt / Equity",
            actual_value=None,
            requirement=f"< {maximum:.2f}",
            status=ScreeningStatus.DATA_UNAVAILABLE,
            provider=provider,
            reason="Debt-to-equity data is unavailable.",
        )

    if debt_to_equity < maximum:
        return ScreeningResult(
            criterion="Debt / Equity",
            actual_value=debt_to_equity,
            requirement=f"< {maximum:.2f}",
            status=ScreeningStatus.PASS,
            provider=provider,
            reason="Debt-to-equity is below the selected maximum.",
        )

    return ScreeningResult(
        criterion="Debt / Equity",
        actual_value=debt_to_equity,
        requirement=f"< {maximum:.2f}",
        status=ScreeningStatus.FAIL,
        provider=provider,
        reason="Debt-to-equity is at or above the selected maximum.",
    )

def screen_dividend_yield(
    dividend_yield: Optional[float],
    minimum: float = 0.02,
    provider: Optional[str] = None,
) -> ScreeningResult:
    if dividend_yield is None:
        return ScreeningResult(
            criterion="Dividend Yield",
            actual_value=None,
            requirement=f">= {minimum:.1%}",
            status=ScreeningStatus.DATA_UNAVAILABLE,
            provider=provider,
            reason="Dividend yield data is unavailable.",
        )

    if dividend_yield >= minimum:
        return ScreeningResult(
            criterion="Dividend Yield",
            actual_value=dividend_yield,
            requirement=f">= {minimum:.1%}",
            status=ScreeningStatus.PASS,
            provider=provider,
            reason="Dividend yield meets or exceeds the selected minimum.",
        )

    return ScreeningResult(
        criterion="Dividend Yield",
        actual_value=dividend_yield,
        requirement=f">= {minimum:.1%}",
        status=ScreeningStatus.FAIL,
        provider=provider,
        reason="Dividend yield is below the selected minimum.",
    )

def screen_forward_fcf_yield(
    forward_free_cash_flow: Optional[float],
    enterprise_value: Optional[float],
    minimum: float = 0.01,
    maximum: float = 0.75,
    provider: Optional[str] = None,
) -> ScreeningResult:
    value = forward_fcf_yield(
        forward_free_cash_flow=forward_free_cash_flow,
        enterprise_value=enterprise_value,
    )

    if value is None:
        return ScreeningResult(
            criterion="Forward FCF Yield",
            actual_value=None,
            requirement=f"{minimum:.1%} to {maximum:.1%}",
            status=ScreeningStatus.DATA_UNAVAILABLE,
            provider=provider,
            reason="Reliable forward free cash flow or enterprise value is unavailable.",
        )

    if minimum <= value <= maximum:
        return ScreeningResult(
            criterion="Forward FCF Yield",
            actual_value=value,
            requirement=f"{minimum:.1%} to {maximum:.1%}",
            status=ScreeningStatus.PASS,
            provider=provider,
            reason="Forward FCF yield is within the selected acceptable range.",
        )

    return ScreeningResult(
        criterion="Forward FCF Yield",
        actual_value=value,
        requirement=f"{minimum:.1%} to {maximum:.1%}",
        status=ScreeningStatus.FAIL,
        provider=provider,
        reason="Forward FCF yield is outside the selected acceptable range.",
    )

class OverallStatus(str, Enum):
    QUALIFIED = "QUALIFIED"
    NOT_QUALIFIED = "NOT QUALIFIED"
    INCOMPLETE = "INCOMPLETE"


def determine_overall_status(
    results: list[ScreeningResult],
) -> OverallStatus:
    if any(result.status == ScreeningStatus.FAIL for result in results):
        return OverallStatus.NOT_QUALIFIED

    if any(
        result.status == ScreeningStatus.DATA_UNAVAILABLE
        for result in results
    ):
        return OverallStatus.INCOMPLETE

    return OverallStatus.QUALIFIED


def screen_stock(
    data: FinancialData,
) -> tuple[list[ScreeningResult], OverallStatus]:
    results = [
        screen_ev_to_fcf(
            enterprise_value=data.enterprise_value,
            free_cash_flow=data.free_cash_flow,
            provider=data.provider,
        ),
        screen_debt_to_equity(
            debt_to_equity=data.debt_to_equity,
            provider=data.provider,
        ),
        screen_dividend_yield(
            dividend_yield=data.dividend_yield,
            provider=data.provider,
        ),
        screen_distance_from_52_week_low(
            current_price=data.price,
            fifty_two_week_low=data.fifty_two_week_low,
            provider=data.provider,
        ),
        screen_forward_fcf_yield(
            forward_free_cash_flow=data.forward_free_cash_flow,
            enterprise_value=data.enterprise_value,
            provider=data.provider,
        ),
    ]

    overall_status = determine_overall_status(results)

    return results, overall_status