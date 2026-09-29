import pandas as pd, numpy as np, contextlib, io
exec(open("m3_attribution.py").read().split("res = {}")[0])
with contextlib.redirect_stdout(io.StringIO()):
    w, resid = decompose("2025-09-10","2026-09-28","A","pre")
cats = {
 "Capex/FCF/funding & dilution": ["2025-12-11","2025-12-12","2026-02-02","2026-06-11","2026-06-12","2026-06-22","2026-06-23","2026-06-24","2026-06-25","2026-06-26","2026-09-10","2026-09-11"],
 "Credit/counterparty/execution (CDS, S&P, OpenAI, Jupiter)": ["2025-11-13","2025-11-14","2025-11-20","2026-02-03","2026-02-04","2026-02-05","2026-07-10","2026-09-23","2026-09-24","2026-09-25","2026-09-28"],
 "Post-hype unwind of Sep-25 spike (Sep-Oct 2025)": [str(d.date()) for d in w.loc["2025-09-11":"2025-10-31"].index],
 "May-Jun 2026 squeeze (+) and reversal": ["2026-05-28","2026-05-29","2026-06-01","2026-06-02","2026-06-03","2026-06-04","2026-06-05"],
}
tot_idio = resid.sum(); tot = w["ORCL"].sum(); used=set()
rows=[]
for k,ds in cats.items():
    ds=[pd.Timestamp(d) for d in ds if pd.Timestamp(d) in resid.index and d not in used]; used |= {str(d.date()) for d in ds}
    rows.append([k,len(ds),resid[ds].sum()*100, resid[ds].sum()/tot*100])
other = [d for d in resid.index if str(d.date()) not in used]
rows.append(["Residual grind (no single catalyst day)",len(other),resid[other].sum()*100,resid[other].sum()/tot*100])
print("total log move %.1f lp; idio %.1f lp (%.0f%% of move)" % (tot*100, tot_idio*100, tot_idio/tot*100))
print(pd.DataFrame(rows,columns=["category","days","idio logpts","% of total drawdown"]).round(1).to_string(index=False))
