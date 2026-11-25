"""Model in Motion · The Logistic Fixed-Effect Model · Episode 12: Swap the patients.

Every number the episode shows or says is computed here, checked, and written to e12_numbers.json.
Scenes and narration read e12_numbers.json; nothing numeric is typed into scene code or the script.

    python e12_numbers.py        # from this folder: prints the ledger, runs every check, writes e12_numbers.json
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
E10 = json.loads((HERE.parent / "e10_no_events_no_peak" / "e10_numbers.json").read_text())
E11 = json.loads((HERE.parent / "e11_swap_the_curve" / "e11_numbers.json").read_text())
gam = {**g_fit, "Elm": E10["printed"]["together"]}
ref = E11["reference"]["gamma"]
N0 = {k: CAST[k][0] for k in ALL}; N1 = {k: CAST[k][2] for k in ALL}
OBS = {k: CAST[k][1] + CAST[k][3] for k in ALL}
pop0, pop1, total_obs = sum(N0.values()), sum(N1.values()), sum(OBS.values())
P = lambda g: (float(expit(g)), float(expit(g + beta)))                        # a curve's two heights: lower-risk, higher-risk
count = lambda g, n0, n1: n0 * P(g)[0] + n1 * P(g)[1]                           # expected readmissions for a set of patients on a curve
own = {k: P(gam[k]) for k in ALL}
at_ref = P(ref)

# ----------------------------------------------------------------------------- 1. the puzzle (S01, S03)
check("last time's ratios: Alder 1.62, Dune 1.46", (round(E11["ratio"]["Alder"], 2), round(E11["ratio"]["Dune"], 2)) == (1.62, 1.46))
check("Dune's curve is the higher one: its slider is at -0.58 against Alder's -0.65, so its chance is greater at every level of risk",
      g_fit["Dune"] > g_fit["Alder"] and (round(g_fit["Dune"], 2), round(g_fit["Alder"], 2)) == (-0.58, -0.65) and own["Dune"][0] > own["Alder"][0] and own["Dune"][1] > own["Alder"][1])
check("lower-risk patients: 18% at the reference, 34% at Alder, 36% at Dune", [round(100 * v) for v in (at_ref[0], own["Alder"][0], own["Dune"][0])] == [18, 34, 36],
      f"{100 * at_ref[0]:.1f}, {100 * own['Alder'][0]:.1f}, {100 * own['Dune'][0]:.1f}")
check("higher-risk patients: 62% at the reference, 80% at Alder, 81% at Dune", [round(100 * v) for v in (at_ref[1], own["Alder"][1], own["Dune"][1])] == [62, 80, 81],
      f"{100 * at_ref[1]:.1f}, {100 * own['Alder'][1]:.1f}, {100 * own['Dune'][1]:.1f}")
mult = {k: (own[k][0] / at_ref[0], own[k][1] / at_ref[1]) for k in ("Alder", "Dune")}
check("as multiples of the reference: close to double for lower-risk patients (1.9 and 2.0), about 1.3 for higher-risk (1.28 and 1.30)",
      fl(mult["Alder"], 2) == [1.91, 1.28] and fl(mult["Dune"], 2) == [2.0, 1.3], f"Alder {fl(mult['Alder'])}, Dune {fl(mult['Dune'])}")
check("Dune's multiple is the larger at both levels, yet Alder's ratio is the larger overall", mult["Dune"][0] > mult["Alder"][0] and mult["Dune"][1] > mult["Alder"][1] and E11["ratio"]["Alder"] > E11["ratio"]["Dune"])
check("who each clinic treats: 24 of Alder's 30 are lower-risk; Dune's 12 are split evenly", (N0["Alder"], N1["Alder"], N0["Dune"], N1["Dune"]) == (24, 6, 6, 6))
share = {k: N0[k] * at_ref[0] / count(ref, N0[k], N1[k]) for k in ("Alder", "Dune")}
mix_ratio = {k: share[k] * mult[k][0] + (1 - share[k]) * mult[k][1] for k in ("Alder", "Dune")}
check("each ratio is its two multiples averaged by where the expected count comes from: 54% lower-risk for Alder, 22% for Dune",
      (round(100 * share["Alder"]), round(100 * share["Dune"])) == (54, 22) and all(abs(mix_ratio[k] - E11["ratio"][k]) < 1e-9 for k in mix_ratio), f"{share['Alder']:.3f}, {share['Dune']:.3f}")
dune_as_alder = count(gam["Dune"], N0["Alder"], N1["Alder"]) / count(ref, N0["Alder"], N1["Alder"])
alder_as_dune = count(gam["Alder"], N0["Dune"], N1["Dune"]) / count(ref, N0["Dune"], N1["Dune"])
check("give Dune Alder's patients and its ratio would be 1.68, above Alder's 1.62; give Alder Dune's and it would be 1.42, below Dune's 1.46",
      (round(dune_as_alder, 2), round(alder_as_dune, 2)) == (1.68, 1.42), f"{dune_as_alder:.4f}, {alder_as_dune:.4f}")

# ----------------------------------------------------------------------------- 2. swap the patients (S04)
check("everyone: 103 patients, 57 lower-risk and 46 higher-risk, 42 readmissions", (pop0 + pop1, pop0, pop1, total_obs) == (103, 57, 46, 42))
direct = {k: count(gam[k], pop0, pop1) for k in ALL}
check("under Alder's curve: 57 x 0.343 + 46 x 0.796 = 56.2 (blueprint)", round(direct["Alder"], 1) == 56.2 and round(57 * round(own["Alder"][0], 3) + 46 * round(own["Alder"][1], 3), 1) == 56.2,
      f"{direct['Alder']:.3f}")
rate = {k: 100 * direct[k] / (pop0 + pop1) for k in ALL}
dsr = {k: direct[k] / total_obs for k in ALL}
check("56.2 out of 103 is 54.5%; against the 42 observed, a ratio of 1.34 (blueprint)", round(rate["Alder"], 1) == 54.5 and round(dsr["Alder"], 2) == 1.34, f"{rate['Alder']:.2f}%, {dsr['Alder']:.4f}")

# ----------------------------------------------------------------------------- 3. the same patients, at every clinic (S05)
check("direct rates: 54.5%, 32.2%, 37.6%, 55.9%, and 0.7% for Elm (blueprint)", fl([rate[k] for k in ALL], 1) == [54.5, 32.2, 37.6, 55.9, 0.7], str(fl([rate[k] for k in ALL], 2)))
PK = LogisticFixedEffectModel().fit(pd.DataFrame({"clinic": np.array(ALL)[PROV], "x": X01, "y": Y}), y_var="y", x_vars=["x"], provider_var="clinic")
tab = PK.calculate_standardized_measures(stdz="direct")["direct"].set_index("provider_id")
check("pprof_py returns the same expected counts, ratios and rates", all(abs(float(tab.loc[k, "expected"]) - direct[k]) < 1e-3 and abs(float(tab.loc[k, "direct_ratio"]) - dsr[k]) < 1e-4
                                                                     and abs(float(tab.loc[k, "direct_rate"]) - rate[k]) < 1e-3 for k in ALL))
by_gamma = sorted(ALL, key=lambda k: -gam[k]); by_rate = sorted(ALL, key=lambda k: -rate[k]); by_ratio = sorted(ALL, key=lambda k: -E11["ratio"][k])
check("on the same patients the order of the rates is the order of the curves: Dune, Alder, Cedar, Birch, Elm", by_rate == by_gamma == ["Dune", "Alder", "Cedar", "Birch", "Elm"])
check("the swap of places: last time's ratio put Alder first and Dune second", by_ratio[:2] == ["Alder", "Dune"] and by_rate[:2] == ["Dune", "Alder"])
check("Elm's 0.7% moves with its printed gamma: 0.74% after one routine, 0.004% after the other (Episode 10)",
      abs(rate["Elm"] - E10["breaks"]["direct_rate"]["together"]) < 1e-6 and round(E10["breaks"]["direct_rate"]["turns"], 3) == 0.004)
overall = 100 * total_obs / (pop0 + pop1)
check("the overall rate is 41% (40.8%), but the reference clinic's own direct rate is 37.6%, a ratio of 0.92 and not 1 (blueprint)",
      round(overall, 1) == 40.8 and round(rate["Cedar"], 1) == 37.6 and round(dsr["Cedar"], 2) == 0.92)
check("everyone at the reference would have 38.8 readmissions: the same 38.8 the expected counts added up to last time",
      round(direct["Cedar"], 1) == 38.8 and abs(direct["Cedar"] - E11["totals"]["reference"]) < 1e-9, f"{direct['Cedar']:.4f}")
vs_ref = {k: direct[k] / direct["Cedar"] for k in ALL}
check("against the reference clinic's 37.6%, Alder's 54.5% is 1.45 times as high; last time's ratio said 1.62", round(vs_ref["Alder"], 2) == 1.45 and round(rate["Alder"] / rate["Cedar"], 2) == 1.45,
      f"{vs_ref['Alder']:.4f}; Dune {vs_ref['Dune']:.4f}")
gap_direct = float(logit(rate["Alder"] / 100) - logit(rate["Cedar"] / 100))
check("for the record: these are Episode 5's 55% and 38%, 0.69 apart on the log-odds ruler against 0.87 within the model (blueprint)",
      (round(rate["Alder"]), round(rate["Cedar"])) == (55, 38) and round(gap_direct, 2) == 0.69 and round(g_fit["Alder"] - g_fit["Cedar"], 2) == 0.87, f"{gap_direct:.4f}")

# ----------------------------------------------------------------------------- 4. the price (S07)
from_high = {k: pop1 * own[k][1] / direct[k] for k in ALL}
check("Alder treated 6 higher-risk patients; its direct count asks about 46, and they supply two-thirds of the 56.2 (36.6, or 65%)",
      N1["Alder"] == 6 and round(pop1 * own["Alder"][1], 1) == 36.6 and round(100 * from_high["Alder"]) == 65, f"{pop1 * own['Alder'][1]:.2f}, {100 * from_high['Alder']:.1f}%")
check("Elm treated no higher-risk patients, yet they supply 86% of its direct count", N1["Elm"] == 0 and round(100 * from_high["Elm"]) == 86, f"{100 * from_high['Elm']:.1f}%")
asked = {k: {"treated": [N0[k], N1[k]], "asked": [pop0, pop1]} for k in ALL}

# ----------------------------------------------------------------------------- 5. in the crowd (S08)
c = simulate(); F = joint_fit(c)
g, lin, prov, y = F["gamma"], F["X"] @ F["beta"], F["prov"], F["y"]
g0 = float(np.median(g))
isr = np.bincount(prov, weights=y, minlength=len(g)) / np.bincount(prov, weights=expit(g0 + lin), minlength=len(g))
dsr_c = np.array([float(expit(gi + lin).sum()) for gi in g]) / float(y.sum())
rank = lambda v: np.argsort(np.argsort(-v)) + 1                                 # 1 = highest
move = np.abs(rank(isr) - rank(dsr_c))
corr = float(np.corrcoef(isr, dsr_c)[0, 1])
check("the crowd: the two ratios correlate 0.99 (blueprint: 0.991)", abs(corr - 0.991) < 5e-4, f"{corr:.4f}")
check("yet between the two rankings four providers move ten places or more, the largest move being 14 (blueprint)", int((move >= 10).sum()) == 4 and int(move.max()) == 14,
      f"{int((move >= 10).sum())} providers; largest {int(move.max())}")
check("in the crowd too, the direct ranking is exactly the ranking of the gammas", np.array_equal(rank(dsr_c), rank(g)))
check("for the record: half the crowd keeps its place to within two", int((move <= 2).sum()) >= 100, f"{int((move <= 2).sum())} of 200 move two places or fewer")

OUT = {
    "episode": 12, "title": "Swap the Patients", "clinics": ALL, "fit": {"beta": beta, "gamma": g_fit}, "elm_printed": gam["Elm"],
    "reference": {"gamma": ref, "p": list(at_ref)}, "own": {k: list(own[k]) for k in ALL}, "multiple": {k: list(mult[k]) for k in mult},
    "cast": {k: {"low": N0[k], "high": N1[k], "observed": OBS[k]} for k in ALL}, "everyone": {"low": pop0, "high": pop1, "total": pop0 + pop1, "observed": total_obs, "rate": overall},
    "indirect": {k: E11["ratio"][k] for k in ALL}, "share_low": share, "swapped": {"dune_with_alders": dune_as_alder, "alder_with_dunes": alder_as_dune},
    "direct": {"expected": direct, "rate": rate, "ratio": dsr, "against_reference": vs_ref, "parts": {k: [pop0 * own[k][0], pop1 * own[k][1]] for k in ALL}, "from_high": from_high},
    "asked": asked, "episode5": {"gap_direct": gap_direct, "gap_model": g_fit["Alder"] - g_fit["Cedar"]},
    "crowd": {"isr": fl(isr, 4), "dsr": fl(dsr_c, 4), "move": [int(v) for v in move], "corr": corr, "movers": int((move >= 10).sum()), "largest": int(move.max())},
}

if __name__ == "__main__":
    print("own curves     ", {k: fl(own[k]) for k in ALL}, " reference", fl(at_ref))
    print("multiples      ", {k: fl(mult[k]) for k in mult}, " share from lower-risk", {k: round(v, 3) for k, v in share.items()})
    print("direct expected", fl([direct[k] for k in ALL], 2), " rates", fl([rate[k] for k in ALL], 2), " ratios", fl([dsr[k] for k in ALL]))
    print("against Cedar  ", fl([vs_ref[k] for k in ALL]), " from higher-risk", fl([from_high[k] for k in ALL]))
    print(f"crowd           correlation {corr:.4f}; {int((move >= 10).sum())} move ten or more; largest {int(move.max())}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e12_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
