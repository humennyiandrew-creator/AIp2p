# Architecture — P2P Spread Scanner

## Scope (v1)
Read-only scanning across 10 exchange P2P markets → normalized ad data → cross-exchange spread detection (≥1.5%) → NLP hidden-fee extraction → bank-charge-adjusted net profitability → alerting. No auto-execution in v1.

## Components

```
apps/
  connectors/         # one adapter per exchange, common interface
    binance_p2p.py
    bybit_p2p.py
    okx_p2p.py
    bitget_p2p.py
    htx_p2p.py
    gateio_p2p.py
    mexc_p2p.py
    noones_p2p.py
    bitpapa_p2p.py
    localcoinswap_p2p.py
    base.py           # Connector ABC: fetch_ads(asset, fiat, side) -> list[Ad]
  scanner/
    poller.py         # scheduler, per-exchange rate limiting/backoff
    normalizer.py      # maps raw ad -> common Ad schema
    spread_engine.py   # cross-exchange spread computation, ≥1.5% filter
  fee_analysis/
    rule_extractor.py  # regex pass over ad remarks
    llm_extractor.py    # Haiku-tier LLM pass for free-text terms
    bank_charges.py     # curated fee table + lookup
    profitability.py    # net = spread - hidden_fee - bank_charge - withdrawal_fee
  alerting/
    notifier.py         # webhook/telegram/email sink
  storage/
    models.py            # Ad, Opportunity, ExchangeStatus
    db.py                 # Postgres via SQLAlchemy/asyncpg
  config/
    exchanges.yaml         # per-exchange asset/fiat pairs to poll, rate limits
    bank_fees.yaml          # seeded, human-maintained
main.py                      # wires poller -> normalizer -> spread_engine -> fee_analysis -> alerting

MEMORY.md                     # project memory log (replaces Obsidian — decisions, state, TODOs)
docs/
  ANALYSIS.md
  ARCHITECTURE.md
```

## Data flow
1. `poller` hits each connector on its own interval (respecting rate limits) → raw ads.
2. `normalizer` maps to common `Ad{exchange, asset, fiat, side, price, limits, payment_methods, remarks, merchant}`.
3. `spread_engine` computes cross-exchange spreads per (asset, fiat), filters ≥1.5%, produces candidate `Opportunity`.
4. `fee_analysis` runs rule + LLM extraction on both legs' remarks, looks up bank charges, computes net profitability.
5. Opportunities with positive net profit after fees → `alerting`.
6. Everything persisted to Postgres for historical spread analysis and backtesting the whole pipeline.

## Model routing (cost control)
- **Haiku**: fee/remarks text extraction (`llm_extractor.py`) — high volume, low complexity per call.
- **Sonnet**: connector implementation, normalization logic, spread engine, day-to-day coding.
- **Opus 5.5**: architecture decisions, cross-exchange edge cases, anything touching money-math correctness or legal-risk judgment calls.

## Memory (replaces Obsidian)
No Obsidian connector is available in this account. `MEMORY.md` at repo root serves as the persistent memory: decisions made, exchanges added/removed, open questions, current build phase. Updated after each completed milestone instead of re-deriving context from scratch each session.

## Open decisions before scaffolding code
- Language/runtime: Python (async, aiohttp/httpx) recommended — best library support for exchange APIs and NLP tooling.
- Storage: Postgres (durable, queryable) vs. lighter SQLite for v1 prototype.
- Alerting channel: Telegram/webhook/email — none specified yet.
