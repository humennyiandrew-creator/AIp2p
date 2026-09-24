from __future__ import annotations

from pathlib import Path

import yaml

DEFAULT_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "bank_fees.yaml"


def load_bank_fees(path: Path = DEFAULT_PATH) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def get_bank_charge_pct(country: str, method: str, table: dict) -> float:
    country_table = table.get(country, {})
    if method in country_table:
        return country_table[method]
    return table.get("default", {}).get(method, 0.0)
