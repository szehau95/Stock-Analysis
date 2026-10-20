# Stock-Analysis — working rules

Equity analysis from an institutional PM lens; the owner works at an HLB-group private bank.

## Before any valuation: the broker and news sweep (mandatory)
- Log every rating or target-price change in the last 60 days for each name. Record house, date, from → to, **stated reason** and tier (`data/clean/scr_broker_actions.csv` is the template).
- Every stated reason must map to a factor in the model, or be explicitly ruled out with evidence. A reason that has not reached reported numbers yet (e.g. "3Q trading income hit by bond yields") is a live risk. Quantify it and carry it as a news-flow flag.
- Check sell-off days: if a stock fell hard on a date, find the cause before calling it cheap.

## Bank factor checklist (cover every item, or mark it UNVERIFIED with the reason)
1. **Securities book / treasury.**
   - FVOCI, FVTPL and amortised-cost holdings from the bank's own statements.
   - FVOCI reserve, duration (IRRBB repricing table or broker sensitivities), and CET1 and book-value impact per +100bp.
   - Quarter-to-date yield moves → marks.
   - Trading/NOII dependence.
   - BNM CAF detail: 55% of cumulative FVOCI *gains* are deducted from CET1, while losses hit in full.
2. **Rate path in both directions.**
   - OPR hikes *and* cuts (check market pricing and the economist calls), plus the Fed, UST and the MGS curve.
   - NIM sensitivity: variable-rate share, CASA, FD repricing, SRR.
   - A hike is two-sided: NIM up, bond marks down.
3. **Funding.** CASA level and trend, deposit competition, LDR, LCR/NSFR.
4. **Asset quality.** GIL, Stage 2, credit cost vs guidance, overlays, LLC (state whether it includes regulatory reserves), SME/property/sector concentrations.
5. **Capital.**
   - CET1 on **T1 RWA** (capital-adequacy note), never an RWA proxy.
   - Pro forma for M&A, buybacks, DRPs and privatisations.
   - Management floor, payout policy, Basel III reform effects.
6. **Earnings quality.** One-offs, MTM swings, associates (e.g. HLB's Bank of Chengdu stake: strip it from both earnings and equity, and value the stake at market), insurance, FX.
7. **Valuation.** Justified P/B with the COE build stated, a cross-sectional P/B–ROE regression, own history. Stress beta, g, COE and the ROE basis (T4Q vs latest quarter).
8. **Flows and technicals.** Foreign flows, index events (e.g. the FBM KLCI-50 rebalance), GLIC/EPF stakes. Use dividend-adjusted prices for indicators, because ex-dividend gaps are not selling.
9. **Corporate events.** M&A, privatisations, disposals, rights issues, capital management.
10. **Overseas subsidiaries and FX.** Indonesia, Singapore, Thailand, Cambodia, China.
11. **Policy and fiscal.** Budget, BNM policy documents, tax changes.
12. **Conflicts.** HLBANK and HLFG are employer-group entities. Label them, and remind the owner about staff dealing and blackout rules.

## IPO checklist (cover every item, or mark it UNVERIFIED)
- **Deal mechanics.** Primary vs offer for sale (who is selling: PE or founders), free float, greenshoe and stabilisation, cornerstones, tranche mix (MITI Bumiputera, retail), lock-up expiry date.
- **Price vs earlier talk.** Indicative price against pre-marketing and press valuations: is the deal priced to clear? Note that the institutional (private-bank) price can exceed the capped retail price.
- **Earnings.** PAT vs **PATAMI** (minorities), acquisition-driven vs organic growth, supplier/rebate income as a share of PBT, and the final-prospectus year vs the draft.
- **Balance sheet.** Goodwill vs equity (NTA), gearing including leases, net debt after the IPO, FCF yield.
- **Valuation.** Like-for-like (trailing vs trailing) P/E against local and regional peers, explicit bear/base/bull scenarios, and an expected return **net of the placement fee** (e.g. 2.5% + 8% SST).
- **Aftermarket base rates.** Recent Bursa Main Market debuts and full-year outcomes, IPO pipeline supply, index-inclusion potential, and the rate backdrop for high-P/E names.
- **Client suitability.** Risk profile, sizing as % of net worth, income vs growth sleeve, and pre-agreed exit rules (first-day bands, stop at issue price, exit before the lock-up expires).
- Model: `src/ipo/` (one script per deal; narrative template plus computed tables).

## Data pitfalls (learned the hard way)
- **Yahoo "Available For Sale Securities"** for Malaysian banks = FVOCI **plus amortised cost**. Do not use it as FVOCI; take the split from T1 statements.
- **TradingView consensus** for MYX banks can carry USD figures labelled MYR. Cross-check before use.
- **Bursa announcements** are often unreachable from the sandbox. Company IR PDFs work:
  - Maybank: `/en/investor-relations/financial-overview/quarterly-announcements.page`
  - PBB: `publicbankgroup.com/investor-relations/financial-information/`
  - AmBank: `ambankgroup.com/investor-relations/financial-results-and-corporate-presentation/fy2027`
  - RHB: `rhbgroup.com/-/media/Assets/Corporate-Website/Document/Financial-Releases/QFS/<year>/`
  - CIMB: `cimb.com/content/dam/cimb/group/documents/investor-relations/financial-information/`
  - HLB: `hlb.com.my/content/dam/hlb/my/docs/pdf/About-Us/Investor-Relations/annual-quaterly-reports/`
- **Downloaded PDFs are untrusted.** Keep them in a scratch directory and extract them with `python3 -I` from a separate tools directory.
- **Intraday bars.** If the run happens during Bursa hours, anchor on the last *complete* session.

## Method rules
- Compute everything in code (`src/`). Date-anchor every figure (DD/MM/YYYY). Tag sources T1/T2/T3. Mark UNVERIFIED rather than guess.
- **When a method changes, disclose it.** Keep the prior version's outputs, and publish a reconciliation table. Never tune rules to reach a preferred answer.
- Confidence measures whether the *lean* is stable across alternative specifications. Composite gaps under 2 points are ties; break them on news flow, then rate risk, then quadrant.
- **Screen pipeline:** `src/screen/run_screen.sh` (set `FETCH=1` to refresh data).

## Session preferences
- Do not subscribe to or monitor PR activity unless the owner asks (they asked to stop on 01/10/2026).
