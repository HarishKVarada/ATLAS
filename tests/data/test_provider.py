from datetime import UTC, datetime

import pytest

from atlas.data import MarketBar, MarketDataProvider


def test_market_data_provider_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        MarketDataProvider()


def test_fake_provider_returns_market_bars():
    class FakeProvider(MarketDataProvider):
        def get_bars(
            self,
            symbol: str,
            timeframe: str,
            start: datetime,
            end: datetime,
        ) -> list[MarketBar]:
            return [
                MarketBar(
                    symbol=symbol,
                    timestamp=start,
                    open=100.0,
                    high=110.0,
                    low=95.0,
                    close=105.0,
                    volume=1_000,
                )
            ]

    provider = FakeProvider()
    bars = provider.get_bars(
        symbol="aapl",
        timeframe="1d",
        start=datetime(2026, 8, 9, 14, 30, tzinfo=UTC),
        end=datetime(2026, 8, 10, 14, 30, tzinfo=UTC),
    )

    assert isinstance(bars, list)
    assert bars == [
        MarketBar(
            symbol="AAPL",
            timestamp=datetime(2026, 8, 9, 14, 30, tzinfo=UTC),
            open=100.0,
            high=110.0,
            low=95.0,
            close=105.0,
            volume=1_000,
        )
    ]
