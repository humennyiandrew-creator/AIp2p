# Project Memory

Persistent memory log for this project (replaces Obsidian — no Obsidian connector available in this account). Updated after each completed milestone.

## Decisions
- 2026-09-24: No Obsidian connector available. User chose repo files as memory store instead.
- 2026-09-24: Scope defined as read-only P2P spread scanner + fee-aware profitability calc, v1. Auto-execution deferred (legal/regulatory risk — P2P trade execution requires KYC'd accounts per exchange and crosses into money-transmission territory).
- 2026-09-24: Target exchanges for v1 (10): Binance, Bybit, OKX, Bitget, HTX, Gate.io, MEXC, Noones, Bitpapa, LocalCoinSwap. All have scannable public P2P ad data without account auth.
- 2026-09-24: Model routing plan — Haiku for high-volume NLP fee extraction, Sonnet for general implementation, Opus 5.5 for architecture/financial-correctness/legal-risk calls.

- 2026-09-24: User deferred stack decision ("you decide"). Chose: Python 3.11+, SQLite for v1 (no infra needed, upgrade to Postgres later if scan volume demands it), Telegram for alerting.
- 2026-09-24: User provided a Telegram bot token + chat UID in chat. Stored ONLY in local `.env` (gitignored) — never committed. Repo has `.env.example` with blank placeholders. For persistence across sessions (this container is ephemeral and `.env` won't survive), move the token to a proper secret store (Railway variables, GitHub Actions secrets) before deploying — flagging for user.

## Open questions (need user input)
- Confirm final exchange list (KuCoin/Paxful excluded — see docs/ANALYSIS.md).
- Where to persist the Telegram credentials long-term (Railway vars / GH secrets) since local .env doesn't survive session restarts.

## Status
- [x] Feasibility analysis (docs/ANALYSIS.md)
- [x] Architecture mapped (docs/ARCHITECTURE.md)
- [x] Tech stack confirmed: Python, SQLite, Telegram
- [x] Scaffolding started: Binance P2P connector (working), spread engine, rule-based
      fee extractor, bank-charge calculator, Telegram notifier, SQLite storage, main.py
- [ ] Remaining 9 exchange connectors (bybit, okx, bitget, htx, gateio, mexc, noones,
      bitpapa, localcoinswap) — stub list only in config/exchanges.yaml, not yet implemented
- [ ] LLM-based fee extractor (Haiku) for long-tail remarks phrasing
- [ ] Live end-to-end test (network call to Binance) not run in this session
