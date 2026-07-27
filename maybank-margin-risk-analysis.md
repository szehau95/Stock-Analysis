# Maybank (MYX: 1155) on Margin — Risk & Drawdown Analysis

**Date:** 27 July 2026
**Reference price:** RM 10.84 (screenshot); RM 10.88 last close
**Purpose:** Enumerate the risks of buying MAYBANK with share margin financing (SMF), and quantify maximum drawdown across scenarios.

> This is analysis, not investment advice. Numbers marked *broker-specific* must be confirmed against your own facility letter — margin of finance, rate, and trigger levels vary by lender and are revisable at the lender's discretion.

---

## 1. Position snapshot

| Metric | Value |
|---|---|
| Price | RM 10.84 |
| 52-week range | RM 9.39 – 12.42 |
| Distance below 52w high | −12.7% |
| PE (rolling 4Q) | 12.6 |
| PB | 1.450 |
| NTA | RM 7.4779 |
| EPS (rolling 4Q) | 86.03 sen |
| DPS | 63 sen |
| Dividend yield | 5.81% |
| ROE | 11.5% |
| Market cap | RM 131.1bn |
| Shares out | 12.10bn |

Maybank is the largest listed company on Bursa Malaysia, trading at a modest premium to book with a well-covered dividend (payout ≈ 73% of EPS). Nothing in the fundamentals is alarming. **The risk in this trade is not the company — it is the financing structure.**

---

## 2. The mechanics that create the risk

Malaysian SMF facilities are governed by a **margin ratio**:

```
Margin ratio = Market value of collateral / Outstanding loan balance
```

Standard industry trigger levels (*broker-specific — confirm yours*):

| Event | Ratio | Consequence |
|---|---|---|
| Margin call | ~150% | Top up cash/collateral, typically within **1–3 market days** |
| Force-selling | **130%** | Broker liquidates at its discretion, without your consent |

The 130% automatic-liquidation threshold is the long-standing Bursa/SC norm. During COVID the SC temporarily gave brokers *discretion* not to force-sell — that was a relief measure, not a permanent right, and you should assume it does not apply to you.

**The critical arithmetic:** if you draw down the *maximum* margin of finance offered, your starting ratio is already close to the margin-call line.

```
Starting ratio = 1 / MOF
MOF 60%  ->  167%   (only 17 points above the 150% call level)
MOF 70%  ->  143%   (already BELOW the call level)
```

---

## 3. Trigger map — how far Maybank must fall before you are hit

Leverage = 1 / (1 − MOF). Price drop required to trigger each event:

| MOF | Leverage | Start ratio | Margin call at | Force-sell at | Equity zero at |
|---|---|---|---|---|---|
| 30% | 1.43x | 333% | −55.0% | −61.0% | −70.0% |
| 40% | 1.67x | 250% | −40.0% | −48.0% | −60.0% |
| 50% | 2.00x | 200% | −25.0% | −35.0% | −50.0% |
| **60%** | **2.50x** | **167%** | **−10.0%** | **−22.0%** | **−40.0%** |
| 65% | 2.86x | 154% | −2.5% | −15.5% | −35.0% |
| 70% | 3.33x | 143% | *immediate* | −9.0% | −30.0% |

Translated into actual Maybank prices from RM 10.84:

| MOF | Margin call price | Force-sell price | Equity wiped out |
|---|---|---|---|
| 30% | RM 4.88 | RM 4.23 | RM 3.25 |
| 40% | RM 6.50 | RM 5.64 | RM 4.34 |
| 50% | RM 8.13 | RM 7.05 | RM 5.42 |
| **60%** | **RM 9.76** | **RM 8.46** | **RM 6.50** |
| 65% | RM 10.57 | RM 9.16 | RM 7.05 |
| 70% | RM 11.38 | RM 9.86 | RM 7.59 |

> **Note the 60% MOF row.** The margin call price of RM 9.76 is *inside the last 12 months' trading range* — Maybank closed at RM 9.39 as recently as 31 July 2025.

---

## 4. What Maybank actually does — real drawdown history

Every drawdown episode >15% on MAYBANK, 2001–2026 (daily data, Yahoo Finance):

### Total-return basis (adjusted for splits, rights, dividends)

| Peak | Trough | Drawdown | Recovered |
|---|---|---|---|
| Sep 2001 | Sep 2001 | −18.8% | Dec 2001 |
| Apr 2002 | Dec 2002 | −24.1% | Jul 2003 |
| Mar 2004 | May 2004 | −17.1% | Nov 2004 |
| Feb 2007 | Aug 2007 | −17.9% | Jan 2008 |
| **Jan 2008** | **Mar 2009** | **−59.2%** | **Sep 2010** |
| Jun 2011 | Sep 2011 | −16.6% | Feb 2012 |
| Jul 2013 | Dec 2014 | −17.5% | Mar 2017 |
| May 2018 | Mar 2020 | −26.5% | Oct 2021 |

