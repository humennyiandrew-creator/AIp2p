from __future__ import annotations

import time

import httpx

from .base import Ad, Connector, Side


class OkxP2P(Connector):
    """Uses OKX's public (undocumented) C2C order-book endpoint. No auth required.

    Field names are based on community reverse-engineering, not an official spec —
    verify against a live response before relying on this for real money decisions
    (network to okx.com is currently blocked in this dev environment, so this has
    not been exercised against live data).
    """

    name = "okx"
    URL = "https://www.okx.com/v3/c2c/tradingOrders/books"

    async def fetch_ads(self, asset: str, fiat: str, side: Side, rows: int = 20) -> list[Ad]:
        params = {
            "t": str(int(time.time() * 1000)),
            "quoteCurrency": fiat.lower(),
            "baseCurrency": asset.lower(),
            "side": side.value,  # OKX exposes this directly from the taker's perspective
            "paymentMethod": "all",
            "userType": "all",
            "showTrade": "false",
            "showFollow": "false",
            "showAlreadyTraded": "false",
            "isAbleFilterMerchantBlock": "false",
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(self.URL, params=params)
            resp.raise_for_status()
            data = resp.json()

        items = data.get("data", {}).get(side.value, []) or []
        ads: list[Ad] = []
        for item in items[:rows]:
            ads.append(
                Ad(
                    exchange=self.name,
                    asset=asset,
                    fiat=fiat,
                    side=side,
                    price=float(item["price"]),
                    min_limit=float(item["minAmount"]),
                    max_limit=float(item["maxAmount"]),
                    payment_methods=[p.get("paymentMethod", "") for p in item.get("paymentMethods", [])],
                    remarks=item.get("remarks") or item.get("remark") or "",
                    merchant_name=item.get("nickName", ""),
                    merchant_verified=bool(item.get("merchantId")),
                )
            )
        return ads
