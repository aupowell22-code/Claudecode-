# Google Sheets template — 2-minute setup

The live Sheets MCP integration was unavailable (account quota), so this folder
contains the same template as importable CSVs. Recreating the Sheet is fast.

## Steps

1. Open <https://sheets.new> (creates a new blank spreadsheet).
2. Rename it to **Buffett Watchlist**.
3. For each CSV in this folder, create a tab and import:
   - Tab **Watchlist** ← `Watchlist.csv`
   - Tab **Criteria**  ← `Criteria.csv`
   - Tab **Pipeline**  ← `Pipeline.csv`

   Per tab: `File -> Import -> Upload`, choose the CSV, set
   *Import location* = **Replace current sheet**, *Separator* = **Comma**.

4. On **Watchlist**:
   - Freeze the header row: `View -> Freeze -> 1 row`.
   - Add a conditional-format rule on column R (`Verdict`):
     - `STRONG` → green
     - `WATCH`  → yellow
     - `PASS`   → grey
   - In any empty cell (e.g. `T1`), add a sort hint:
     `=SORT(A2:T100, 16, TRUE)` — sorts a copy by `% to buy zone` ascending.

5. On **Pipeline**, select the TRUE/FALSE columns and use
   `Insert -> Checkbox` to convert them to clickable checkboxes.

## Filling it in

- Run the screener:

  ```bash
  python buffett_screener.py --tickers-file tickers.example.txt --csv watchlist.csv
  ```

- Open `watchlist.csv` in Sheets (or paste it into the **Watchlist** tab —
  match the column order to the header row).
- Fill in the qualitative columns by hand: **Moat type**, **Moat 1-5**, **Notes**.
- Tick **Pipeline** boxes as you complete each due-diligence step per ticker.
- Sort **Watchlist** by `% to buy zone` ascending. Negative values mean the
  stock is trading inside your buy-below price.

## Tweaking criteria

Edit thresholds in the **Criteria** tab to remind yourself what the screener
uses; if you actually want different thresholds, change `THRESHOLDS` at the top
of `buffett_screener.py` and rerun.
