from datetime import UTC, datetime, timedelta, timezone

import pytest

from atlas.data import MarketBar
from atlas.data.providers.yfinance_provider import (
    TIMEFRAME_TO_YFINANCE_INTERVAL,
    YFinanceMarketDataProvider,
)


class FakeFrame:
    def __init__(self, rows):
        self._rows = rows
        self.empty = not rows

    def iterrows(self):
        return iter(self._rows)


class FakeTimestamp:
    def __init__(self, value):
        self._value = value

    def to_pydatetime(self):
        return self._value


def install_fake_download(monkeypatch, frame):
    calls = []

    def fake_download(**kwargs):
        calls.append(kwargs)
        return frame

    monkeypatch.setattr(
        "atlas.data.providers.yfinance_provider.yf.download",
        fake_download,
    )
    return calls


def make_frame():
    eastern = timezone(timedelta(hours=-4))
    return FakeFrame(
        [
            (
                FakeTimestamp(datetime(2026, 8, 8, 10, 30, tzinfo=eastern)),
                {
                    "Open": 100.0,
                    "High": 110.0,
                    "Low": 95.0,
                    "Close": 105.0,
                    "Volume": 1_000,
                },
            )
        ]
    )


def test_valid_provider_response_becomes_market_bars(monkeypatch):
    install_fake_download(monkeypatch, make_frame())

    bars = YFinanceMarketDataProvider().get_bars(
        symbol="SPY",
        timeframe="1d",
        start=datetime(2026, 8, 8, tzinfo=UTC),
        end=datetime(2026, 8, 9, tzinfo=UTC),
    )

    assert bars == [
        MarketBar(
            symbol="SPY",
            timestamp=datetime(2026, 8, 8, 14, 30, tzinfo=UTC),
            open=100.0,
            high=110.0,
            low=95.0,
            close=105.0,
            volume=1_000,
        )
    ]


def test_symbol_normalization(monkeypatch):
    install_fake_download(monkeypatch, make_frame())

    bars = YFinanceMarketDataProvider().get_bars(
        symbol=" spy ",
        timeframe="1d",
        start=datetime(2026, 8, 8, tzinfo=UTC),
        end=datetime(2026, 8, 9, tzinfo=UTC),
    )

    assert bars[0].symbol == "SPY"


def test_timestamp_normalization_to_utc(monkeypatch):
    install_fake_download(monkeypatch, make_frame())

    bars = YFinanceMarketDataProvider().get_bars(
        symbol="SPY",
        timeframe="1d",
        start=datetime(2026, 8, 8, tzinfo=UTC),
        end=datetime(2026, 8, 9, tzinfo=UTC),
    )

    assert bars[0].timestamp.tzinfo == UTC
    assert bars[0].timestamp == datetime(2026, 8, 8, 14, 30, tzinfo=UTC)


def test_timeframe_mapping(monkeypatch):
    calls = install_fake_download(monkeypatch, make_frame())

    YFinanceMarketDataProvider().get_bars(
        symbol="SPY",
        timeframe="15m",
        start=datetime(2026, 8, 8, tzinfo=UTC),
        end=datetime(2026, 8, 9, tzinfo=UTC),
    )

    assert calls[0]["interval"] == TIMEFRAME_TO_YFINANCE_INTERVAL["15m"]


def test_unsupported_timeframe_rejected(monkeypatch):
    install_fake_download(monkeypatch, make_frame())

    with pytest.raises(ValueError, match="unsupported timeframe"):
        YFinanceMarketDataProvider().get_bars(
            symbol="SPY",
            timeframe="2d",
            start=datetime(2026, 8, 8, tzinfo=UTC),
            end=datetime(2026, 8, 9, tzinfo=UTC),
        )


def test_empty_provider_response_returns_empty_list(monkeypatch):
    install_fake_download(monkeypatch, FakeFrame([]))

    bars = YFinanceMarketDataProvider().get_bars(
        symbol="SPY",
        timeframe="1d",
        start=datetime(2026, 8, 8, tzinfo=UTC),
        end=datetime(2026, 8, 9, tzinfo=UTC),
    )

    assert bars == []


def test_provider_specific_structure_does_not_leak(monkeypatch):
    install_fake_download(monkeypatch, make_frame())

    bars = YFinanceMarketDataProvider().get_bars(
        symbol="SPY",
        timeframe="1d",
        start=datetime(2026, 8, 8, tzinfo=UTC),
        end=datetime(2026, 8, 9, tzinfo=UTC),
    )

    assert isinstance(bars, list)
    assert all(isinstance(bar, MarketBar) for bar in bars)
    assert not isinstance(bars, FakeFrame)


def test_invalid_provider_data_is_rejected_by_market_bar(monkeypatch):
    frame = FakeFrame(
        [
            (
                datetime(2026, 8, 8, 14, 30, tzinfo=UTC),
                {
                    "Open": 100.0,
                    "High": 99.0,
                    "Low": 95.0,
                    "Close": 105.0,
                    "Volume": 1_000,
                },
            )
        ]
    )
    install_fake_download(monkeypatch, frame)

    with pytest.raises(ValueError, match="high"):
        YFinanceMarketDataProvider().get_bars(
            symbol="SPY",
            timeframe="1d",
            start=datetime(2026, 8, 8, tzinfo=UTC),
            end=datetime(2026, 8, 9, tzinfo=UTC),
        )
