"""Inject rendered tables (output/tables.md) into reports/narrative.md -> reports/MY_Banks_Correction_Verdict_30092026.md"""
import re, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
T = dict(re.findall(r"<!--(\w+)-->\n(.*?)\n\n(?=<!--|\Z)", open("output/tables.md").read(), re.S))
s = open("reports/narrative.md").read()
missing = [k for k in re.findall(r"\{\{(\w+)\}\}", s) if k not in T]
assert not missing, missing
s = re.sub(r"\{\{(\w+)\}\}", lambda m: T[m.group(1)], s)
open("reports/MY_Banks_Correction_Verdict_30092026.md", "w").write(s)
print("written", len(s))
