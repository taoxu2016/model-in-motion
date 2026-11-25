"""Model in Motion · The Logistic Fixed-Effect Model · Episode 17: Fixed or random?

Every number the episode shows or says is computed here, checked, and written to e17_numbers.json.
Scenes and narration read e17_numbers.json; nothing numeric is typed into scene code or the script.

The random-effect fits are pprof_py's LogisticRandomEffectModel (a logistic model with normal random intercepts,
fitted lme4-style). The fixed-effect fits are the series' own. Truth is known because the crowd is simulated.

    python e17_numbers.py        # from this folder: prints the ledger, runs every check, writes e17_numbers.json
"""
from __future__ import annotations

import json
import logging
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, coin_pmf, expit, fit, mid_p, rows  # noqa: E402
from mim.crowd import case_mix_se, joint_fit, simulate  # noqa: E402

warnings.simplefilter("ignore")
logging.disable(logging.CRITICAL)
import pandas as pd  # noqa: E402
from pprof_py import LogisticRandomEffectModel  # noqa: E402

ALL = list(CAST)
CHECKS: list[tuple[str, bool, str]] = []
fl = lambda a, k=3: [round(float(v), k) for v in a]
about_median = lambda v: v - np.median(v)
rms = lambda e: float(np.sqrt(np.mean(np.asarray(e) ** 2)))


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


def both_fits(c):
    """Fit one crowd both ways and line the results up against its truth."""
    F = joint_fit(c)
    m, n, prov = len(c["n"]), c["n"], c["prov"]
    df = pd.DataFrame({"prov": prov, "x1": c["x1"], "x2": c["x2"], "y": c["y"]})
    R = LogisticRandomEffectModel(verbose=False).fit(df, y_var="y", x_vars=["x1", "x2"], provider_var="prov")
    blup = R.get_random_effects().reindex(range(m)).to_numpy(dtype=float)
    summ, test = R.summary(), R.test()
    planted = np.zeros(m, dtype=int)
    planted[list(c["planted_high"])] = 1; planted[list(c["planted_low"])] = -1
    starts = np.concatenate([[0], np.cumsum(n)])
    p0 = expit(float(np.median(F["gamma"])) + F["X"] @ F["beta"])
    obs = np.bincount(prov, weights=c["y"], minlength=m)
    fe_flag = np.array([mid_p(coin_pmf(p0[starts[i]:starts[i + 1]]), int(obs[i])) < 0.05 for i in range(m)])
    re_flag = test["flag"].reindex(range(m)).to_numpy() != 0
    fe, re, truth = about_median(F["gamma"]), about_median(float(summ.iloc[0]["Estimate"]) + blup), about_median(c["gamma"])
    return {"n": n, "mu": c["mu"], "planted": planted, "fe": fe, "re": re, "blup": blup, "truth": truth, "sigma": float(R.get_sigma()), "intercept": float(summ.iloc[0]["Estimate"]),
            "beta_fe": F["beta"], "beta_re": summ["Estimate"].to_numpy(dtype=float)[1:], "se": case_mix_se(F), "fe_flag": fe_flag, "re_flag": re_flag, "gamma_true": c["gamma"]}


# ----------------------------------------------------------------------------- 1. the cast, and Dune (S01, S03)
PROV, X01, Y = rows(ALL)
g_cast, b_cast, _, _ = fit(FINITE)
E09 = json.loads((HERE.parent / "e09_how_sure_are_we" / "e09_numbers.json").read_text())
se_cast = {d["clinic"]: d["se"] for d in E09["caterpillar"] if d["clinic"] in FINITE}       # Episode 9's standard errors, at the average case mix
check("Dune's estimate is -0.58, the highest of the cast, from 12 patients; Alder's is -0.65, from 30", max(g_cast, key=g_cast.get) == "Dune" and (round(g_cast["Dune"], 2), round(g_cast["Alder"], 2)) == (-0.58, -0.65)
      and (sum(CAST["Dune"][k] for k in (0, 2)), sum(CAST["Alder"][k] for k in (0, 2))) == (12, 30))