### Raw price basis (what your collateral is actually marked at)

| Peak | Trough | Drawdown | Recovered | Time underwater |
|---|---|---|---|---|
| Feb 2007 RM 9.84 | Mar 2009 RM 3.57 | **−63.7%** | May 2013 | **6.2 years** |
| Jul 2013 RM 10.74 | Sep 2016 RM 7.50 | −30.2% | Apr 2018 | 4.8 years |
| May 2018 RM 10.88 | Oct 2020 RM 7.00 | −35.7% | Sep 2024 | **6.3 years** |
| Feb 2026 RM 12.38 | Jun 2026 RM 10.42 | −15.8% | *ongoing* | — |

> Raw price overstates the GFC decline because of the Feb 2009 rights issue; the true economic loss was closer to the −59% adjusted figure. But **your margin ratio is computed on raw market value**, so the raw column is what triggers liquidation.

### Distribution of the worst 12-month drawdown (rolling, 2001–2026)

| Percentile | Worst 12m drawdown |
|---|---|
| Median | **−13.5%** |
| 75th | −18.4% |
| 90th | −23.1% |
| 95th | −32.1% |
| 99th | −51.6% |
| Absolute worst | −55.5% |

**This is the single most important table in this document.** In a *median* year — not a crisis, an ordinary year — Maybank has a 13.5% peak-to-trough dip. At 60% MOF your margin call sits at −10%. **You would be margin-called in a typical year, more often than not.**

---

## 5. Maximum drawdown by scenario

RM 100,000 own capital, 1 year held, borrow rate 5.5%, dividend 5.81% received.
Figures are **change in your own equity**, mark-to-market.

| Scenario | 1.0x (cash) | 1.5x | 2.0x | 2.5x |
|---|---|---|---|---|
| Median year (−13.5%) | −7.7% | −14.3% | −20.9% | −27.5% |
| Typical bad year (−18.4%) | −12.6% | −21.6% | −30.7% | −39.7% |
| 1-in-10 year (−23.1%) | −17.3% | −28.7% | −40.1% | −51.5% ⚠ |
| 1-in-20 year (−32.1%) | −26.3% | −42.2% | −58.1% | −74.0% ⚠ |
| COVID-era (−35.7%) | −29.9% | −47.6% | −65.3% ⚠ | −83.0% ⚠ |
| 1-in-100 (−51.6%) | −45.8% | −71.4% | −97.1% ⚠ | −122.7% ⚠ |
| GFC repeat (−59.2%) | −53.4% | −82.8% ⚠ | −112.3% ⚠ | −141.7% ⚠ |

⚠ = **position force-sold before this point.** You do not get to hold and recover — the loss is crystallised at the liquidation price.

### The real maximum drawdown: crystallised loss at force-sell

Because liquidation happens at a *fixed ratio*, the loss it locks in is deterministic. Equity remaining at the 130% trigger = 30% of the loan balance.

| MOF | Leverage | Force-sell at price drop | Equity left | **Loss** | If gapped to 120% |
|---|---|---|---|---|---|
| 30% | 1.43x | −61.0% | RM 12,857 | **−87%** | −91% |
| 40% | 1.67x | −48.0% | RM 20,000 | **−80%** | −87% |
| 50% | 2.00x | −35.0% | RM 30,000 | **−70%** | −80% |
| 60% | 2.50x | −22.0% | RM 45,000 | **−55%** | −70% |
| 65% | 2.86x | −15.5% | RM 55,714 | **−44%** | −63% |

Read this correctly: **lower leverage does not mean a smaller loss once you are force-sold** — it means force-selling is far less likely, but if the market falls far enough to trigger it anyway, you have ridden it down further and lose more. The protection from low leverage is in *avoiding the trigger*, not in softening it.

**Absolute worst case: greater than 100% loss.** At 2.0x+ in a GFC-magnitude decline with a gap-down (limit-down opens, suspension, or a weekend event), the collateral can be worth less than the loan. Malaysian SMF is **full recourse** — you owe the shortfall in cash, and the broker can pursue your other assets.

---

## 6. Complete risk register

### 6.1 Financing / structural risks

