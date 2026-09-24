# AIp2p — P2P Spread Scanner

Read-only agent that scans P2P markets across multiple exchanges for cross-exchange
spreads, parses ad text for hidden fees, adjusts for bank/card charges, and alerts
via Telegram when net spread clears the threshold (default 1.5%).

See `docs/ANALYSIS.md` for the feasibility writeup and `docs/ARCHITECTURE.md` for
the module map. `MEMORY.md` is the running project log.

## Status
- Binance P2P connector implemented and working.
- 9 more exchange connectors stubbed in `apps/connectors/` (see `config/exchanges.yaml`).
- Rule-based hidden-fee extraction in place; LLM-based extraction for long-tail
  phrasing is planned (routed to Haiku — see docs/ARCHITECTURE.md).
- Auto-execution is out of scope for v1 (see docs/ANALYSIS.md, §3 legal/ToS risk).

## Setup
```
pip install -r requirements.txt
cp .env.example .env   # fill in TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
python main.py
```
