"""Model in Motion · The Logistic Fixed-Effect Model · Episode 11: Swap the curve.

Every number the episode shows or says is computed here, checked, and written to e11_numbers.json.
Scenes and narration read e11_numbers.json; nothing numeric is typed into scene code or the script.

    python e11_numbers.py        # from this folder: prints the ledger, runs every check, writes e11_numbers.json
"""
from __future__ import annotations

import json
import logging
import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, expit, fit, logit, rows  # noqa: E402
from mim.crowd import joint_fit, simulate  # noqa: E402

warnings.simplefilter("ignore")
logging.disable(logging.CRITICAL)
import pandas as pd  # noqa: E402
from pprof_py import LogisticFixedEffectModel  # noqa: E402

ALL = list(CAST)
PROV, X01, Y = rows(ALL)
CHECKS: list[tuple[str, bool, str]] = []
fl = lambda a, k=3: [round(float(v), k) for v in a]


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


g_fit, beta, cov4, ll_fit = fit()
E9 = json.loads((HERE.parent / "e09_how_sure_are_we" / "e09_numbers.json").read_text())
E10 = json.loads((HERE.parent / "e10_no_events_no_peak" / "e10_numbers.json").read_text())
N0 = {k: CAST[k][0] for k in ALL}; N1 = {k: CAST[k][2] for k in ALL}
OBS = {k: CAST[k][1] + CAST[k][3] for k in ALL}
SIZE = {k: N0[k] + N1[k] for k in ALL}
expected = lambda k, g: N0[k] * float(expit(g)) + N1[k] * float(expit(g + beta))        # clinic k's own patients on the curve at level g

# ----------------------------------------------------------------------------- 1. the reference clinic (S03)
elm_printed = E10["printed"]["together"]
gammas = {**g_fit, "Elm": elm_printed}
ref = float(np.median(list(gammas.values())))
check("the middle of the five sliders is Cedar's, at -1.52 (blueprint: -1.523)", abs(ref - g_fit["Cedar"]) < 1e-12 and round(ref, 2) == -1.52 and abs(ref + 1.523) < 5e-4, f"{ref:.4f}")
p_lo, p_hi = float(expit(ref)), float(expit(ref + beta))
check("at the reference a lower-risk patient has an 18% chance and a higher-risk patient 62% (blueprint: 17.9% and 62.1%)",
      (round(100 * p_lo, 1), round(100 * p_hi, 1)) == (17.9, 62.1), f"{100 * p_lo:.2f}%, {100 * p_hi:.2f}%")


def median_after_move(name, to):
    g = dict(gammas); g[name] = to
    return float(np.median(list(g.values())))


order = sorted(gammas.values())
shifts = [median_after_move(k, to) for k in ALL for to in (-50.0, 50.0)]
check("push any one slider as far as you like: the middle value moves no further than the next clinic along (Birch's -1.82 or Alder's -0.65)",
      all(order[1] - 1e-12 <= s <= order[3] + 1e-12 for s in shifts) and round(order[1], 2) == -1.82 and round(order[3], 2) == -0.65, str(sorted(set(fl(shifts, 2)))))

# ----------------------------------------------------------------------------- 2. swap the curve (S04)
a_lo, a_hi = float(expit(g_fit["Alder"])), float(expit(g_fit["Alder"] + beta))
check("Alder: 24 lower-risk and 6 higher-risk patients, 13 readmissions", (N0["Alder"], N1["Alder"], OBS["Alder"]) == (24, 6, 13))
check("on Alder's own curve its patients sit at 34% and 80% (34.3% and 79.6%)", (round(100 * a_lo, 1), round(100 * a_hi, 1)) == (34.3, 79.6), f"{100 * a_lo:.2f}%, {100 * a_hi:.2f}%")
check("those chances add up to 13, exactly what Alder observed: the fit balanced it", abs(expected("Alder", g_fit["Alder"]) - 13.0) < 1e-6, f"{expected('Alder', g_fit['Alder']):.6f}")
e_alder = expected("Alder", ref)
check("on the reference curve: 24 x 0.179 + 6 x 0.621 = 8.02 (blueprint)", round(e_alder, 2) == 8.02 and round(24 * round(p_lo, 3) + 6 * round(p_hi, 3), 2) == 8.02, f"{e_alder:.4f}")
check("13 over 8.02 is 1.62: 62% more than expected at the reference", round(OBS["Alder"] / e_alder, 2) == 1.62 and round(100 * (OBS["Alder"] / e_alder - 1)) == 62)
check("every fitted clinic's observed count is its expected count on its own curve", all(abs(expected(k, g_fit[k]) - OBS[k]) < 1e-6 for k in FINITE))

