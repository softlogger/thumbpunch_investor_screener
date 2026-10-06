from app.calculations import distance_from_52_week_low


def test_distance_from_52_week_low() -> None:
    result = distance_from_52_week_low(
        current_price=105.00,
        fifty_two_week_low=100.00,
    )

    assert result == 0.05


def test_distance_from_52_week_low_missing_data() -> None:
    result = distance_from_52_week_low(
        current_price=None,
        fifty_two_week_low=100.00,
    )

    assert result is None


def test_distance_from_52_week_low_invalid_low() -> None:
    result = distance_from_52_week_low(
        current_price=105.00,
        fifty_two_week_low=0,
    )

    assert result is None


def test_ev_to_fcf():
    from app.calculations import ev_to_fcf

    result = ev_to_fcf(
        enterprise_value=43.3,
        free_cash_flow=10.0,
    )

    assert result == 4.33


def test_ev_to_fcf_negative_fcf():
    from app.calculations import ev_to_fcf

    result = ev_to_fcf(
        enterprise_value=43.3,
        free_cash_flow=-10.0,
    )

    assert result is None