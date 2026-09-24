from __future__ import annotations

from dataclasses import dataclass

from apps.connectors.base import Ad


@dataclass
class Opportunity:
    asset: str
    fiat: str
    buy_exchange: str
    sell_exchange: str
    buy_price: float
    sell_price: float
    spread_pct: float
    buy_ad: Ad
    sell_ad: Ad


def find_spreads(buy_ads: list[Ad], sell_ads: list[Ad], min_spread_pct: float = 1.5) -> list[Opportunity]:
    """Cross-exchange only: buying on one exchange and selling on another."""
    opportunities: list[Opportunity] = []
    for buy_ad in buy_ads:
        for sell_ad in sell_ads:
            if buy_ad.exchange == sell_ad.exchange:
                continue
            spread_pct = (sell_ad.price - buy_ad.price) / buy_ad.price * 100
            if spread_pct >= min_spread_pct:
                opportunities.append(
                    Opportunity(
                        asset=buy_ad.asset,
                        fiat=buy_ad.fiat,
                        buy_exchange=buy_ad.exchange,
                        sell_exchange=sell_ad.exchange,
                        buy_price=buy_ad.price,
                        sell_price=sell_ad.price,
                        spread_pct=spread_pct,
                        buy_ad=buy_ad,
                        sell_ad=sell_ad,
                    )
                )
    return sorted(opportunities, key=lambda o: o.spread_pct, reverse=True)
