# Buffett Watchlist Toolkit

A small, opinionated toolkit for building and maintaining a Warren Buffett /
Charlie Munger style stock watchlist. Two pieces:

1. **`buffett_screener.py`** — a Python CLI that pulls fundamentals for a list
   of tickers, scores them against Buffett-style criteria, and computes a
   conservative intrinsic-value-based "buy below" price.
2. **A Google Sheets template** — a structured place to record the
   *qualitative* side (moat, management, circle of competence) alongside the
   numbers from the screener. Created via the companion MCP step; columns and
   formulas are documented below so you can rebuild it manually if needed.

The screener is a research aid, not investment advice. Read the 10-K.

---

## The 8-step Buffett method this implements

1. **Define your circle of competence** — only score companies in industries
   you understand.
2. **Qualitative moat filter** — brand, switching costs, network effects, low-
   cost producer, regulatory. Track in the Sheet.
3. **Quantitative screen** — what `buffett_screener.py` automates.
4. **Read the 10-K** — manual; record findings in the Sheet's Notes column.
5. **Evaluate management** — manual; capital allocation, candor, ownership.
6. **Estimate intrinsic value** — the screener does a conservative two-stage
   DCF on free cash flow per share.
7. **Maintain the watchlist** — sort by `% to buy zone`, act only when price
   meets your number.
8. **Review quarterly, act rarely.**

---

## Screener: usage

```bash
pip install -r requirements.txt

# Inline tickers
python buffett_screener.py KO PEP MSFT AAPL

# From a file
python buffett_screener.py --tickers-file tickers.example.txt

# Write a CSV (paste into the Sheet's Watchlist tab)
python buffett_screener.py --tickers-file tickers.example.txt --csv watchlist.csv
```

### Criteria (all editable in `THRESHOLDS` at the top of the file)

| Test | Threshold |
| --- | --- |
| Return on Equity | >= 15% |
| Debt / Equity | <= 0.5 |
| Operating margin | >= 15% |
| Gross margin | >= 40% |
| Net margin | >= 10% |
| Free cash flow | > 0 |
| Earnings growth | > 0 |
| P/E ratio | <= 25 |

Verdicts: **STRONG** (7+ pass), **WATCH** (5-6), **PASS** (<5).

### Intrinsic value model

A two-stage discounted cash flow on FCF per share:

- Stage 1: 10 years at the company's reported earnings growth, capped at 12%.
- Stage 2: terminal value at 2.5% perpetual growth.
- Discount rate: 10%.
- Margin of safety: 30% (i.e., `Buy below = IV * 0.7`).

Output column `% to buy zone` is `(price - buy_price) / buy_price`. Negative =
trading inside your buy zone.

---

## Google Sheets template — column layout

The Sheet has three tabs:

### `Watchlist` (one row per company)

| Column | Notes |
| --- | --- |
| Ticker | e.g. `KO` |
| Company | Auto from screener |
| Sector | Auto from screener |
| Moat type | Manual: `Brand` / `Switching` / `Network` / `Cost` / `Regulatory` |
| Moat 1-5 | Manual confidence score in the moat |
| ROE | From screener |
| D/E | From screener |
| Op margin | From screener |
| FCF (USD) | From screener |
| P/E | From screener |
| Price | From screener |
| Intrinsic value | From screener |
| Buy below | From screener |
| % to buy zone | From screener |
| Score | From screener (0-8) |
| Verdict | STRONG / WATCH / PASS |
| Last reviewed | Manual date |
| Notes | Manual: 10-K takeaways, mgmt impressions |

### `Criteria` (the rules, in cells you can tune)

Pairs of label/value cells holding the thresholds, mirroring `THRESHOLDS` in
the Python script. Useful for quick what-if tweaks without rerunning Python.

### `Pipeline` (qualitative gates)

Checkboxes for each step of the 8-step method per ticker — circle of
competence, moat understood, 10-K read, management evaluated, IV calculated,
margin-of-safety price set.

---

## Recommended workflow

1. Add tickers to `tickers.example.txt` (or your own file) within your circle
   of competence.
2. Run `buffett_screener.py --csv watchlist.csv`.
3. Paste the CSV into the Sheet's `Watchlist` tab.
4. Fill in the qualitative columns (moat, management) and `Pipeline` checkboxes.
5. Sort by `% to buy zone` ascending. Anything negative + STRONG/WATCH is
   worth deeper diligence.
6. Rerun monthly; update `Last reviewed`.
