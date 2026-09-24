from __future__ import annotations

import httpx

from .base import Ad, Connector, Side


class BybitP2P(Connector):
    """Uses Bybit's public (undocumented) P2P order-book endpoint. No auth required.

    Field names are based on community reverse-engineering, not an official spec —
    verify against a live response before relying on this for real money decisions
    (network to api2.bybit.com is currently blocked in this dev environment, so this
    has not been exercised against live data).
    """

    name = "bybit"
    URL = "https://api2.bybit.com/fiat/otc/item/online"

    async def fetch_ads(self, asset: str, fiat: str, side: Side, rows: int = 20) -> list[Ad]:
        # Bybit's "side" is from the merchant's perspective: 0 = merchant buying, 1 = merchant selling.
        # A user wanting to BUY crypto needs ads where merchants are SELLING -> side "1".
        merchant_side = "1" if side == Side.BUY else "0"
        payload = {
            "userId": "",
            "tokenId": asset,
            "currencyId": fiat,
            "payment": [],
            "side": merchant_side,
            "size": str(rows),
            "page": "1",
            "amount": "",
            "authMaker": False,
            "canTrade": False,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(self.URL, json=payload)
            resp.raise_for_status()
            data = resp.json()

        ads: list[Ad] = []
        for item in data.get("result", {}).get("items", []):
            ads.append(
                Ad(
                    exchange=self.name,
                    asset=asset,
                    fiat=fiat,
                    side=side,
                    price=float(item["price"]),
                    min_limit=float(item["minAmount"]),
                    max_limit=float(item["maxAmount"]),
                    payment_methods=[p.get("paymentType", "") for p in item.get("payments", [])],
                    remarks=item.get("remark") or "",
                    merchant_name=item.get("nickName", ""),
                    merchant_verified=bool(item.get("authTag") or item.get("isOnline")),
                )
            )
        return ads
