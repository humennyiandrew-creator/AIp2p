from __future__ import annotations

import sqlite3
from pathlib import Path

from apps.fee_analysis.profitability import ScoredOpportunity

DB_PATH = Path(__file__).resolve().parent.parent.parent / "aip2p.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset TEXT, fiat TEXT,
    buy_exchange TEXT, sell_exchange TEXT,
    buy_price REAL, sell_price REAL,
    spread_pct REAL, net_spread_pct REAL,
    hidden_fee_pct REAL, bank_charge_pct REAL,
    found_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def get_connection(path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    return conn


def save_scored_opportunity(conn: sqlite3.Connection, scored: ScoredOpportunity) -> None:
    opp = scored.opportunity
    conn.execute(
        """INSERT INTO opportunities
           (asset, fiat, buy_exchange, sell_exchange, buy_price, sell_price,
            spread_pct, net_spread_pct, hidden_fee_pct, bank_charge_pct)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (
            opp.asset,
            opp.fiat,
            opp.buy_exchange,
            opp.sell_exchange,
            opp.buy_price,
            opp.sell_price,
            opp.spread_pct,
            scored.net_spread_pct,
            scored.hidden_fee_pct,
            scored.bank_charge_pct,
        ),
    )
    conn.commit()
