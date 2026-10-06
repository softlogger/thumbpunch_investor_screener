from typing import Optional



def distance_from_52_week_low(
    current_price: Optional[float],
    fifty_two_week_low: Optional[float],
) -> Optional[float]:
    if current_price is None or fifty_two_week_low is None:
        return None

    if fifty_two_week_low <= 0:
        return None

    return (current_price - fifty_two_week_low) / fifty_two_week_low

def ev_to_fcf(
    enterprise_value: Optional[float],
    free_cash_flow: Optional[float],
) -> Optional[float]:
    if enterprise_value is None or free_cash_flow is None:
        return None

    if free_cash_flow <= 0:
        return None

    return enterprise_value / free_cash_flow


def forward_fcf_yield(
    forward_free_cash_flow: Optional[float],
    enterprise_value: Optional[float],
) -> Optional[float]:
    if forward_free_cash_flow is None or enterprise_value is None:
        return None

    if forward_free_cash_flow <= 0 or enterprise_value <= 0:
        return None

    return forward_free_cash_flow / enterprise_value
