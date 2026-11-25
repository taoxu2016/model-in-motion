"""Model in Motion · The Logistic Fixed-Effect Model · Episode 15: The funnel.

Every number the episode shows or says is computed here, checked, and written to e15_numbers.json.
Scenes and narration read e15_numbers.json; nothing numeric is typed into scene code or the script.

    python e15_numbers.py        # from this folder: prints the ledger, runs every check, writes e15_numbers.json
"""
from __future__ import annotations

import json
import logging
import sys
import warnings
from math import sqrt
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, coin_pmf, expit, fit, mid_p, rows  # noqa: E402
from mim.crowd import joint_fit, simulate  # noqa: E402

warnings.simplefilter("ignore")
logging.disable(logging.CRITICAL)
import pandas as pd  # noqa: E402
from pprof_py import LogisticFixedEffectModel  # noqa: E402

ALL = list(CAST)
PROV, X01, Y = rows(ALL)
CHECKS: list[tuple[str, bool, str]] = []
fl = lambda a, k=3: [round(float(v), k) for v in a]
Z95 = 1.959964


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


E13 = json.loads((HERE.parent / "e13_unequal_coins" / "e13_numbers.json").read_text())
E14 = json.loads((HERE.parent / "e14_three_shortcuts" / "e14_numbers.json").read_text())


def measures(c, max_iter=30):
    """Fit a crowd and return, for each provider, what the funnel needs: observed, expected and spread at the reference."""
    F = joint_fit(c, max_iter=max_iter)
    g0 = float(np.median(F["gamma"]))
    p0 = expit(g0 + F["X"] @ F["beta"])
    m = len(F["gamma"])
    O = np.bincount(F["prov"], weights=F["y"], minlength=m)
    E = np.bincount(F["prov"], weights=p0, minlength=m)
    V = np.bincount(F["prov"], weights=p0 * (1 - p0), minlength=m)
    planted = np.zeros(m, dtype=int)
    planted[list(c["planted_high"])] = 1; planted[list(c["planted_low"])] = -1
    return {"O": O, "E": E, "V": V, "ratio": O / E, "precision": E * E / V, "z": (O - E) / np.sqrt(V), "n": c["n"], "planted": planted, "p0": p0, "starts": np.concatenate([[0], np.cumsum(c["n"])]), "g0": g0, "fit": F}


# ----------------------------------------------------------------------------- 1. the league table (S01)
LV = measures(simulate(seed=2026, tau=0.0, plant=0.8))                             # the level crowd: 194 identical providers and six planted at +-0.8
ordinary = LV["planted"] == 0
order = np.argsort(-LV["ratio"])                                                  # the league table: highest ratio first
rank = np.empty(200, dtype=int); rank[order] = np.arange(1, 201)
check("the level crowd: 200 providers, 194 identical and six that truly differ, three worse and three better", len(LV["n"]) == 200 and int(ordinary.sum()) == 194
      and (int((LV["planted"] == 1).sum()), int((LV["planted"] == -1).sum())) == (3, 3))
check("their ratios run from 0.32 to 2.03", (round(float(LV["ratio"].min()), 2), round(float(LV["ratio"].max()), 2)) == (0.32, 2.03))
picks = list(order[:3]) + list(order[-3:])
right = [int(i) for i in picks if LV["planted"][i] != 0]
wrong = [int(i) for i in picks if LV["planted"][i] == 0]
median_size = float(np.median(LV["n"]))
check("pick the three highest and the three lowest: two of the six are right, and the four wrong ones are all smaller than the median provider",
      len(right) == 2 and len(wrong) == 4 and all(LV["n"][i] < median_size for i in wrong), f"right {[int(LV['n'][i]) for i in right]} patients; wrong {[int(LV['n'][i]) for i in wrong]} patients; median {median_size}")
ends = list(order[:10]) + list(order[-10:])
ends_ordinary = [i for i in ends if LV["planted"][i] == 0]
check("of the 16 identical providers in the top and bottom ten, 13 are smaller than the median", len(ends_ordinary) == 16 and sum(LV["n"][i] < median_size for i in ends_ordinary) == 13)
check("the six sit at ranks 1, 4 and 8 from the top and 164, 185 and 198", sorted(int(rank[i]) for i in np.where(LV["planted"] != 0)[0]) == [1, 4, 8, 164, 185, 198])

