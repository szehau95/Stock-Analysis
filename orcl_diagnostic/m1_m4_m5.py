import pandas as pd, numpy as np
df = pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)
r = df[["ORCL","^GSPC","^NDX","CRWV","NVDA","AVGO","SMH","MSFT","AMZN","GOOGL","IGV"]].pct_change()*100
r["PEERS_EW"] = r[["MSFT","AMZN","GOOGL","CRWV","NVDA","AVGO","SMH","IGV"]].mean(axis=1)
c = df["ORCL_close"]

print("=== MODULE 1: event-day moves (close-to-close %) ===")
ev = [("2025-09-10","Q1 FY26 print (9 Sep AMC): RPO $455B; ORCL all-time closing high"),
      ("2025-10-17","Day after AI World FY30 targets ($225B rev) + 30-40% OCI GM guide; sell-the-news"),
      ("2025-12-11","Q2 FY26 (10 Dec AMC): rev/cloud miss; FY26 capex guide +$15B to ~$50B"),
      ("2026-02-02","Plan to raise $45-50B debt+equity in CY2026 (incl. ATM)"),
      ("2026-02-05","Week -15.8%: CDS elevated, OpenAI exposure, PT cuts"),
      ("2026-03-11","Q3 FY26 (10 Mar): 'best quarter in 15 yrs'; FCF TTM -$24.7B"),
      ("2026-05-29","Wedbush PT $275, $30B US govt deal; momentum squeeze"),
      ("2026-06-01","Continuation of squeeze; local high $248.15"),
      ("2026-06-05","AVGO AI guide disappointment spills over; Hold downgrade 2 Jun"),
      ("2026-06-11","Q4 FY26 (10 Jun AMC): FY27 capex $90-95B gross/$70B net; $40B raise incl. $20B ATM"),
      ("2026-06-22","10-K filed: $260B uncommenced leases; headcount -13%"),
      ("2026-06-23","ATM prospectus (424B5) / ATM amendment"),
      ("2026-07-09","S&P cuts to BBB- (stable); OpenAI named key credit risk"),
      ("2026-07-10","Post-downgrade reversal"),
      ("2026-07-24","Cycle low close $114.99"),
      ("2026-07-30","GOOGL Gemini on OCI; MSFT Azure >$100B (29 Jul)"),
      ("2026-09-01","Global bond selloff; UST30Y near 20y high"),
      ("2026-09-10","Q1 FY27 day-of (release AMC): pre-print risk-off"),
      ("2026-09-11","Q1 FY27 reaction: beat/raise, RPO $664B, FCF -$5.4B; opened +7.5%, reversed"),
      ("2026-09-14","Ellison cancels 10b5-1 (PR 12 Sep, 8-K 14 Sep); AI-regulation/Fed hike fear"),
      ("2026-09-17","Relief bounce"),
      ("2026-09-23","No discrete catalyst; balance-sheet scrutiny"),
      ("2026-09-24","Bloomberg: force majeure notice to Blue Owl on Project Jupiter (NM); CDS record ~227bp"),
      ("2026-09-25","Follow-through"),
      ("2026-09-28","Reports of new layoff round; Jupiter loan stress")]
rows=[]
for d,e in ev:
    d=pd.Timestamp(d)
    if d in r.index: rows.append([d.date(), e, r.at[d,"ORCL"], r.at[d,"^GSPC"], r.at[d,"PEERS_EW"], r.at[d,"CRWV"], r.at[d,"ORCL"]-r.at[d,"PEERS_EW"]])
t=pd.DataFrame(rows,columns=["date","event","ORCL%","SPX%","PeersEW%","CRWV%","ORCL-Peers"]).round(2)
pd.set_option("display.width",250); pd.set_option("display.max_colwidth",95)
print(t.to_string(index=False)); t.to_csv("data/event_table.csv",index=False)

print("\n=== MODULE 3.5: earnings reaction realized vs implied ===")
E=[("2025-12-10","2025-12-11",None),("2026-03-10","2026-03-11",None),("2026-06-10","2026-06-11",12.0),("2026-09-10","2026-09-11",11.5)]
for pre,post,imp in E:
    p0=c[:pre].iloc[-1]; p1=c[post]; p5=c[post:].iloc[4]; pm1=c[:pre].iloc[-2]
    print(f"{post}: 1d {(p1/p0-1)*100:+.1f}% | from prior-day close {(p1/pm1-1)*100:+.1f}% | +5d drift {(p5/p0-1)*100:+.1f}% | implied ±{imp if imp else 'n/a'}%")
o=df["ORCL_open"]; print(f"11-Sep-26 open gap {(o['2026-09-11']/c['2026-09-10']-1)*100:+.1f}%, open->close {(c['2026-09-11']/o['2026-09-11']-1)*100:+.1f}%")

