"""Parse Oracle Form 4 / Form 144 filings from EDGAR (Tier 1)."""
import urllib.request, json, re, time, xml.etree.ElementTree as ET, pandas as pd
UA={"User-Agent":"research contact limszehau95@gmail.com"}
def get(u):
    time.sleep(0.15); return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read()
feed=get("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341439&type=&dateb=&owner=include&count=100&output=atom").decode()
ents=re.findall(r"<filing-date>(.*?)</filing-date>.*?<filing-href>(.*?)</filing-href>.*?<filing-type>(.*?)</filing-type>",feed,re.S)
CODES={"S":"Open-mkt sale","P":"Open-mkt BUY","M":"Option exercise","F":"Tax withholding","A":"Grant/award","G":"Gift","C":"Conversion","D":"Disposed to issuer","X":"Option exercise"}
rows=[]; r144=[]
for fdate,href,ftype in ents:
    if fdate<"2026-03-01" or ftype not in ("4","4/A","144"): continue
    base=href.rsplit("/",1)[0]
    idx=json.loads(get(base+"/index.json"))
    xmls=[i["name"] for i in idx["directory"]["item"] if i["name"].endswith(".xml") and "primary_doc" in i["name"] or (ftype.startswith("4") and i["name"].endswith(".xml") and not i["name"].startswith("R"))]
    if not xmls: continue
    x=get(base+"/"+xmls[0]).decode(errors="ignore")
    x=re.sub(r'\sxmlns(:\w+)?="[^"]+"','',x); x=re.sub(r'<(/?)\w+:',r'<\1',x)
    root=ET.fromstring(x)
    if ftype=="144":
        g=lambda p: (root.findtext(p) or "").strip()
        name=g(".//nameOfPersonForWhoseAccountTheSecuritiesAreToBeSold") or "?"
        r144.append([fdate,name,g(".//noOfUnitsSold"),g(".//aggregateMarketValue"),g(".//approxSaleDate"),g(".//natureOfAcquisitionTransaction")]); continue
    who=root.findtext(".//reportingOwner/reportingOwnerId/rptOwnerName")
    rel=root.find(".//reportingOwnerRelationship"); title=(rel.findtext("officerTitle") or ("Director" if rel.findtext("isDirector") in ("1","true") else "")) if rel is not None else ""
    plan = "10b5-1" if "10b5-1" in x else ""
    for t in root.findall(".//nonDerivativeTransaction"):
        code=t.findtext(".//transactionCoding/transactionCode")
        sh=float(t.findtext(".//transactionShares/value") or 0); px=t.findtext(".//transactionPricePerShare/value")
        ad=t.findtext(".//transactionAcquiredDisposedCode/value"); post=t.findtext(".//sharesOwnedFollowingTransaction/value")
        rows.append([fdate,t.findtext(".//transactionDate/value"),who,title,code,CODES.get(code,code),ad,sh,float(px) if px else None,float(post) if post else None,plan])
df=pd.DataFrame(rows,columns=["filed","txn_date","insider","title","code","type","A/D","shares","price","owned_after","10b5-1"])
df["value_$"]=(df.shares*df.price).round(0)
pd.set_option("display.width",250); pd.set_option("display.max_columns",20)
print(df.sort_values("txn_date",ascending=False).to_string(index=False))
df.to_csv("data/insider_form4.csv",index=False)
print("\nForm 144:"); print(pd.DataFrame(r144,columns=["filed","seller","shares","mkt_value","approx_sale","acq_nature"]).to_string(index=False))
s=df[df.code=="S"]; b=df[df.code=="P"]
print(f"\nOpen-market SALES since 1-Mar-26: {len(s)} txns, {s.shares.sum():,.0f} sh, ${s['value_$'].sum():,.0f}")
print(f"Open-market BUYS since 1-Mar-26: {len(b)} txns, ${b['value_$'].sum():,.0f}")
print(s.groupby("insider")[["shares","value_$"]].sum().sort_values("value_$",ascending=False).to_string())
