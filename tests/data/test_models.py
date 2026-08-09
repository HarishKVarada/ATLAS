from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone

import pytest

from atlas.data import MarketBar


def make_bar(**overrides):
    values = {
        "symbol": "AAPL",
        "timestamp": datetime(2026, 8, 9, 14, 30, tzinfo=UTC),
        "open": 100.0,
        "high": 110.0,
        "low": 95.0,
        "close": 105.0,
        "volume": 1_000,
    }
    values.update(overrides)
    return MarketBar(**values)


def test_valid_market_bar_creation():
    bar = make_bar()

    assert bar.symbol == "AAPL"
    assert bar.open == 100.0
    assert bar.high == 110.0
    assert bar.low == 95.0
    assert bar.close == 105.0
    assert bar.volume == 1_000


def test_market_bar_is_immutable():
    bar = make_bar()

    with pytest.raises(FrozenInstanceError):
        bar.close = 106.0


def test_symbol_normalizes_to_uppercase():
    bar = make_bar(symbol=" msft ")

    assert bar.symbol == "MSFT"


def test_timestamp_normalizes_to_utc():
    eastern = timezone(timedelta(hours=-4))
    bar = make_bar(timestamp=datetime(2026, 8, 9, 10, 30, tzinfo=eastern))

    assert bar.timestamp == datetime(2026, 8, 9, 14, 30, tzinfo=UTC)


def test_blank_symbol_rejected():
    with pytest.raises(ValueError, match="symbol"):
        make_bar(symbol="   ")


def test_naive_timestamp_rejected():
    with pytest.raises(ValueError, match="timestamp"):
        make_bar(timestamp=datetime(2026, 8, 9, 14, 30))


@pytest.mark.parametrize("field", ["open", "high", "low", "close"])
@pytest.mark.parametrize("value", [0.0, -1.0])
def test_non_positive_prices_rejected(field, value):
    with pytest.raises(ValueError, match=field):
        make_bar(**{field: value})


def test_negative_volume_rejected():
    with pytest.raises(ValueError, match="volume"):
        make_bar(volume=-1)


def test_invalid_high_rejected():
    with pytest.raises(ValueError, match="high"):
        make_bar(high=99.0)


def test_invalid_low_rejected():
    with pytest.raises(ValueError, match="low"):
        make_bar(low=106.0)


def test_zero_volume_accepted():
    bar = make_bar(volume=0)

    assert bar.volume == 0
