"""Base run (2 seeds x 120k sims) + lap-1 conditionals + one-at-a-time sensitivity (20k each)."""
import copy
import json

from race_mc import BASE, simulate

TOP = ["VER", "ANT", "HAM", "RUS", "HAD", "LEC", "NOR", "PIA"]


def fmt(r, idx):
    return " ".join(f"{c}={r['p'][idx[c]]:.3f}" for c in TOP)


runs = [simulate(BASE, 300, 400, seed=s) for s in (7, 8)]
idx = {c: i for i, c in enumerate(runs[0]["codes"])}
for s, r in zip((7, 8), runs):
    print(f"BASE seed={s} sims={r['sims']}")
    for c in TOP:
        print(f"  {c} {r['p'][idx[c]]:.4f} [{r['lo'][idx[c]]:.3f}, {r['hi'][idx[c]]:.3f}]")
    for k, v in r["by_scen"].items():
        print("  ", k, round(v["share"], 3), {c: round(v[c], 3) for c in TOP})
pooled = {c: (runs[0]["p"][idx[c]] + runs[1]["p"][idx[c]]) / 2 for c in runs[0]["codes"]}
print("POOLED 240k", {c: round(pooled[c], 4) for c in TOP})
json.dump(dict(runs=runs, pooled=pooled), open("base_result.json", "w"), indent=1)

r = runs[0]
print("\nLAP-1 CONDITIONALS (seed 7)")
for c in ["VER", "HAM", "ANT", "RUS", "HAD", "LEC"]:
    print(" ", c, {k: f"P(win)={v[0]:.3f} freq={v[1]:.3f}" for k, v in r["cond"][c].items()})
print("  VER|SC", round(r["cond"]["VER_given_SC"], 3), "VER|noSC", round(r["cond"]["VER_given_noSC"], 3))


def run(name, **kw):
    cfg = copy.deepcopy(BASE)
    cfg.update(kw)
    print(f"{name:28s}", fmt(simulate(cfg, 40, 500, seed=11), idx))


print("\nSENSITIVITY (20k sims each, common seed)")
run("reference")
run("VER pace -0.10", pace_shift={"VER": -0.10})
run("VER pace +0.10", pace_shift={"VER": 0.10})
run("ANT pace -0.10", pace_shift={"ANT": -0.10})
run("ANT pace +0.10", pace_shift={"ANT": 0.10})
run("HAM pace -0.10", pace_shift={"HAM": -0.10})
run("RUS pace +0.10", pace_shift={"RUS": 0.10})
run("HAD pace +0.10", pace_shift={"HAD": 0.10})
run("rain: dry 0.70", p_rain=(0.70, 0.25, 0.05))
run("rain: wet-heavy", p_rain=(0.20, 0.45, 0.35))
run("all dry", p_rain=(0.999, 0.0005, 0.0005))
run("pass harder (0.04/0.4)", pass_base=0.04, pass_slope=0.4)
run("pass easier (0.15/0.9)", pass_base=0.15, pass_slope=0.9)
run("VER DNF 0.03", dnf_set={"VER": 0.03})
run("VER DNF 0.12", dnf_set={"VER": 0.12})
run("start sd 0.6", start_sd=0.6)
run("deg 0.15", deg=0.15)
run("SC prob x0.6", p_sc=(0.27, 0.39, 0.51))
