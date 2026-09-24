from __future__ import annotations

import httpx

from .base import Ad, Connector, Side


class BinanceP2P(Connector):
    """Uses Binance's public (undocumented) P2P ad-search endpoint. No auth required."""

    name = "binance"
    URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    async def fetch_ads(self, asset: str, fiat: str, side: Side, rows: int = 20) -> list[Ad]:
        trade_type = "BUY" if side == Side.BUY else "SELL"
        payload = {
            "asset": asset,
            "fiat": fiat,
            "tradeType": trade_type,
            "page": 1,
            "rows": rows,
            "payTypes": [],
            "publisherType": None,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(self.URL, json=payload)
            resp.raise_for_status()
            data = resp.json()

        ads: list[Ad] = []
        for item in data.get("data", []):
            adv = item["adv"]
            advertiser = item["advertiser"]
            ads.append(
                Ad(
                    exchange=self.name,
                    asset=asset,
                    fiat=fiat,
                    side=side,
                    price=float(adv["price"]),
                    min_limit=float(adv["minSingleTransAmount"]),
                    max_limit=float(adv["maxSingleTransAmount"]),
                    payment_methods=[m.get("tradeMethodName", "") for m in adv.get("tradeMethods", [])],
                    remarks=adv.get("remarks") or "",
                    merchant_name=advertiser.get("nickName", ""),
                    merchant_verified=advertiser.get("userType") == "merchant",
                )
            )
        return ads
