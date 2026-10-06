from dataclasses import dataclass
from typing import Optional


@dataclass
class FinancialData:
    ticker: str
    company_name: Optional[str] = None

    price: Optional[float] = None
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    free_cash_flow: Optional[float] = None

    debt_to_equity: Optional[float] = None
    dividend_yield: Optional[float] = None

    fifty_two_week_low: Optional[float] = None

    forward_free_cash_flow: Optional[float] = None

    provider: Optional[str] = None