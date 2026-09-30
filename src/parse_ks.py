"""Parse klsescreener quarterly-report tables (tier-3 transcription of Bursa quarterly filings).
Outputs data/clean/quarterly_<BANK>.csv and dividends_ks_<BANK>.csv and substantial_<BANK>.csv"""
import re, sys, pandas as pd
from bs4 import BeautifulSoup
CODES = {"MAYBANK":1155,"PBBANK":1295,"CIMB":1023,"HLBANK":5819,"RHBBANK":1066,"AMBANK":1015,"BIMB":5258,"ALLIANCE":2488,"AFFIN":5185}

def num(s):
    s = s.replace(',', '').strip()
    if s in ('', '-'): return None
    m = re.match(r'^(-?[\d.]+)([kmb]?)$', s)
    if not m: return None
    v = float(m.group(1)); mult = {'':1,'k':1e3,'m':1e6,'b':1e9}[m.group(2)]
    return v*mult

def parse(bank, code):
    soup = BeautifulSoup(open(f"data/raw/ks_{code}.html").read(), "lxml")
    t = soup.find("table", class_="financial_reports")
    rows = []
    for r in t.find_all("tr"):
        c = [x.get_text(" ", strip=True) for x in r.find_all("td")]
        if len(c) >= 12 and re.match(r"\d{4}-\d{2}-\d{2}", c[6]):
            rows.append(dict(eps_sen=num(c[0]), dps_sen=num(c[1]), nta=num(c[2]), revenue=num(c[3]), pl=num(c[4]),
                             fq=(int(c[5]) if c[5].isdigit() else None), qdate=c[6], fy=c[7], announced=c[8], roe_q=c[9]))
    q = pd.DataFrame(rows)
    q["qdate"] = pd.to_datetime(q["qdate"]); q["announced"] = pd.to_datetime(q["announced"], errors="coerce")
    q = q.drop_duplicates("qdate").sort_values("qdate").reset_index(drop=True)
    q.to_csv(f"data/clean/quarterly_{bank}.csv", index=False)
    # substantial shareholder table
    subs = None
    for tb in soup.find_all("table"):
        hdr = [h.get_text(strip=True) for h in tb.find_all("th")]
        if hdr[:4] == ["Announced", "Date Change", "Type", "Shares"]:
            rr = [[x.get_text(" ", strip=True) for x in r.find_all("td")] for r in tb.find_all("tr")]
            rr = [x[:5] for x in rr if len(x) >= 5]
            subs = pd.DataFrame(rr, columns=["announced","date_change","type","shares","name"])
            subs.to_csv(f"data/clean/substantial_{bank}.csv", index=False)
        if hdr[:6] == ["Announced","Financial Year","Subject","EX Date","Payment Date","Amount"]:
            rr = [[x.get_text(" ", strip=True) for x in r.find_all("td")] for r in tb.find_all("tr")]
            rr = [x[:7] for x in rr if len(x) >= 6]
            pd.DataFrame(rr).to_csv(f"data/clean/dividends_ks_{bank}.csv", index=False)
    return q, subs

for b, c in CODES.items():
    q, s = parse(b, c)
    print(f"{b:9s} quarters={len(q):3d} {q.qdate.min().date()}..{q.qdate.max().date()} lastNTA={q.nta.iloc[-1]} lastEPS={q.eps_sen.iloc[-1]} subs={0 if s is None else len(s)}")