# ----------------------------------------------------------------------------- 2. from pile to band (S03)
cast = {k: {"O": E14["cast"][k]["observed"], "E": E14["cast"][k]["expected"], "V": E14["cast"][k]["sd"] ** 2} for k in ALL}
for k in ALL:
    cast[k]["ratio"] = cast[k]["O"] / cast[k]["E"]
    cast[k]["precision"] = cast[k]["E"] ** 2 / cast[k]["V"]
    cast[k]["lower"], cast[k]["upper"] = 1 - Z95 / sqrt(cast[k]["precision"]), 1 + Z95 / sqrt(cast[k]["precision"])
dune = np.array(E13["pmf"]["Dune"])
check("Dune's pile divided by its 4.8 expected sits on the ratio scale, centred on 1", abs(cast["Dune"]["E"] - 4.8) < 1e-9 and abs(float((np.arange(13) / cast["Dune"]["E"]) @ dune) - 1.0) < 1e-9)
check("Dune's precision is 10 and its band runs from 0.38 to 1.62 (blueprint)", round(cast["Dune"]["precision"], 1) == 10.0 and (round(cast["Dune"]["lower"], 2), round(cast["Dune"]["upper"], 2)) == (0.38, 1.62))
inside = [k for k in range(13) if cast["Dune"]["lower"] <= k / cast["Dune"]["E"] <= cast["Dune"]["upper"]]
check("that band holds 95% of Dune's exact pile: the counts from 2 to 7", inside == [2, 3, 4, 5, 6, 7] and round(100 * float(dune[inside].sum())) == 95, f"{dune[inside].sum():.4f}")
check("Birch's precision is 39 and its band runs from 0.69 to 1.31 (blueprint)", round(cast["Birch"]["precision"]) == 39 and (round(cast["Birch"]["lower"], 2), round(cast["Birch"]["upper"], 2)) == (0.69, 1.31))

# ----------------------------------------------------------------------------- 3. join the edges (S04)
check("the cast on the funnel: Alder (13.0, 1.62), Dune (10.0, 1.46), Cedar (16.7, 1.00), Birch (39.1, 0.88), Elm (2.4, 0) (blueprint)",
      [(round(cast[k]["precision"], 1), round(cast[k]["ratio"], 2)) for k in ("Alder", "Dune", "Cedar", "Birch", "Elm")] == [(13.0, 1.62), (10.0, 1.46), (16.7, 1.0), (39.1, 0.88), (2.4, 0.0)])
outside = [k for k in ALL if not cast[k]["lower"] <= cast[k]["ratio"] <= cast[k]["upper"]]
check("only Alder lies outside: 1.62 against an upper edge of 1.54", outside == ["Alder"] and round(cast["Alder"]["upper"], 2) == 1.54)
check("outside the funnel is the bell-curve test's flag, clinic for clinic", all((abs(E14["z"]["bell"][k]) > Z95) == (k in outside) for k in ALL))
check("at Elm's precision the lower edge is below zero (-0.27): no count could flag it as better", round(cast["Elm"]["lower"], 2) == -0.27 and abs(E14["z"]["bell"]["Elm"]) < Z95 and E13["p_value"]["Elm"] > 0.05)
PK = LogisticFixedEffectModel().fit(pd.DataFrame({"clinic": np.array(ALL)[PROV], "x": X01, "y": Y}), y_var="y", x_vars=["x"], provider_var="clinic")
fun = PK.funnel_limits().providers
check("pprof_py's funnel limits and flags for the cast are the same", all(abs(float(fun.loc[k, "lower"]) - cast[k]["lower"]) < 1e-4 and abs(float(fun.loc[k, "upper"]) - cast[k]["upper"]) < 1e-4
                                                                         and (int(fun.loc[k, "flag"]) != 0) == (k in outside) for k in ALL))

check("a clinic can be flagged as better only if its precision exceeds 3.84; Elm's is 2.4", abs(Z95 ** 2 - 3.84) < 0.005 and cast["Elm"]["precision"] < Z95 ** 2 < cast["Dune"]["precision"])

# ----------------------------------------------------------------------------- 4. two hundred at once (S05)
out_lv = np.abs(LV["z"]) > Z95
check("of the 194 identical providers, 13 fall outside the funnel (blueprint): 6.7%", int(out_lv[ordinary].sum()) == 13 and round(100 * 13 / 194, 1) == 6.7)
REDRAWS, share = 50, []
for j in range(REDRAWS):
    R = measures(simulate(seed=4000 + 10 * j, tau=0.0, plant=0.8))
    share.append(float((np.abs(R["z"]) > Z95)[R["planted"] == 0].mean()))
