from __future__ import annotations

import re

FEE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*(fee|charge|extra)", re.IGNORECASE)
RESTRICTION_KEYWORDS = ("no memo", "verified only", "no third party", "must be verified", "no vpn")


def extract_fee_hints(remarks: str) -> dict:
    """Regex pass over free-text ad remarks. Catches explicit %-fee mentions and
    common restriction phrases. Ambiguous/long-tail phrasing needs an LLM pass
    (see docs/ARCHITECTURE.md — llm_extractor, routed to Haiku)."""
    if not remarks:
        return {"extra_fee_pct": 0.0, "restrictions": []}

    match = FEE_PATTERN.search(remarks)
    extra_fee_pct = float(match.group(1)) if match else 0.0

    lowered = remarks.lower()
    restrictions = [kw for kw in RESTRICTION_KEYWORDS if kw in lowered]

    return {"extra_fee_pct": extra_fee_pct, "restrictions": restrictions}