| # | Risk | Detail |
|---|---|---|
| 1 | **Force-selling at the worst price** | Broker liquidates at 130% at its sole discretion, into a falling market, typically at market orders. You have no say in timing or price. |
| 2 | **Margin call timing** | 1–3 market days to fund. If you cannot raise cash that fast, you are liquidated regardless of your conviction. |
| 3 | **Gap risk** | Triggers are not guarantees. A limit-down open, trading halt, or weekend news can take you straight past 130% to below 100%. |
| 4 | **Full recourse / negative equity** | Losses are not capped at your capital. A shortfall is a personal debt. |
| 5 | **MOF can be cut unilaterally** | Brokers reduce margin of finance on a counter — or across the board — in stressed markets. Your ratio worsens *with no price movement*. This happens precisely when markets are falling. |
| 6 | **Rate is floating** | Priced off SBR (currently 2.75%, OPR held at 2.75% since Jul 2025). Rate rises flow straight through. |
| 7 | **Facility is callable** | Most SMF facilities are repayable on demand. The lender can withdraw the line. |
| 8 | **Concentration in one counter** | Single-stock collateral gets a harsher haircut and offers no diversification. Some brokers cap single-counter exposure within the facility. |
| 9 | **IDSS flag** | The screenshot shows Maybank is **IDSS-eligible** (Intraday Short Selling). It can be shorted intraday, which can amplify short-term downside volatility. |

### 6.2 The carry trap

The seductive case for this trade: dividend yield 5.81% > borrowing cost ~5.5%, so the position appears to fund itself.

**Net annual carry, % of your own capital:**

| Borrow rate | 1.0x | 1.5x | 2.0x | 2.5x |
|---|---|---|---|---|
| 4.50% | 5.81% | 6.46% | 7.12% | 7.77% |
| **5.50%** | 5.81% | 5.96% | 6.12% | **6.27%** |
| 6.50% | 5.81% | 5.46% | 5.12% | 4.77% |
| 7.50% | 5.81% | 4.96% | 4.12% | 3.28% |

At 2.5x and 5.5%, leverage buys you **+0.46% p.a.** over simply holding the shares in cash — while multiplying your downside by 2.5x. **The entire positive-carry case rests on a ~31bp spread.**

That spread breaks in three ordinary ways:

**(a) Rates rise.** One 25bp OPR hike roughly halves it. Two erase it.

**(b) Maybank cuts the dividend.** It has done exactly this: **FY2019 DPS 64 sen → FY2020 DPS 52 sen (−18.8%)**, on COVID impairments. Re-run at DY 4.80%:

| Borrow rate | 1.0x | 1.5x | 2.0x | 2.5x |
|---|---|---|---|---|
| 4.50% | 4.80% | 4.95% | 5.09% | 5.24% |
| **5.50%** | 4.80% | 4.45% | 4.09% | **3.74%** |
| 6.50% | 4.80% | 3.95% | 3.09% | 2.24% |
| 7.50% | 4.80% | 3.45% | 2.09% | **0.74%** |

Leverage now makes you **worse off than holding cash at every rate level**. And a dividend cut is *correlated* with the price falling — you lose the carry exactly when you are also being margin-called.

**(c) Dividend timing mismatch.** Interest accrues monthly; dividends arrive twice a year. You must fund the gap from other income.

### 6.3 Company & sector risks

| # | Risk | Detail |
|---|---|---|
| 10 | **Credit cycle** | Maybank is a bank — earnings are geared to loan losses. A Malaysian recession hits provisions, EPS, dividend, *and* the share price together. |
| 11 | **NIM compression** | OPR at 2.75% and expected to stay there. Further cuts compress net interest margin. |
| 12 | **Regional exposure** | Significant Singapore and Indonesia operations — FX translation and Indonesian credit risk. |
| 13 | **Dividend is ~73% of EPS** | Little buffer. An earnings decline forces a payout cut or an uncomfortable payout ratio. |
| 14 | **Regulatory capital** | BNM can restrict distributions in stress (as regulators did globally in 2020). |
| 15 | **Not a growth story** | ROE 11.5%, PB 1.45. Total return is mostly the dividend. Leverage amplifies a *low-return* asset — you take equity-crash risk for bond-like upside. |
| 16 | **Index/foreign flows** | As the largest KLCI constituent, Maybank is the liquidity vehicle foreign investors sell first in an EM risk-off. |

### 6.4 The time risk nobody prices

Maybank's recoveries are **slow**:

- 2007 peak → recovered **May 2013** (6.2 years underwater)
- 2018 peak → recovered **Sep 2024** (6.3 years underwater)

Interest bill while you wait (RM 100k capital, 5.5%):

| Leverage | 3 years | 6 years |
|---|---|---|
| 1.5x | RM 8,250 (8% of capital) | RM 16,500 (16%) |
| 2.0x | RM 16,500 (17%) | RM 33,000 (33%) |
| 2.5x | RM 24,750 (25%) | **RM 49,500 (50%)** |

**At 2.5x, a six-year recovery costs you half your starting capital in interest alone — even if the price fully recovers and you are never force-sold.** "Just hold on and wait for recovery" is not a free option on margin. It is the most expensive option there is.

