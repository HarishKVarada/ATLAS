from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class MarketBar:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    def __post_init__(self) -> None:
        symbol = self.symbol.strip().upper()
        if not symbol:
            raise ValueError("symbol must not be blank")

        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ValueError("timestamp must be timezone-aware")

        self._validate_prices()

        if self.volume < 0:
            raise ValueError("volume must be zero or greater")

        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "timestamp", self.timestamp.astimezone(UTC))

    def _validate_prices(self) -> None:
        prices = {
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
        }

        for name, price in prices.items():
            if price <= 0:
                raise ValueError(f"{name} must be positive")

        if self.high < max(self.open, self.close, self.low):
            raise ValueError(
                "high must be greater than or equal to open, close, and low"
            )

        if self.low > min(self.open, self.close, self.high):
            raise ValueError("low must be less than or equal to open, close, and high")