CR = both_fits(simulate(seed=2026))                                                # the series' crowd: providers differ a little, and sicker case mixes do truly better
sigma = CR["sigma"]
check("pprof_py's random-effect fit of the crowd puts the spread of provider effects at 0.33 (blueprint)", round(sigma, 2) == 0.33, f"{sigma:.4f}")
rel_dune = sigma ** 2 / (sigma ** 2 + se_cast["Dune"] ** 2)
check("with that spread and Dune's standard error of 0.66, Dune's reliability is 0.20: it keeps a fifth of its distance (blueprint)", round(se_cast["Dune"], 2) == 0.66 and round(rel_dune, 2) == 0.20, f"{rel_dune:.4f}")
centre = g_cast["Cedar"]                                                           # the series' reference for the cast: the median of the five, with Elm lowest
check("the centre used for the cast is its reference from Episode 11: Cedar's -1.52, the median of the five clinics", round(centre, 2) == -1.52 and sorted(g_cast.values())[1] == centre)


def shrunk(name):
    """A clinic's most likely effect if effects are draws from a bell curve at the cast's reference with the crowd's spread."""
    i = ALL.index(name)
    x, y = X01[PROV == i], Y[PROV == i]
    return float(brentq(lambda a: float(np.sum(y - expit(a + b_cast * x)) - (a - centre) / sigma ** 2), -12.0, 6.0))


S_cast = {k: shrunk(k) for k in ALL}
kept = {k: (S_cast[k] - centre) / (g_cast[k] - centre) for k in ("Alder", "Birch", "Dune")}
check("pulled that way, Dune moves from -0.58 to -1.33 and Alder from -0.65 to -1.18: the order flips", (round(S_cast["Dune"], 2), round(S_cast["Alder"], 2)) == (-1.33, -1.18) and S_cast["Alder"] > S_cast["Dune"],
      str({k: round(v, 3) for k, v in S_cast.items()}))
check("Dune keeps about a fifth of its distance from the centre, Alder two fifths", round(kept["Dune"], 1) == 0.2 and round(kept["Alder"], 2) == 0.40, str({k: round(v, 3) for k, v in kept.items()}))
check("Elm, which has no fixed-effect estimate, gets a finite one: -1.71", round(S_cast["Elm"], 2) == -1.71 and np.isfinite(S_cast["Elm"]))
df_cast = pd.DataFrame({"clinic": np.array(ALL)[PROV], "x": X01, "y": Y})
RC = LogisticRandomEffectModel(verbose=False).fit(df_cast, y_var="y", x_vars=["x"], provider_var="clinic")
pk = (float(RC.summary().iloc[0]["Estimate"]) + RC.get_random_effects()).to_dict()
check("pprof_py's own random-effect fit of the five clinics agrees on both points: Alder above Dune, and a finite estimate for Elm (-1.65)",
      pk["Alder"] > pk["Dune"] and round(pk["Elm"], 2) == -1.65, f"sigma {float(RC.get_sigma()):.3f}; " + str({k: round(v, 3) for k, v in pk.items()}))

# ----------------------------------------------------------------------------- 2. the pull, in the crowd (S04)
n, small, large = CR["n"], CR["n"] < 50, CR["n"] > 200
rel = sigma ** 2 / (sigma ** 2 + CR["se"] ** 2)
check("a typical reliability is 0.37 under 50 patients and 0.83 above 200 (blueprint)", (round(float(np.median(rel[small])), 2), round(float(np.median(rel[large])), 2)) == (0.37, 0.83),
      f"{np.median(rel[small]):.4f} over {int(small.sum())} providers; {np.median(rel[large]):.4f} over {int(large.sum())}")
moved = np.abs(CR["fe"] - CR["re"])
check("small providers move most: 0.26 on average under 50 patients, against 0.05 or 0.06 above 200", round(float(moved[small].mean()), 2) == 0.26 and 0.05 < float(moved[large].mean()) < 0.06,
      f"{moved[small].mean():.4f}, {moved[large].mean():.4f}")
approx = rel * CR["fe"]
check("reliability times the fixed-effect estimate reproduces the package's random effects: correlation 0.999", round(float(np.corrcoef(approx, CR["blup"])[0, 1]), 3) == 0.999)
sd = lambda v: float(np.std(v, ddof=1))
check("the spread of the estimates falls from 0.44 to 0.26, either side of the true 0.33 (blueprint: 0.44 and 0.26)", (round(sd(CR["fe"]), 2), round(sd(CR["re"]), 2), round(sd(CR["truth"]), 2)) == (0.44, 0.26, 0.33))

