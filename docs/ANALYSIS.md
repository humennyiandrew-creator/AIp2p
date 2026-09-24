# Feasibility Analysis — P2P Spread Scanning Agent

## Verdict
**Possible, with caveats.** The hard parts are not "can we call an API" — most major exchanges expose P2P order-book data — but ToS/legal risk, data-quality (free-text ad terms), and the fact that spreads move faster than most polling loops.

## 1. Exchange coverage (P2P markets, 10+ target)

| Exchange | Public P2P ad API | Auth required for scanning? | Notes |
|---|---|---|---|
| Binance P2P | Yes (undocumented REST, widely reverse-engineered: `/bapi/c2c/v2/friendly/c2c/adv/search`) | No | Most liquid market. ToS technically restricts automated/bot access — see §3. |
| Bybit P2P | Yes (documented-ish, same pattern as Binance) | No | |
| OKX P2P | Yes | No | |
| Bitget P2P | Yes | No | |
| Huobi/HTX P2P | Yes | No | |
| Gate.io P2P | Yes | No | |
| MEXC P2P | Yes | No | |
| KuCoin | No public P2P ad-book API | N/A | Would need browser automation — higher risk, likely excluded from v1 |
| Paxful | Deprecated in favor of Noones | — | |
| Noones (Paxful successor) | Yes, has a real public API | No for read | Good candidate, more permissive ToS historically |
| Bitpapa | Yes | No | |
| LocalCoinSwap | Yes | No | |

→ 10 is achievable using: Binance, Bybit, OKX, Bitget, HTX, Gate.io, MEXC, Noones, Bitpapa, LocalCoinSwap. All of these can be scanned **without account credentials** — P2P ad listings are public. Authenticated API keys are only needed if the agent later *executes* trades, not for scanning.

## 2. Spread detection (≥1.5%)
Straightforward once normalized ad data is in hand: for a given (asset, fiat) pair, compare best buy price on exchange A vs best sell price on exchange B (or same exchange different side), compute `(sell - buy) / buy`. Flag ≥1.5%. The real difficulty is **normalization** — each exchange has different min/max limits, payment-method taxonomies, and merchant verification levels that affect whether a spread is actually executable.

## 3. Legal / ToS risk (the actual blocker to watch)
- Binance's terms prohibit "scraping" and automated use of undocumented endpoints in some jurisdictions; enforcement varies (rate-limit/IP-block is the typical consequence, not legal action, for read-only scanning).
- P2P trading itself is regulated as money-transmission/VASP activity in many countries. An agent that only **scans and alerts** is low risk; one that **auto-executes trades** crosses into a different regulatory category and needs KYC-compliant accounts on every exchange.
- Recommendation: v1 = read-only scanner + alerting. Execution stays human-in-the-loop until legal review.

## 4. Hidden-fee / trade-description analysis
P2P ad "remarks"/terms fields are free text, e.g. "only Chase or BofA, no memo, 2% fee for card, must be verified 30+ days." This is an NLP extraction problem, not a data problem:
- Rule-based regex catches common patterns (explicit % fees, bank whitelist/blacklist, minimum account age).
- LLM pass (cheap model, e.g. Haiku) for the long tail — ambiguous/informal phrasing, multiple languages.
- Output: structured `{extra_fee_pct, allowed_payment_methods, restrictions[], confidence}`.

## 5. Bank/card charge calculation
Needs a maintained fee table: card cash-advance vs. purchase treatment, wire fees, FX markup by bank/network. This data isn't available via API from any exchange — it has to be a curated table (seeded manually, updatable) keyed by `(country, bank_or_method)`. Net profitability = `spread% - hidden_fee% - bank_charge% - withdrawal_fee%`.

## 6. Practical risks not to skip
- **Speed**: P2P spreads close in seconds to minutes. A polling interval that's too slow makes "opportunities" theoretical.
- **Liquidity/limits**: A 3% spread on an ad with a $50 cap isn't a real opportunity at scale.
- **Counterparty risk**: P2P trades settle via real bank transfers with real counterparties; scanning doesn't eliminate settlement risk.
- **Rate limits / bans**: needs backoff, rotating request patterns, and graceful degradation per exchange.

## Conclusion
Build a **read-only, multi-exchange P2P spread scanner + fee-aware profitability calculator** first. Treat "connects to accounts" as needed only for a later execution phase, not for scanning. This is the scope reflected in the architecture doc.
