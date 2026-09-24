from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass
class Ad:
    exchange: str
    asset: str
    fiat: str
    side: Side
    price: float
    min_limit: float
    max_limit: float
    payment_methods: list[str]
    remarks: str
    merchant_name: str
    merchant_verified: bool = False


class Connector:
    """Common interface every exchange adapter implements."""

    name: str = "base"

    async def fetch_ads(self, asset: str, fiat: str, side: Side, rows: int = 20) -> list[Ad]:
        raise NotImplementedError
