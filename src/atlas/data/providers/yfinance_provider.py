from datetime import UTC, datetime
from typing import Any

import yfinance as yf

from atlas.data import MarketBar, MarketDataProvider

TIMEFRAME_TO_YFINANCE_INTERVAL = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "1d": "1d",
}


class YFinanceMarketDataProvider(MarketDataProvider):
    def get_bars(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> list[MarketBar]:
        interval = self._get_interval(timeframe)

        try:
            data = yf.download(
                tickers=symbol,
                start=start,
                end=end,
                interval=interval,
                progress=False,
                auto_adjust=False,
                actions=False,
                multi_level_index=False,
            )
        except Exception as exc:
            raise RuntimeError("failed to retrieve yfinance market data") from exc

        if data is None:
            raise RuntimeError("yfinance returned no response")

        if getattr(data, "empty", False):
            return []

        return [
            self._row_to_market_bar(symbol, timestamp, row)
            for timestamp, row in data.iterrows()
        ]

    def _get_interval(self, timeframe: str) -> str:
        try:
            return TIMEFRAME_TO_YFINANCE_INTERVAL[timeframe]
        except KeyError as exc:
            raise ValueError(f"unsupported timeframe: {timeframe}") from exc

    def _row_to_market_bar(
        self,
        symbol: str,
        timestamp: Any,
        row: Any,
    ) -> MarketBar:
        return MarketBar(
            symbol=symbol,
            timestamp=self._to_utc_datetime(timestamp),
            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),
            volume=int(row["Volume"]),
        )

    def _to_utc_datetime(self, value: Any) -> datetime:
        timestamp = value.to_pydatetime() if hasattr(value, "to_pydatetime") else value

        if not isinstance(timestamp, datetime):
            raise ValueError("provider timestamp must be a datetime")

        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            timestamp = timestamp.replace(tzinfo=UTC)

        return timestamp.astimezone(UTC)
