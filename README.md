# Stock-Analysis
Analyze stocks from an institutional PM lens.

## Structure
- `templates/equity-research-master-prompt.md` — reusable Fundamental + Technical research engine.
  Fill the PARAMETERS block per ticker and run.
- `research/` — dated per-ticker briefs produced from the template.
  - `ENTG-2026-07-01.md` — Entegris fundamental + technical brief (intraday chart provided).

## Sourcing discipline
Primary sources only (SEC filings, company IR, recognized financial news). Every figure carries an
as-of date; unverifiable metrics are marked "data unavailable" rather than estimated.