---

## 7. Where the risk actually concentrates

The scenario that ends this trade is not a GFC. It is mundane:

1. You take 60% MOF at RM 10.84 (2.5x — the level most brokers will happily extend on a blue chip).
2. Maybank drifts to RM 9.76 — a 10% fall, **smaller than its median annual drawdown**, and a price it traded at nine months ago.
3. Margin call. You have 1–3 days to find cash.
4. If you cannot, or if it keeps sliding to RM 8.46 (−22%, less than the 90th-percentile year), you are force-sold.
5. **Crystallised loss: −55% of your capital, plus accrued interest.** Maybank does not need a crisis to do this. It needs an ordinary bad year.

---

## 8. Practical risk controls

If proceeding regardless:

1. **Do not draw the full MOF.** The offer is the broker's risk appetite, not yours. Drawing 60% because it is offered is the single most common way this trade fails.
2. **Size to survive −35%, not −13.5%.** Target a starting ratio ≥ 250% (≈40% MOF, 1.67x). That puts the margin call at RM 6.50 — below the COVID low — and keeps you outside every non-GFC episode in 25 years of history.
3. **Hold a dedicated top-up reserve in cash**, sized to fund a call at a −25% price level, outside the margin account. If the reserve is invested in equities it will be down when you need it.
4. **Write down your own force-sell price before you buy**, and treat the broker's 130% as a backstop you never reach.
5. **Confirm in writing:** exact MOF for counter 1155, the interest formula and reset frequency, the precise margin-call and force-sell ratios, the cure period in market days, whether the facility is repayable on demand, and the broker's right to revise MOF.
6. **Stress-test the carry at SBR +100bp and DPS 52 sen.** If the trade does not work under both, the carry is not the reason you are doing it — and you should be honest about what is.
7. **Never meet a margin call by pledging more of the same stock.** It raises collateral and exposure together and accelerates the next call.

---

## 9. Bottom line

| Question | Answer |
|---|---|
| Worst historical drawdown | **−59% adjusted / −64% raw price** (Jan 2008 → Mar 2009) |
| Worst 12-month drawdown | −55.5% |
| Median-year drawdown | **−13.5%** |
| Max loss at 2.0x (force-sold) | **−70%** of capital (−80% on a gap) |
| Max loss at 2.5x (force-sold) | **−55%** of capital (−70% on a gap) |
| Max loss, GFC repeat, held to the end at 2.0x+ | **>100% — you owe money** |
| Longest time underwater | **6.3 years** (2018–2024) |
| Gain from leverage at 2.5x | **+0.46% p.a.** over holding in cash |

The asymmetry is the point. At 2.5x you are risking a −55% crystallised loss, a 6-year interest drag, and full-recourse liability — to earn roughly **46 basis points a year** more than just owning the shares outright. And that 46bp evaporates entirely on one OPR hike or one dividend cut, both of which Maybank has experienced within the last cycle.

Maybank is a reasonable stock to own. **The leverage is what makes it dangerous, and at current yield-versus-funding spreads, the leverage is not being paid for.**

---

## Sources

- [Securities Commission Malaysia — Margin financing flexibilities for capital market participants](https://www.sc.com.my/resources/media/media-release/margin-financing-flexibilities-for-capital-market-participants)
- [Maybank Investment Bank — Share Margin Financing](https://www.maybank2u.com.my/Investment-bank/en/retail-investors/products/stocks-trading/financing/share-margin.page)
- [Maybank — Share Trading Margin Financing](https://www.maybank2u.com.my/maybank2u/malaysia/en/personal/loans/investment/share_trading_margin_financing.page)
- [RHB — Share Margin Financing Product Disclosure Sheet](https://www.rhbgroup.com/-/media/Files/share-margin-financing/pds_share_margin_financing.pdf)
- [Bank Negara Malaysia — OPR Decisions](https://www.bnm.gov.my/monetary-stability/opr-decisions)
- [New Straits Times — Bank Negara keeps OPR at 2.75pct (Jul 2026)](https://www.nst.com.my/business/corporate/2026/07/1484448/bank-negara-keeps-opr-275pct-growth-inflation-stay-balanced)
- [Maybank — Dividend History](https://www.maybank.com/en/investor-relations/dividends/dividend-history.page)
- [The Malaysian Reserve — Maybank 1st bank to declare full-year dividend for FY20](https://themalaysianreserve.com/2020/11/30/maybank-1st-bank-to-declare-full-year-dividend-for-fy20/)
- [Yahoo Finance — Malayan Banking Berhad (1155.KL) historical prices](https://finance.yahoo.com/quote/1155.KL/history/)
- Price history: Yahoo Finance chart API, 1155.KL, daily 2001-07-27 to 2026-07-27 (6,226 observations)