check("over fifty redraws of the crowd the share outside averages 5% (blueprint: 5.0% over a hundred)", round(100 * float(np.mean(share))) == 5, f"{100 * np.mean(share):.2f}%, from {100 * min(share):.1f}% to {100 * max(share):.1f}%")
pl = [{"n": int(LV["n"][i]), "kind": "worse" if LV["planted"][i] == 1 else "better", "ratio": float(LV["ratio"][i]), "precision": float(LV["precision"][i]), "z": float(LV["z"][i]),
       "caught": bool(out_lv[i]), "rank": int(rank[i])} for i in np.where(LV["planted"] != 0)[0]]
caught = sorted((d["kind"], d["n"]) for d in pl if d["caught"])
missed = sorted((d["kind"], d["n"]) for d in pl if not d["caught"])
check("of the six who truly differ, the funnel catches three and misses both with 37 patients and the better one with 105 (blueprint)",
      caught == [("better", 285), ("worse", 100), ("worse", 280)] and missed == [("better", 37), ("better", 105), ("worse", 37)], f"caught {caught}; missed {missed}")
exact_flag = np.array([mid_p(coin_pmf(LV["p0"][LV["starts"][i]:LV["starts"][i + 1]]), int(LV["O"][i])) < 0.05 for i in range(200)])
check("for the record: the exact test flags 11 of the 194 (blueprint) and the same three of the six", int(exact_flag[ordinary].sum()) == 11 and int(exact_flag[~ordinary].sum()) == 3)

# ----------------------------------------------------------------------------- 5. why precision, not size (S06)
prec = lambda n, p: (n * p) ** 2 / (n * p * (1 - p))
check("two providers of 100 patients, one with risks near 5% and one near 40%: precisions 5 and 67", (round(prec(100, 0.05)), round(prec(100, 0.40))) == (5, 67), f"{prec(100, 0.05):.2f}, {prec(100, 0.40):.2f}")
near = (LV["n"] >= 90) & (LV["n"] <= 110)
check("in the crowd, providers of about a hundred patients (90 to 110) have precisions from 19 to 74", int(near.sum()) >= 8 and (round(float(LV["precision"][near].min())), round(float(LV["precision"][near].max()))) == (19, 74),
      f"{int(near.sum())} providers: {LV['precision'][near].min():.1f} to {LV['precision'][near].max():.1f}")

# ----------------------------------------------------------------------------- 6. the caterpillar (S07)
def one_sided(ps, o, g_shift, upper):
    f = coin_pmf(expit(np.log(ps / (1 - ps)) + g_shift))
    return float(f[o + 1:].sum() + 0.5 * f[o]) if upper else float(f[:o].sum() + 0.5 * f[o])


def exact_ratio_interval(ps, o):
    """Exact 95% interval for observed over expected, by sliding the provider's level until the count sits on the edge of a tail."""
    def solve(upper):
        lo, hi = -8.0, 8.0
        for _ in range(34):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if (one_sided(ps, o, mid, upper) < 0.025) == upper else (lo, mid)
        return 0.5 * (lo + hi)
    e0 = float(ps.sum())
    low = float(expit(np.log(ps / (1 - ps)) + solve(True)).sum()) / e0 if o > 0 else 0.0
    return low, float(expit(np.log(ps / (1 - ps)) + solve(False)).sum()) / e0


cat = []
for i in range(200):
    ps = LV["p0"][LV["starts"][i]:LV["starts"][i + 1]]
    a, b = exact_ratio_interval(ps, int(LV["O"][i]))
    cat.append({"ratio": float(LV["ratio"][i]), "low": a, "high": b, "flag": bool(exact_flag[i]), "planted": int(LV["planted"][i]), "n": int(LV["n"][i])})
check("each provider's exact interval leaves out 1 exactly when the exact test flags it", all((not (d["low"] <= 1.0 <= d["high"])) == d["flag"] for d in cat))
check("the caterpillar's intervals are widest at the ends of the table: the ten highest and ten lowest average 1.0 wide, the middle hundred 0.7",
      round(float(np.mean([cat[i]["high"] - cat[i]["low"] for i in ends])), 1) == 1.0 and round(float(np.mean([cat[i]["high"] - cat[i]["low"] for i in order[50:150]])), 1) == 0.7,
      f"{np.mean([cat[i]['high'] - cat[i]['low'] for i in ends]):.2f}, {np.mean([cat[i]['high'] - cat[i]['low'] for i in order[50:150]]):.2f}")
