# Project Memory

Persistent memory log for this project (replaces Obsidian — no Obsidian connector available in this account). Updated after each completed milestone.

## Decisions
- 2026-09-24: No Obsidian connector available. User chose repo files as memory store instead.
- 2026-09-24: Scope defined as read-only P2P spread scanner + fee-aware profitability calc, v1. Auto-execution deferred (legal/regulatory risk — P2P trade execution requires KYC'd accounts per exchange and crosses into money-transmission territory).
- 2026-09-24: Target exchanges for v1 (10): Binance, Bybit, OKX, Bitget, HTX, Gate.io, MEXC, Noones, Bitpapa, LocalCoinSwap. All have scannable public P2P ad data without account auth.
- 2026-09-24: Model routing plan — Haiku for high-volume NLP fee extraction, Sonnet for general implementation, Opus 5.5 for architecture/financial-correctness/legal-risk calls.

- 2026-09-24: User deferred stack decision ("you decide"). Chose: Python 3.11+, SQLite for v1 (no infra needed, upgrade to Postgres later if scan volume demands it), Telegram for alerting.
- 2026-09-24: User provided a Telegram bot token + chat UID in chat. Stored ONLY in local `.env` (gitignored) — never committed. Repo has `.env.example` with blank placeholders. For persistence across sessions (this container is ephemeral and `.env` won't survive), move the token to a proper secret store (Railway variables, GitHub Actions secrets) before deploying — flagging for user.

- 2026-09-24: This dev sandbox's network policy blocks outbound to p2p.binance.com and
  api.telegram.org (allowlist is currently just package registries + Anthropic). Could not
  live-test Binance connector or Telegram alerting. Not a code issue — fix is broadening
  network access in the environment's settings (cloud environment menu -> Edit -> Network access),
  or moving execution to an environment with broader access.
- 2026-09-24: Implemented Bybit and OKX connectors on top of Binance (best-effort, based on
  community reverse-engineered field names — none of the 3 have been verified against a live
  response in this session due to the network block above). Bitget/HTX/Gate.io/MEXC/Noones/
  Bitpapa/LocalCoinSwap left as explicit NotImplementedError stubs in
  apps/connectors/unimplemented.py rather than guessed at, since none could be verified either
  and shipping unverified guesses as "done" isn't honest.

## Open questions (need user input)
- Broaden this environment's network access (p2p.binance.com, api2.bybit.com, okx.com,
  api.telegram.org) so the scanner can actually run and be tested live.
- Persist Telegram credentials properly: add TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID as
  environment secrets (cloud environment settings) rather than pasting in chat — a local
  .env doesn't survive this container being recycled.
- Confirm final exchange list (KuCoin/Paxful excluded — see docs/ANALYSIS.md).
- Implement remaining 7 connectors, or deprioritize some?

## Status
- [x] Feasibility analysis (docs/ANALYSIS.md)
- [x] Architecture mapped (docs/ARCHITECTURE.md)
- [x] Tech stack confirmed: Python, SQLite, Telegram
- [x] Scaffolding: spread engine, rule-based fee extractor, bank-charge calculator,
      Telegram notifier, SQLite storage, main.py orchestration
- [x] Connectors: Binance, Bybit, OKX implemented (untested live — network blocked)
- [ ] Connectors: Bitget, HTX, Gate.io, MEXC, Noones, Bitpapa, LocalCoinSwap
- [ ] LLM-based fee extractor (Haiku) for long-tail remarks phrasing
- [ ] Live end-to-end test — blocked on network access, see open questions