# ----------------------------------------------------------------------------- 3. all five (S05)
e_ref = {k: expected(k, ref) for k in ALL}
ratio = {k: OBS[k] / e_ref[k] for k in ALL}
check("expected at the reference: 8.02, 15.98, 8.00, 4.80 and 1.97 (blueprint)", fl([e_ref[k] for k in ALL], 2) == [8.02, 15.98, 8.0, 4.8, 1.97])
check("the ratios: 1.62, 0.88, 1.00, 1.46 and 0 (blueprint); Cedar's is exactly 1", fl([ratio[k] for k in ALL], 2) == [1.62, 0.88, 1.0, 1.46, 0.0] and abs(ratio["Cedar"] - 1.0) < 1e-6)
PK = LogisticFixedEffectModel().fit(pd.DataFrame({"clinic": np.array(ALL)[PROV], "x": X01, "y": Y}), y_var="y", x_vars=["x"], provider_var="clinic")
tab = PK.calculate_standardized_measures(stdz="indirect")["indirect"].set_index("provider_id")
check("pprof_py returns the same expected counts and ratios", all(abs(float(tab.loc[k, "expected"]) - e_ref[k]) < 1e-4 and abs(float(tab.loc[k, "indirect_ratio"]) - ratio[k]) < 1e-4 for k in ALL))
low_n, low_e = sum(N0.values()), sum(CAST[k][1] for k in ALL)
high_n, high_e = sum(N1.values()), sum(CAST[k][3] for k in ALL)
pooled = {k: OBS[k] / (N0[k] * low_e / low_n + N1[k] * high_e / high_n) for k in ALL}
check("Episode 3's pooled standard: 13 of 57 and 29 of 46; ratios 1.40, 0.85, 0.93, 1.36 and 0 (blueprint)",
      (low_e, low_n, high_e, high_n) == (13, 57, 29, 46) and fl([pooled[k] for k in ALL], 2) == [1.4, 0.85, 0.93, 1.36, 0.0])
rest_lo = (low_e - CAST["Alder"][1]) / (low_n - N0["Alder"]); rest_hi = (high_e - CAST["Alder"][3]) / (high_n - N1["Alder"])
alder_rest = OBS["Alder"] / (N0["Alder"] * rest_lo + N1["Alder"] * rest_hi)
check("Episode 3's second answer: against everyone but Alder, 1.8", round(alder_rest, 1) == 1.8, f"{alder_rest:.3f}")
check("so Alder's 1.62 lies between Episode 3's 1.4 and 1.8", pooled["Alder"] < ratio["Alder"] < alder_rest)
tot_ref, tot_pool = sum(e_ref.values()), sum(OBS[k] / pooled[k] if pooled[k] else N0[k] * low_e / low_n + N1[k] * high_e / high_n for k in ALL)
check("expected counts add up to 42 against the pooled standard, and to 38.8 against the middle clinic (blueprint)", abs(tot_pool - 42.0) < 1e-9 and round(tot_ref, 1) == 38.8 and sum(OBS.values()) == 42,
      f"{tot_pool:.3f}, {tot_ref:.3f}")

# ----------------------------------------------------------------------------- 4. as a rate (S06)
overall = sum(OBS.values()) / sum(SIZE.values())
rate = {k: 100 * ratio[k] * overall for k in ALL}
check("the overall readmission rate is 41% (42 of 103, 40.8%)", round(100 * overall, 1) == 40.8 and round(100 * overall) == 41)
check("as rates: 66%, 36%, 41%, 59% and 0% (blueprint), as pprof_py also reports", fl([rate[k] for k in ALL], 0) == [66.0, 36.0, 41.0, 59.0, 0.0]
      and all(abs(float(tab.loc[k, "indirect_rate"]) - rate[k]) < 1e-3 for k in ALL), str(fl([rate[k] for k in ALL], 2)))
check("no group of Alder's patients has a 66% chance: its own curve gives 34% and 80%", not (65.5 < 100 * a_lo < 66.5) and not (65.5 < 100 * a_hi < 66.5))

# ----------------------------------------------------------------------------- 5. ratio and gamma (S07)
curve_of = lambda g: expected("Alder", g) / e_alder
grid = np.linspace(-3.2, 1.2, 89)
curve = [float(curve_of(g)) for g in grid]
check("Alder's ratio is one rising curve in its gamma: 1 at the reference, 1.62 at its own", np.all(np.diff(curve) > 0) and abs(curve_of(ref) - 1.0) < 1e-12 and round(curve_of(g_fit["Alder"]), 2) == 1.62)
cat = {c["clinic"]: c for c in E9["caterpillar"]}
g_lo, g_hi = cat["Alder"]["low"], cat["Alder"]["high"]
r_lo, r_hi = curve_of(g_lo), curve_of(g_hi)
check("Episode 9's interval for Alder's gamma, -1.50 to 0.19, becomes 1.02 to 2.31 for its ratio (blueprint, Wald inversion)",
      (round(g_lo, 2), round(g_hi, 2)) == (-1.5, 0.19) and (round(r_lo, 2), round(r_hi, 2)) == (1.02, 2.31), f"{r_lo:.4f}, {r_hi:.4f}")
