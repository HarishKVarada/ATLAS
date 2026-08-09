from abc import ABC, abstractmethod
from datetime import datetime

from atlas.data.models import MarketBar


class MarketDataProvider(ABC):
    @abstractmethod
    def get_bars(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> list[MarketBar]:
        raise NotImplementedError