# ----------------------------------------------------------------------------- 3. what it buys (S05)
e_fe, e_re = CR["fe"] - CR["truth"], CR["re"] - CR["truth"]                        # errors in a provider's position about the median
check("the typical error falls from 0.28 to 0.20 (blueprint: 0.280 and 0.196)", (round(rms(e_fe), 2), round(rms(e_re), 2)) == (0.28, 0.20), f"{rms(e_fe):.4f}, {rms(e_re):.4f}")
check("for providers under 50 patients it falls from 0.40 to 0.25 (blueprint: 0.403 and 0.250)", (round(rms(e_fe[small]), 2), round(rms(e_re[small]), 2)) == (0.40, 0.25), f"{rms(e_fe[small]):.4f}, {rms(e_re[small]):.4f}")
check("above 200 patients the two are nearly level: 0.15 and 0.13", (round(rms(e_fe[large]), 2), round(rms(e_re[large]), 2)) == (0.15, 0.13), f"{rms(e_fe[large]):.4f}, {rms(e_re[large]):.4f}")

# ----------------------------------------------------------------------------- 4. what it costs: the outliers (S06)
pl = CR["planted"] != 0
check("the six planted providers truly sit 0.8 from the centre; fixed effects put them at 0.67 on average, random effects at 0.46 (blueprint)",
      (round(float(np.abs(CR["fe"][pl]).mean()), 2), round(float(np.abs(CR["blup"][pl]).mean()), 2)) == (0.67, 0.46), f"{np.abs(CR['fe'][pl]).mean():.3f}, {np.abs(CR['blup'][pl]).mean():.3f}")
check("fixed effects flag four of the six, random effects three (blueprint)", (int(CR["fe_flag"][pl].sum()), int(CR["re_flag"][pl].sum())) == (4, 3))
check("among the 194 ordinary providers, fixed effects flag 48 and random effects 39", (int(CR["fe_flag"][~pl].sum()), int(CR["re_flag"][~pl].sum())) == (48, 39))

# ----------------------------------------------------------------------------- 5. what it costs: the case mix (S07)
link = float(np.corrcoef(CR["gamma_true"], CR["mu"])[0, 1])
check("in this crowd, providers with sicker patients truly do better: effect and case mix correlate -0.50", round(link, 2) == -0.50, f"{link:.3f}")
c_fe, c_re = float(np.corrcoef(e_fe, CR["mu"])[0, 1]), float(np.corrcoef(e_re, CR["mu"])[0, 1])
check("random-effect errors correlate 0.35 with case mix, fixed-effect errors 0.06 (blueprint: 0.35 and 0.07)", (round(c_re, 2), round(c_fe, 2)) == (0.35, 0.06), f"{c_re:.4f}, {c_fe:.4f}")
by_mix = np.argsort(CR["mu"])
healthy, sick = by_mix[:40], by_mix[-40:]
tilt = lambda e, g: float(np.mean(e[g]) - np.mean(e))
check("the sickest fifth look 0.10 worse than they are under random effects, the healthiest fifth 0.10 better (blueprint)", (round(tilt(e_re, sick), 2), round(tilt(e_re, healthy), 2)) == (0.10, -0.10),
      f"{tilt(e_re, sick):+.3f}, {tilt(e_re, healthy):+.3f}; fixed effects {tilt(e_fe, sick):+.3f}, {tilt(e_fe, healthy):+.3f}")
check("part of that comes through the risk rule: the random-effect fit puts 0.78 on the first risk factor, the fixed-effect fit 0.81, and the truth is 0.80",
      (round(float(CR["beta_re"][0]), 2), round(float(CR["beta_fe"][0]), 2)) == (0.78, 0.81))
NL = both_fits(simulate(seed=2026, rho=0.0))                                       # the same crowd with the link between effect and case mix broken
n_fe, n_re = NL["fe"] - NL["truth"], NL["re"] - NL["truth"]
c_nl = float(np.corrcoef(n_re, NL["mu"])[0, 1])
check("break the link and the random-effect correlation vanishes: -0.01 (blueprint, on its own draws: 0.06)", round(c_nl, 2) == -0.01 and abs(float(np.corrcoef(NL["gamma_true"], NL["mu"])[0, 1])) < 0.05, f"{c_nl:.3f}")
check("without the link the fixed-effect correlation is 0.10: about what chance gives among 200 providers", round(float(np.corrcoef(n_fe, NL["mu"])[0, 1]), 2) == 0.10)
check("without the link, random effects still cut the typical error, from 0.30 to 0.20", (round(rms(n_fe), 2), round(rms(n_re), 2)) == (0.30, 0.20), f"{rms(n_fe):.4f}, {rms(n_re):.4f}")

