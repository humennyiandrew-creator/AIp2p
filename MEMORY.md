# Project Memory

Persistent memory log for this project (replaces Obsidian — no Obsidian connector available in this account). Updated after each completed milestone.

## Decisions
- 2026-09-24: No Obsidian connector available. User chose repo files as memory store instead.
- 2026-09-24: Scope defined as read-only P2P spread scanner + fee-aware profitability calc, v1. Auto-execution deferred (legal/regulatory risk — P2P trade execution requires KYC'd accounts per exchange and crosses into money-transmission territory).
- 2026-09-24: Target exchanges for v1 (10): Binance, Bybit, OKX, Bitget, HTX, Gate.io, MEXC, Noones, Bitpapa, LocalCoinSwap. All have scannable public P2P ad data without account auth.
- 2026-09-24: Model routing plan — Haiku for high-volume NLP fee extraction, Sonnet for general implementation, Opus 5.5 for architecture/financial-correctness/legal-risk calls.

## Open questions (need user input)
- Language/runtime for implementation: Python assumed but not confirmed.
- Storage: Postgres vs SQLite for v1.
- Alerting channel: Telegram / webhook / email — not specified.
- Confirm final exchange list (KuCoin/Paxful excluded — see docs/ANALYSIS.md).

## Status
- [x] Feasibility analysis (docs/ANALYSIS.md)
- [x] Architecture mapped (docs/ARCHITECTURE.md)
- [ ] Tech stack confirmed
- [ ] Scaffolding started