try:
    w = PK.calculate_confidence_intervals(option="SM", stdz="indirect", measure="ratio", test_method="wald")["indirect_ratio"].set_index("provider_id").loc["Alder"]
    pk_ci = (float(w["ci_ratio_lower"]), float(w["ci_ratio_upper"]))
except Exception as err:                                                       # pragma: no cover
    pk_ci = (float("nan"), float("nan"))
check("pprof_py's own Wald interval for Alder's ratio is the same", abs(pk_ci[0] - r_lo) < 1e-3 and abs(pk_ci[1] - r_hi) < 1e-3,
      f"{pk_ci[0]:.4f}, {pk_ci[1]:.4f}")

# ----------------------------------------------------------------------------- 6. two cautions and the crowd (S08)
mean_ref = E10["breaks"]["mean_reference"]["together"]
mean_ratio = {k: OBS[k] / expected(k, mean_ref) for k in FINITE}
check("against a size-weighted average (-1.75) the ratios become 1.87, 0.97, 1.12 and 1.63 (blueprint; Episode 10)",
      round(mean_ref, 2) == -1.75 and fl([mean_ratio[k] for k in FINITE], 2) == [1.87, 0.97, 1.12, 1.63] and abs(mean_ratio["Alder"] - E10["breaks"]["ratio"]["together"]["Alder"]) < 2e-4)
c = simulate()
F = joint_fit(c)
g0_c = float(np.median(F["gamma"]))
e_c = np.bincount(F["prov"], weights=expit(g0_c + F["X"] @ F["beta"]), minlength=len(F["gamma"]))
o_c = np.bincount(F["prov"], weights=F["y"], minlength=len(F["gamma"]))
r_c = o_c / e_c
check("the crowd: 200 ratios from 0.44 to 1.99 (blueprint), with their middle at 1", len(r_c) == 200 and (round(float(r_c.min()), 2), round(float(r_c.max()), 2)) == (0.44, 1.99)
      and abs(float(np.median(r_c)) - 1.0) < 0.02, f"{r_c.min():.3f} to {r_c.max():.3f}; median {np.median(r_c):.3f}")
sg = np.sort(F["gamma"]); mid = len(sg) // 2
check("in the crowd, one provider can move the middle value by at most 0.01", max(sg[mid] - sg[mid - 2], sg[mid + 1] - sg[mid - 1]) / 2 < 0.02 and (sg[mid + 1] - sg[mid - 2]) < 0.03,
      f"neighbouring middle values span {sg[mid + 1] - sg[mid - 2]:.4f}")
above = int(np.sum(r_c > 1.0))
check("about half the crowd's ratios are above 1 and half below, as a median reference implies", 90 <= above <= 110, f"{above} above")

OUT = {
    "episode": 11, "title": "Swap the Curve", "clinics": ALL, "fit": {"beta": beta, "gamma": g_fit}, "elm_printed": elm_printed,
    "reference": {"gamma": ref, "p_low": p_lo, "p_high": p_hi, "next_below": order[1], "next_above": order[3]},
    "cast": {k: {"low": N0[k], "high": N1[k], "observed": OBS[k], "size": SIZE[k]} for k in ALL},
    "alder": {"p_low": a_lo, "p_high": a_hi, "own_expected": expected("Alder", g_fit["Alder"]), "ref_expected": e_alder, "ratio": ratio["Alder"]},
    "expected": e_ref, "ratio": ratio, "pooled": pooled, "alder_rest": alder_rest, "totals": {"observed": sum(OBS.values()), "reference": tot_ref, "pooled": tot_pool},
    "overall": overall, "rate": rate,
    "link": {"grid": [float(v) for v in grid], "curve": curve, "gamma_interval": [g_lo, g_hi], "ratio_interval": [float(r_lo), float(r_hi)], "package_interval": list(pk_ci)},
    "mean_reference": {"gamma": mean_ref, "ratio": mean_ratio},
    "crowd": {"ratios": fl(np.sort(r_c), 4), "min": float(r_c.min()), "max": float(r_c.max()), "median": float(np.median(r_c)), "above": above, "reference": g0_c},
}

if __name__ == "__main__":
    print(f"reference {ref:.4f}: {100 * p_lo:.1f}% and {100 * p_hi:.1f}%")
    print("expected ", fl([e_ref[k] for k in ALL]), " sum", round(tot_ref, 2))
    print("ratio    ", fl([ratio[k] for k in ALL]), " pooled", fl([pooled[k] for k in ALL]), " Alder against the rest", round(alder_rest, 3))
    print("rate     ", fl([rate[k] for k in ALL], 1), " overall", round(100 * overall, 2))
    print(f"link      gamma {g_lo:.3f} to {g_hi:.3f} -> ratio {r_lo:.3f} to {r_hi:.3f}; package {pk_ci[0]:.3f} to {pk_ci[1]:.3f}")
    print(f"crowd     {r_c.min():.3f} to {r_c.max():.3f}, median {np.median(r_c):.3f}, {above} above 1; reference {g0_c:.3f}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e11_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
