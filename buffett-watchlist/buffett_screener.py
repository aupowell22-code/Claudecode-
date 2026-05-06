"""
Buffett-style stock screener.

Pulls fundamentals from Yahoo Finance (via yfinance) for a list of tickers and
flags each one against a Buffett/Munger-style criteria set:

  - ROE >= 15%
  - Debt/Equity <= 0.5
  - Operating margin >= 15%
  - Gross margin >= 40%
  - Net margin >= 10%
  - Free cash flow > 0
  - Positive earnings growth
  - Reasonable price (P/E <= 25 by default)

A simple owner-earnings-style intrinsic value estimate and margin-of-safety
buy price are also computed. These are conservative heuristics, not advice.

Usage
-----
    python buffett_screener.py KO PEP MSFT AAPL
    python buffett_screener.py --tickers tickers.txt --csv out.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass, asdict
from typing import Optional

try:
    import yfinance as yf
except ImportError:
    sys.stderr.write(
        "yfinance is required. Install with:  pip install -r requirements.txt\n"
    )
    sys.exit(1)


# ---- Buffett-style thresholds (tweak in one place) -------------------------

THRESHOLDS = {
    "roe_min": 0.15,
    "debt_to_equity_max": 0.5,
    "operating_margin_min": 0.15,
    "gross_margin_min": 0.40,
    "net_margin_min": 0.10,
    "pe_max": 25.0,
    "discount_rate": 0.10,
    "terminal_growth": 0.025,
    "margin_of_safety": 0.30,  # buy at 70% of intrinsic value
}


# ---- Data model ------------------------------------------------------------

@dataclass
class Metrics:
    ticker: str
    name: Optional[str] = None
    sector: Optional[str] = None
    price: Optional[float] = None
    market_cap: Optional[float] = None
    pe: Optional[float] = None
    roe: Optional[float] = None
    debt_to_equity: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    free_cash_flow: Optional[float] = None
    earnings_growth: Optional[float] = None
    intrinsic_value_per_share: Optional[float] = None
    buy_below_price: Optional[float] = None
    pct_to_buy_zone: Optional[float] = None
    score: Optional[int] = None
    verdict: Optional[str] = None
    notes: str = ""


# ---- Fetching --------------------------------------------------------------

def _safe(value, scale: float = 1.0) -> Optional[float]:
    """Coerce a yfinance value to float, returning None on missing/junk."""
    if value is None:
        return None
    try:
        out = float(value) * scale
    except (TypeError, ValueError):
        return None
    if out != out:  # NaN
        return None
    return out


def fetch(ticker: str) -> Metrics:
    t = yf.Ticker(ticker)
    info = getattr(t, "info", {}) or {}

    m = Metrics(ticker=ticker)
    m.name = info.get("longName") or info.get("shortName")
    m.sector = info.get("sector")
    m.price = _safe(info.get("currentPrice") or info.get("regularMarketPrice"))
    m.market_cap = _safe(info.get("marketCap"))
    m.pe = _safe(info.get("trailingPE"))
    m.roe = _safe(info.get("returnOnEquity"))
    # yfinance reports debtToEquity as a percentage (e.g. 50.0 => 0.50)
    m.debt_to_equity = _safe(info.get("debtToEquity"), scale=0.01)
    m.gross_margin = _safe(info.get("grossMargins"))
    m.operating_margin = _safe(info.get("operatingMargins"))
    m.net_margin = _safe(info.get("profitMargins"))
    m.free_cash_flow = _safe(info.get("freeCashflow"))
    m.earnings_growth = _safe(info.get("earningsGrowth"))

    iv, buy = intrinsic_value(m)
    m.intrinsic_value_per_share = iv
    m.buy_below_price = buy
    if buy and m.price:
        m.pct_to_buy_zone = (m.price - buy) / buy

    score(m)
    return m


# ---- Valuation -------------------------------------------------------------

def intrinsic_value(m: Metrics) -> tuple[Optional[float], Optional[float]]:
    """
    Two-stage DCF on free cash flow per share.

    Stage 1: 10 years at company's earnings growth rate (capped at 12%).
    Stage 2: terminal value at 2.5% perpetual growth.
    Discount: 10%.

    Returns (intrinsic_value_per_share, buy_below_price).
    """
    if not m.free_cash_flow or not m.market_cap or not m.price:
        return None, None
    shares = m.market_cap / m.price
    if shares <= 0:
        return None, None

    fcf_per_share = m.free_cash_flow / shares
    if fcf_per_share <= 0:
        return None, None

    g_stage1 = m.earnings_growth if m.earnings_growth is not None else 0.05
    g_stage1 = max(min(g_stage1, 0.12), 0.0)
    g_terminal = THRESHOLDS["terminal_growth"]
    r = THRESHOLDS["discount_rate"]

    pv = 0.0
    cf = fcf_per_share
    for year in range(1, 11):
        cf *= (1 + g_stage1)
        pv += cf / (1 + r) ** year

    terminal = cf * (1 + g_terminal) / (r - g_terminal)
    pv += terminal / (1 + r) ** 10

    buy = pv * (1 - THRESHOLDS["margin_of_safety"])
    return round(pv, 2), round(buy, 2)


# ---- Scoring ---------------------------------------------------------------

CRITERIA = [
    ("ROE >= 15%", lambda m: m.roe is not None and m.roe >= THRESHOLDS["roe_min"]),
    ("D/E <= 0.5", lambda m: m.debt_to_equity is not None and m.debt_to_equity <= THRESHOLDS["debt_to_equity_max"]),
    ("Operating margin >= 15%", lambda m: m.operating_margin is not None and m.operating_margin >= THRESHOLDS["operating_margin_min"]),
    ("Gross margin >= 40%", lambda m: m.gross_margin is not None and m.gross_margin >= THRESHOLDS["gross_margin_min"]),
    ("Net margin >= 10%", lambda m: m.net_margin is not None and m.net_margin >= THRESHOLDS["net_margin_min"]),
    ("Free cash flow > 0", lambda m: m.free_cash_flow is not None and m.free_cash_flow > 0),
    ("Earnings growth > 0", lambda m: m.earnings_growth is not None and m.earnings_growth > 0),
    ("P/E <= 25", lambda m: m.pe is not None and m.pe <= THRESHOLDS["pe_max"]),
]


def score(m: Metrics) -> None:
    passed, failed = [], []
    for name, fn in CRITERIA:
        try:
            (passed if fn(m) else failed).append(name)
        except Exception:
            failed.append(f"{name} (error)")
    m.score = len(passed)
    if m.score >= 7:
        m.verdict = "STRONG"
    elif m.score >= 5:
        m.verdict = "WATCH"
    else:
        m.verdict = "PASS"
    if failed:
        m.notes = "Fails: " + "; ".join(failed)


# ---- Output ----------------------------------------------------------------

def fmt_pct(x: Optional[float]) -> str:
    return "n/a" if x is None else f"{x * 100:.1f}%"


def fmt_num(x: Optional[float]) -> str:
    return "n/a" if x is None else f"{x:,.2f}"


def print_report(metrics: list[Metrics]) -> None:
    metrics.sort(key=lambda m: (-(m.score or 0), m.pct_to_buy_zone if m.pct_to_buy_zone is not None else 9e9))
    header = f"{'Ticker':<7}{'Verdict':<9}{'Score':<7}{'Price':>10}{'IV':>10}{'Buy<':>10}{'%Gap':>8}{'ROE':>8}{'D/E':>8}{'OpM':>8}{'P/E':>8}"
    print(header)
    print("-" * len(header))
    for m in metrics:
        print(
            f"{m.ticker:<7}"
            f"{(m.verdict or '?'):<9}"
            f"{(str(m.score) if m.score is not None else '-'):<7}"
            f"{fmt_num(m.price):>10}"
            f"{fmt_num(m.intrinsic_value_per_share):>10}"
            f"{fmt_num(m.buy_below_price):>10}"
            f"{fmt_pct(m.pct_to_buy_zone):>8}"
            f"{fmt_pct(m.roe):>8}"
            f"{fmt_num(m.debt_to_equity):>8}"
            f"{fmt_pct(m.operating_margin):>8}"
            f"{fmt_num(m.pe):>8}"
        )
    print("\nLegend: %Gap < 0 means price is below buy-zone (potential value).")
    print("STRONG = 7+ criteria pass, WATCH = 5-6, PASS = <5.")


def write_csv(metrics: list[Metrics], path: str) -> None:
    fields = list(asdict(metrics[0]).keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for m in metrics:
            w.writerow(asdict(m))
    print(f"\nWrote {len(metrics)} rows to {path}")


# ---- CLI -------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("tickers", nargs="*", help="Ticker symbols (e.g. KO PEP MSFT)")
    p.add_argument("--tickers-file", help="File with one ticker per line")
    p.add_argument("--csv", help="Optional path to write a CSV report")
    return p.parse_args()


def load_tickers(args: argparse.Namespace) -> list[str]:
    tickers = list(args.tickers)
    if args.tickers_file:
        with open(args.tickers_file) as f:
            tickers.extend(line.strip() for line in f if line.strip() and not line.startswith("#"))
    if not tickers:
        sys.stderr.write("Provide tickers as args or via --tickers-file.\n")
        sys.exit(2)
    return [t.upper() for t in tickers]


def main() -> None:
    args = parse_args()
    tickers = load_tickers(args)
    results: list[Metrics] = []
    for tk in tickers:
        print(f"Fetching {tk}...", file=sys.stderr)
        try:
            results.append(fetch(tk))
        except Exception as e:
            sys.stderr.write(f"  failed: {e}\n")
            results.append(Metrics(ticker=tk, verdict="ERROR", notes=str(e)))
    print()
    print_report(results)
    if args.csv:
        write_csv(results, args.csv)


if __name__ == "__main__":
    main()
