from __future__ import annotations

from dataclasses import dataclass

from apps.scanner.spread_engine import Opportunity

from .bank_charges import get_bank_charge_pct
from .rule_extractor import extract_fee_hints


@dataclass
class ScoredOpportunity:
    opportunity: Opportunity
    hidden_fee_pct: float
    bank_charge_pct: float
    net_spread_pct: float
    restrictions: list[str]


def score_opportunity(opp: Opportunity, bank_fee_table: dict, country: str = "default") -> ScoredOpportunity:
    buy_hints = extract_fee_hints(opp.buy_ad.remarks)
    sell_hints = extract_fee_hints(opp.sell_ad.remarks)
    hidden_fee_pct = buy_hints["extra_fee_pct"] + sell_hints["extra_fee_pct"]

    method = opp.buy_ad.payment_methods[0] if opp.buy_ad.payment_methods else "bank_transfer"
    bank_charge_pct = get_bank_charge_pct(country, method, bank_fee_table)

    net_spread_pct = opp.spread_pct - hidden_fee_pct - bank_charge_pct

    return ScoredOpportunity(
        opportunity=opp,
        hidden_fee_pct=hidden_fee_pct,
        bank_charge_pct=bank_charge_pct,
        net_spread_pct=net_spread_pct,
        restrictions=buy_hints["restrictions"] + sell_hints["restrictions"],
    )