print("\n=== Rates / credit sensitivity (daily, since 2026-01-01) ===")
w = df.loc["2026-01-01":]
x = pd.DataFrame({"orcl":w["ORCL"].pct_change(),"ndx":w["^NDX"].pct_change(),"dtnx":w["^TNX"].diff(),"hyg":w["HYG"].pct_change()}).dropna()
X=np.column_stack([np.ones(len(x)),x.ndx,x.dtnx,x.hyg]); b=np.linalg.lstsq(X,x.orcl,rcond=None)[0]
print(f"ORCL = a + {b[1]:.2f}*NDX + {b[2]*100:.2f}%/per 1pt(10bp?) dTNX + {b[3]:.2f}*HYG   (TNX quoted in %, so coef per 1.00 = 100bp)")
print(f"=> per +10bp 10Y: {b[2]*0.1*100:+.2f}% ORCL beyond NDX beta")
print("10Y yield: 2026-09-08 %.2f  2026-09-28 %.2f ; since 2025-09-10: %.2f -> %.2f" % (df['^TNX']['2026-09-08'],df['^TNX'].iloc[-1],df['^TNX']['2025-09-10'],df['^TNX'].iloc[-1]))

print("\n=== ATM supply vs volume (Jun-Aug 2026 = FQ1 FY27) ===")
v=df["ORCL_vol"]["2026-06-01":"2026-08-31"]; n=len(v)
print(f"days={n}, avg vol={v.mean()/1e6:.1f}M, ATM 141M sh -> {141/n:.2f}M/day = {141e6/n/v.mean()*100:.1f}% of ADV; implied avg ATM price ${19.909e9/141e6:.2f}")
vw=(df['ORCL_close']*df['ORCL_vol'])["2026-06-01":"2026-08-31"].sum()/v.sum(); print(f"Quarter VWAP (close-weighted) ${vw:.2f}")

print("\n=== MODULE 4 scorecard math ($B) ===")
q = dict(rev=19.345, rev_py=14.926, gop=6.728, gop_py=4.277, int_=1.428, int_py=0.923, ocf=23.1, ocf_py=23.1/2.84, capex=28.499, capex_py=8.502,
         prepay=11.363, cash=36.369+0.7, debt=125.337, opl=34.621, unc_lease=288, unc_lease_prior=260, rpo=664, rpo_prior=638, rpo12=0.13,
         cs_rev=17.157, cs_m=9.358, cs_rev_py=12.907, cs_m_py=7.691, sbc=1.127, dep=3.156, dep_py=1.351, sh=3024, sh_prior=2880, fy26_fcf=-23.7)
fcf=q["ocf"]-q["capex"]; fcf_py=q["ocf_py"]-q["capex_py"]
print(f"Q1 FCF {fcf:.1f} (PY {fcf_py:.2f}); FCF ex-customer-prepayments {q['ocf']-q['prepay']-q['capex']:.1f}")
print(f"TTM FCF {q['fy26_fcf']+fcf-fcf_py:.1f}")
print(f"Capex/Revenue {q['capex']/q['rev']*100:.0f}% ; capex/OCF {q['capex']/q['ocf']:.2f}x ; capex/OCF ex-prepay {q['capex']/(q['ocf']-q['prepay']):.2f}x")
print(f"Net debt {q['debt']-q['cash']:.1f}; + on-BS op leases {q['debt']-q['cash']+q['opl']:.1f}; uncommenced leases {q['unc_lease']} (+{q['unc_lease']-q['unc_lease_prior']} QoQ)")
print(f"GAAP EBIT/interest {q['gop']/q['int_']:.1f}x vs PY {q['gop_py']/q['int_py']:.1f}x ; interest +{(q['int_']/q['int_py']-1)*100:.0f}%")
print(f"Cloud&software segment margin {q['cs_m']/q['cs_rev']*100:.1f}% vs PY {q['cs_m_py']/q['cs_rev_py']*100:.1f}% ; depreciation +{(q['dep']/q['dep_py']-1)*100:.0f}%")
print(f"RPO next-12m ${q['rpo']*q['rpo12']:.0f}B ; RPO QoQ +{q['rpo']-q['rpo_prior']} ; share count +{(q['sh']/q['sh_prior']-1)*100:.1f}% QoQ ; SBC/rev {q['sbc']/q['rev']*100:.1f}%")
print(f"Uncommenced leases / market cap: {q['unc_lease']/(c.iloc[-1]*q['sh']/1000):.2f}x ; mkt cap ${c.iloc[-1]*q['sh']/1000:.0f}B")
print(f"P/E on FY27 non-GAAP EPS $8.10: {c.iloc[-1]/8.10:.1f}x")