rows_out = lambda R: [{"n": int(R["n"][i]), "fe": float(R["fe"][i]), "re": float(R["re"][i]), "truth": float(R["truth"][i]), "planted": int(R["planted"][i]), "mu": float(R["mu"][i]),
                       "fe_flag": bool(R["fe_flag"][i]), "re_flag": bool(R["re_flag"][i])} for i in range(len(R["n"]))]
OUT = {
    "episode": 17, "title": "Fixed or Random?", "clinics": ALL, "sigma": sigma,
    "cast": {"fixed": g_cast, "se": se_cast, "centre": centre, "shrunk": S_cast, "kept": kept, "reliability_dune": rel_dune, "patients": {k: CAST[k][0] + CAST[k][2] for k in ALL}, "package": pk},
    "crowd": {"providers": rows_out(CR), "reliability": {"small": float(np.median(rel[small])), "large": float(np.median(rel[large]))}, "moved": {"small": float(moved[small].mean()), "large": float(moved[large].mean())},
              "sd": {"fixed": sd(CR["fe"]), "random": sd(CR["re"]), "truth": sd(CR["truth"])},
              "error": {"fixed": rms(e_fe), "random": rms(e_re), "fixed_small": rms(e_fe[small]), "random_small": rms(e_re[small]), "fixed_large": rms(e_fe[large]), "random_large": rms(e_re[large])},
              "planted": {"truth": 0.8, "fixed": float(np.abs(CR["fe"][pl]).mean()), "random": float(np.abs(CR["blup"][pl]).mean()), "fixed_flags": int(CR["fe_flag"][pl].sum()), "random_flags": int(CR["re_flag"][pl].sum())},
              "link": link, "corr": {"fixed": c_fe, "random": c_re}, "fifths": {"sick": tilt(e_re, sick), "healthy": tilt(e_re, healthy), "sick_fixed": tilt(e_fe, sick), "healthy_fixed": tilt(e_fe, healthy)},
              "beta": {"fixed": float(CR["beta_fe"][0]), "random": float(CR["beta_re"][0])}},
    "no_link": {"providers": rows_out(NL), "corr": {"fixed": float(np.corrcoef(n_fe, NL["mu"])[0, 1]), "random": c_nl}, "error": {"fixed": rms(n_fe), "random": rms(n_re)}},
}

if __name__ == "__main__":
    print("cast      fixed", {k: round(v, 3) for k, v in g_cast.items()}, "| pulled", {k: round(v, 3) for k, v in S_cast.items()}, "| kept", {k: round(v, 2) for k, v in kept.items()})
    print("package  ", {k: round(v, 3) for k, v in pk.items()}, f"(sigma {float(RC.get_sigma()):.3f})")
    print(f"crowd     sigma {sigma:.4f}; reliability {np.median(rel[small]):.3f}, {np.median(rel[large]):.3f}; spread {sd(CR['fe']):.3f} -> {sd(CR['re']):.3f} (truth {sd(CR['truth']):.3f})")
    print(f"error     {rms(e_fe):.3f} -> {rms(e_re):.3f}; small {rms(e_fe[small]):.3f} -> {rms(e_re[small]):.3f}; large {rms(e_fe[large]):.3f} -> {rms(e_re[large]):.3f}")
    print(f"planted   fixed {np.abs(CR['fe'][pl]).mean():.3f}, random {np.abs(CR['blup'][pl]).mean():.3f}; flags {int(CR['fe_flag'][pl].sum())} and {int(CR['re_flag'][pl].sum())}; ordinary flags {int(CR['fe_flag'][~pl].sum())} and {int(CR['re_flag'][~pl].sum())}")
    print(f"case mix  link {link:.3f}; error correlation random {c_re:.3f}, fixed {c_fe:.3f}; fifths {tilt(e_re, sick):+.3f}, {tilt(e_re, healthy):+.3f}; no link {c_nl:.3f}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e17_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