gaps = -np.diff(LV["ratio"][order])
check("neighbours in the league table differ by about 0.01 on average", round(float(gaps.mean()), 2) == 0.01, f"{gaps.mean():.4f}")
cast_iv = E13["ratio_interval"]
d_ok = [k for k in range(13) if mid_p(dune, k) >= 0.05]
check("the exact funnel for Dune: counts 2 to 7 are unflagged, so its limits fall half-way between counts, at 0.31 and 1.56, against the smooth 0.38 and 1.62",
      d_ok == [2, 3, 4, 5, 6, 7] and (round(1.5 / cast["Dune"]["E"], 2), round(7.5 / cast["Dune"]["E"], 2)) == (0.31, 1.56))

# ----------------------------------------------------------------------------- 7. when providers truly differ (S08)
TR = measures(simulate(seed=2026, tau=0.3, plant=0.8))                             # the series' usual crowd: providers differ a little
out_tr = np.abs(TR["z"]) > Z95
ord_tr = TR["planted"] == 0
check("let providers truly differ a little and about a quarter of the 194 leave the funnel", round(float(out_tr[ord_tr].mean()), 2) in (0.24, 0.25, 0.26, 0.27), f"{int(out_tr[ord_tr].sum())} of 194, {100 * out_tr[ord_tr].mean():.1f}%")
exact_tr = int(sum(mid_p(coin_pmf(TR["p0"][TR["starts"][i]:TR["starts"][i + 1]]), int(TR["O"][i])) < 0.05 for i in np.where(ord_tr)[0]))
check("for the record: the exact test flags 48 of those 194 (blueprint)", exact_tr == 48)

dots = lambda M, flags: [{"precision": float(M["precision"][i]), "ratio": float(M["ratio"][i]), "out": bool(flags[i]), "planted": int(M["planted"][i]), "n": int(M["n"][i])} for i in range(200)]
OUT = {
    "episode": 15, "title": "The Funnel", "clinics": ALL, "z95": Z95, "cast": cast, "cast_interval": cast_iv, "dune_pmf": dune.tolist(), "dune_band_counts": inside,
    "league": {"ratios": [float(LV["ratio"][i]) for i in order], "planted": [int(LV["planted"][i]) for i in order], "n": [int(LV["n"][i]) for i in order], "median_size": median_size,
               "picks_right": len(right), "picks_wrong_sizes": [int(LV["n"][i]) for i in wrong], "ends_small": 13, "ends_ordinary": 16},
    "level": {"dots": dots(LV, out_lv), "outside": int(out_lv[ordinary].sum()), "ordinary": 194, "share": 13 / 194, "redraws": REDRAWS, "redraw_share": float(np.mean(share)), "planted": pl,
              "exact_flags": int(exact_flag[ordinary].sum())},
    "size": {"low_risk": prec(100, 0.05), "high_risk": prec(100, 0.40), "near_100": [float(LV["precision"][near].min()), float(LV["precision"][near].max())]},
    "caterpillar": [cat[i] for i in order], "dune_exact_limits": [1.5 / cast["Dune"]["E"], 7.5 / cast["Dune"]["E"]],
    "differ": {"dots": dots(TR, out_tr), "outside": int(out_tr[ord_tr].sum()), "share": float(out_tr[ord_tr].mean()), "exact_flags": exact_tr},
}

if __name__ == "__main__":
    print("cast     ", {k: (round(cast[k]["precision"], 1), round(cast[k]["ratio"], 2), round(cast[k]["lower"], 3), round(cast[k]["upper"], 3)) for k in ALL})
    print("picks     right", [int(LV["n"][i]) for i in right], "wrong", [int(LV["n"][i]) for i in wrong], "| median size", median_size)
    print(f"level     13 of 194 outside; redraws {100 * np.mean(share):.2f}%; exact flags {int(exact_flag[ordinary].sum())}")
    print("planted  ", [(d["kind"], d["n"], round(d["ratio"], 2), round(d["precision"], 1), round(d["z"], 2), d["caught"], d["rank"]) for d in pl])
    print(f"differ    {int(out_tr[ord_tr].sum())} of 194 outside ({100 * out_tr[ord_tr].mean():.1f}%); exact {exact_tr}")
    print(f"near 100  {int(near.sum())} providers, precision {LV['precision'][near].min():.1f} to {LV['precision'][near].max():.1f}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e15_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
