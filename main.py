from __future__ import annotations

import asyncio
import logging

import yaml
from dotenv import load_dotenv

from apps.alerting.telegram_notifier import TelegramNotifier
from apps.connectors.base import Side
from apps.connectors.binance_p2p import BinanceP2P
from apps.fee_analysis.bank_charges import load_bank_fees
from apps.fee_analysis.profitability import score_opportunity
from apps.scanner.spread_engine import find_spreads
from apps.storage.db import get_connection, save_scored_opportunity

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("aip2p")

# Only Binance is implemented so far; add connectors here as they land.
CONNECTORS = [BinanceP2P()]


async def scan_once(config: dict, notifier: TelegramNotifier, db) -> None:
    bank_fees = load_bank_fees()
    min_spread_pct = config["min_spread_pct"]

    for pair in config["pairs"]:
        asset, fiat = pair["asset"], pair["fiat"]

        buy_ads, sell_ads = [], []
        for connector in CONNECTORS:
            buy_ads += await connector.fetch_ads(asset, fiat, Side.BUY)
            sell_ads += await connector.fetch_ads(asset, fiat, Side.SELL)

        opportunities = find_spreads(buy_ads, sell_ads, min_spread_pct)
        log.info("%s/%s: %d raw opportunities >= %.1f%%", asset, fiat, len(opportunities), min_spread_pct)

        for opp in opportunities:
            scored = score_opportunity(opp, bank_fees)
            save_scored_opportunity(db, scored)
            if scored.net_spread_pct >= min_spread_pct:
                await notifier.send(
                    f"{asset}/{fiat}: buy {scored.opportunity.buy_exchange} @ {scored.opportunity.buy_price} -> "
                    f"sell {scored.opportunity.sell_exchange} @ {scored.opportunity.sell_price}\n"
                    f"gross spread {scored.opportunity.spread_pct:.2f}% | "
                    f"hidden fees {scored.hidden_fee_pct:.2f}% | bank charge {scored.bank_charge_pct:.2f}% | "
                    f"net {scored.net_spread_pct:.2f}%"
                    + (f"\nrestrictions: {', '.join(scored.restrictions)}" if scored.restrictions else "")
                )


async def main() -> None:
    load_dotenv()
    with open("config/exchanges.yaml") as f:
        config = yaml.safe_load(f)

    notifier = TelegramNotifier()
    db = get_connection()
    await scan_once(config, notifier, db)


if __name__ == "__main__":
    asyncio.run(main())
