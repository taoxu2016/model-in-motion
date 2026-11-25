"""Model in Motion · The Logistic Fixed-Effect Model · Episode 19: Wider than chance.

Every number the episode shows or says is computed here, checked, and written to e19_numbers.json.
Scenes and narration read e19_numbers.json; nothing numeric is typed into scene code or the script.

The fits, the exact tests and the empirical null are pprof_py's (LogisticFixedEffectModel, test, funnel_limits and
pprof_py.inference.EmpiricalNull); the exact test is also run with the series' own code and the two are compared.
The crowd is the series' own (seed 2026), with its knob for how much providers truly differ set to 0, 0.1, 0.2 and 0.3.

    python e19_numbers.py        # from this folder: prints the ledger, runs every check, writes e19_numbers.json  (about a minute)
"""
from __future__ import annotations

import json
import logging
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import coin_pmf, expit, mid_p  # noqa: E402
from mim.crowd import case_mix_se, joint_fit, simulate  # noqa: E402

warnings.simplefilter("ignore")
logging.disable(logging.CRITICAL)
import pandas as pd  # noqa: E402
from pprof_py import LogisticFixedEffectModel  # noqa: E402
from pprof_py.inference import EmpiricalNull  # noqa: E402

CHECKS: list[tuple[str, bool, str]] = []
fl = lambda a, k=3: [round(float(v), k) for v in a]
SEED, KNOB, GROUPS, M, Z95 = 2026, (0.0, 0.1, 0.2, 0.3), 3, 200, 1.959964
col = lambda T, name: T[name].reindex(range(M)).to_numpy()


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


def study(c, groups=GROUPS, funnel=False):
    """Fit one crowd with pprof_py and test every provider twice: against the standard null and against an empirical one."""
    df = pd.DataFrame({"prov": c["prov"], "x1": c["x1"], "x2": c["x2"], "y": c["y"]})
    model = LogisticFixedEffectModel().fit(df, y_var="y", x_vars=["x1", "x2"], provider_var="prov")
    n = np.asarray(c["n"])
    fitter = EmpiricalNull.fitter(size=n, n_groups=groups)
    T0, T1 = model.test(test_method="poibin_exact"), model.test(test_method="poibin_exact", null_model=fitter)
    planted = np.zeros(M, dtype=int)
    planted[list(c["planted_high"])] = 1; planted[list(c["planted_low"])] = -1
    out = {"n": n, "planted": planted, "z": col(T0, "z_raw").astype(float), "flag0": col(T0, "flag") != 0, "flag1": col(T1, "flag") != 0, "z_adj": col(T1, "z_adjusted").astype(float),
           "group": col(T1, "null_group").astype(int), "null_sd": col(T1, "null_sd").astype(float), "null_mean": col(T1, "null_mean").astype(float)}
    if funnel:
        F0, F1 = model.funnel_limits(test_method="score").providers, model.funnel_limits(test_method="score", null_model=fitter).providers
        T2 = model.test(test_method="score", null_model=fitter)                    # the funnel is the score test's picture, so its empirical null is fitted to the score test's z-values
        out.update({"score_sd": col(T2, "null_sd").astype(float), "score_mean": col(T2, "null_mean").astype(float), "precision": col(F0, "precision").astype(float), "ratio": col(F0, "estimate").astype(float), "lower0": col(F0, "lower").astype(float), "upper0": col(F0, "upper").astype(float),
                    "lower1": col(F1, "lower").astype(float), "upper1": col(F1, "upper").astype(float), "out0": col(F0, "flag") != 0, "out1": col(F1, "flag") != 0})
    return out


def own_exact(c):
    """The series' own exact test at the median reference (Episode 13), for comparison with the package's."""
    F = joint_fit(c)
    p0 = expit(float(np.median(F["gamma"])) + F["X"] @ F["beta"])
    starts = np.concatenate([[0], np.cumsum(c["n"])])
    obs = np.bincount(c["prov"], weights=c["y"], minlength=M)
    return np.array([mid_p(coin_pmf(p0[starts[i]:starts[i + 1]]), int(obs[i])) < 0.05 for i in range(M)]), case_mix_se(F)


# ----------------------------------------------------------------------------- 1. turn the knob (S03)
K = {}
for tau in KNOB:
    c = simulate(seed=SEED, tau=tau)
    K[tau] = study(c, funnel=(tau == KNOB[-1]))
    K[tau]["own"], K[tau]["se"] = own_exact(c)
ordinary = K[0.0]["planted"] == 0
check("the same 194 ordinary providers and six planted ones at every setting of the knob", int(ordinary.sum()) == 194 and all(np.array_equal(K[t]["planted"], K[0.0]["planted"]) and np.array_equal(K[t]["n"], K[0.0]["n"]) for t in KNOB))
check("pprof_py's exact test and the series' own flag the same providers at every setting", all(np.array_equal(K[t]["flag0"], K[t]["own"]) for t in KNOB))
flags = [int(K[t]["flag0"][ordinary].sum()) for t in KNOB]
check("flags among the 194 ordinary providers as the knob turns: 11, 16, 35, 48 (blueprint)", flags == [11, 16, 35, 48])
sds = [float(np.std(K[t]["z"][ordinary], ddof=1)) for t in KNOB]
check("the spread of their z-values: 0.95, 1.10, 1.40, 1.79 (blueprint)", all(abs(a - b) < 0.006 for a, b in zip(sds, (0.95, 1.10, 1.40, 1.79))), str(fl(sds)))
check("at the last setting a quarter of the ordinary providers are flagged, and 52 of all 200", round(flags[-1] / 194, 2) == 0.25 and int(K[0.3]["flag0"].sum()) == 52)
check("a knob setting of 0.3 means a typical provider's odds differ from the reference by roughly 30%: 35% above or 26% below", round(100 * (np.exp(0.3) - 1)) == 35 and round(100 * (1 - np.exp(-0.3))) == 26)

# ----------------------------------------------------------------------------- 2. the large ones go first (S04)
R = K[0.3]
n, large, small = R["n"], R["n"] >= 200, R["n"] < 50
share = lambda k: float(R["flag0"][ordinary & k].mean())
check("at 0.3, 40% of ordinary providers with 200 patients or more are flagged, against 7% of those under 50 (blueprint)", (round(100 * share(large)), round(100 * share(small))) == (40, 7),
      f"{share(large):.3f} of {int((ordinary & large).sum())}; {share(small):.3f} of {int((ordinary & small).sum())}")
sd_at = lambda s, tau=0.3: float(np.sqrt(1.0 + tau ** 2 / s ** 2))
check("a provider known to within 0.1 has a z with 3.2 times the spread chance alone gives, and is flagged 54% of the time (blueprint: 3.2, more than half)",
      round(sd_at(0.1), 1) == 3.2 and round(100 * 2 * norm.sf(Z95 / sd_at(0.1))) == 54, f"{sd_at(0.1):.3f}; {2 * norm.sf(Z95 / sd_at(0.1)):.3f}")

se_min = float(np.min(R["se"]))
check("no provider in the crowd is known quite that well: the largest, with 484 patients, has a standard error of 0.11", round(se_min, 2) == 0.11 and int(n[int(np.argmin(R["se"]))]) == 484, f"{se_min:.4f}")

# ----------------------------------------------------------------------------- 3. a null drawn from the providers (S06)
spreads = [float(R["null_sd"][R["group"] == g][0]) for g in (1, 2, 3)]
centres = [float(R["null_mean"][R["group"] == g][0]) for g in (1, 2, 3)]
bounds = [(int(n[R["group"] == g].min()), int(n[R["group"] == g].max()), int((R["group"] == g).sum())) for g in (1, 2, 3)]
check("three size groups of 67, 66 and 67 providers: 20 to 61 patients, 62 to 157, and 158 to 484", bounds == [(20, 61, 67), (62, 157, 66), (158, 484, 67)], str(bounds))
check("the fitted spreads of z in the three groups: 1.14, 1.60 and 2.18 (blueprint)", fl(spreads, 2) == [1.14, 1.60, 2.18], f"spreads {fl(spreads)}; centres {fl(centres)}")
predicted = [sd_at(float(np.median(R["se"][(R["group"] == g) & ordinary]))) for g in (1, 2, 3)]
check("those spreads are close to what the one-line formula gives for each group's typical precision: 1.2, 1.5 and 2.2, each within 0.1 of the fitted one",
      fl(predicted, 1) == [1.2, 1.5, 2.2] and all(abs(a - b) < 0.11 for a, b in zip(predicted, spreads)), str(fl(predicted)))
tally = lambda f: (int(f.sum()), int(f[ordinary].sum()), int(f[~ordinary].sum()))
check("judged against its own group's curve, 13 providers are flagged in place of 52: 10 ordinary and 3 planted, in place of 48 and 4 (blueprint)", tally(R["flag1"]) == (13, 10, 3) and tally(R["flag0"]) == (52, 48, 4))
i280 = [i for i in np.where(R["planted"] == 1)[0] if n[i] == 280][0]
check("for the provider of 280 patients the funnel's limits move from 0.76 and 1.24 out to 0.50 and 1.57 (blueprint)",
      (round(R["lower0"][i280], 2), round(R["upper0"][i280], 2), round(R["lower1"][i280], 2), round(R["upper1"][i280], 2)) == (0.76, 1.24, 0.50, 1.57))
f_spreads = [float(R["score_sd"][R["group"] == g][0]) for g in (1, 2, 3)]             # the funnel's own null: fitted to the score test's z-values
f_centres = [float(R["score_mean"][R["group"] == g][0]) for g in (1, 2, 3)]
lim = lambda p, g, sign: 1.0 + (f_centres[g - 1] + sign * Z95 * f_spreads[g - 1]) / np.sqrt(p)
gap = max(float(np.max(np.abs(lim(R["precision"][R["group"] == g], g, sign) - R[key][R["group"] == g]))) for g in (1, 2, 3) for sign, key in ((-1, "lower1"), (+1, "upper1")))
check("each group's widened limits are one formula: 1 plus (centre -+ 1.96 spreads) over the root of precision, with the score test's fitted centre and spread (1.15, 1.60, 2.21)",
      gap < 1e-6 and fl(f_spreads, 2) == [1.15, 1.60, 2.21], f"largest gap {gap:.1e}; spreads {fl(f_spreads)}; centres {fl(f_centres)}")
check("on the funnel, 49 ordinary providers lie outside the standard limits and 12 outside the widened ones", (int(R["out0"][ordinary].sum()), int(R["out1"][ordinary].sum())) == (49, 12))
REDRAWS = 20
r0, r1, s0, s1 = [], [], [], []
for j in range(REDRAWS):
    a = study(simulate(seed=4000 + 10 * j, tau=0.3))
    o = a["planted"] == 0
    r0.append(float(a["flag0"][o].mean())); r1.append(float(a["flag1"][o].mean()))
    b = study(simulate(seed=4000 + 10 * j, tau=0.0))
    s0.append(float(b["flag0"][o].mean())); s1.append(float(b["flag1"][o].mean()))
check("over twenty redraws at 0.3, the share of ordinary providers flagged falls from 23% to 5% (blueprint, on its own redraws: 24.4% to 5.7%)", (round(100 * np.mean(r0)), round(100 * np.mean(r1))) == (23, 5),
      f"{100 * np.mean(r0):.1f}%, {100 * np.mean(r1):.1f}%")

# ----------------------------------------------------------------------------- 4. what it costs (S07)
lost = [(("worse" if R["planted"][i] == 1 else "better"), int(n[i])) for i in np.where(R["planted"] != 0)[0] if R["flag0"][i] and not R["flag1"][i]]
check("of the six planted providers the standard test catches four and the empirical null three: the one lost is the better provider with 105 patients (blueprint: four and three)",
      int(R["flag0"][~ordinary].sum()) == 4 and int(R["flag1"][~ordinary].sum()) == 3 and lost == [("better", 105)])
Z0 = K[0.0]
spreads0 = [float(Z0["null_sd"][Z0["group"] == g][0]) for g in (1, 2, 3)]
check("with the knob at zero, this crowd's fitted curves come out too narrow (0.79, 0.82, 1.06) and flag 20 ordinary providers where the standard test flags 11",
      fl(spreads0, 2) == [0.79, 0.82, 1.06] and (int(Z0["flag1"][ordinary].sum()), int(Z0["flag0"][ordinary].sum())) == (20, 11), str(fl(spreads0)))
check("that is the fit's own luck: over twenty redraws at zero both tests flag about 4% to 5% of ordinary providers, and the empirical null's share varies more from crowd to crowd",
      3.5 < 100 * np.mean(s1) < 5.5 and 3.5 < 100 * np.mean(s0) < 5.5 and np.std(s1) > np.std(s0), f"standard {100 * np.mean(s0):.1f}% (sd {100 * np.std(s0, ddof=1):.1f}); empirical {100 * np.mean(s1):.1f}% (sd {100 * np.std(s1, ddof=1):.1f})")
one = study(simulate(seed=SEED, tau=0.3), groups=1)
check("one curve for all sizes would not do: its spread of 1.56 flags 22 ordinary providers and only 2 of the planted six", round(float(one["null_sd"][0]), 2) == 1.56 and tally(one["flag1"])[1:] == (22, 2))

edges = np.arange(-6.0, 6.0001, 0.5)
hist = lambda z: np.histogram(np.clip(z, -5.99, 5.99), bins=edges)[0].tolist()
OUT = {
    "episode": 19, "title": "Wider than Chance", "knob": list(KNOB), "ordinary": 194, "z95": Z95,
    "steps": [{"tau": t, "flags": f, "sd": s, "hist": hist(K[t]["z"][ordinary])} for t, f, s in zip(KNOB, flags, sds)], "edges": edges.tolist(),
    "all_flags": {"standard": tally(R["flag0"]), "empirical": tally(R["flag1"])}, "odds": {"above": float(np.exp(0.3) - 1), "below": float(1 - np.exp(-0.3))},
    "size": {"large": share(large), "small": share(small), "large_n": int((ordinary & large).sum()), "small_n": int((ordinary & small).sum()), "se": 0.1, "sd": sd_at(0.1), "flagged": float(2 * norm.sf(Z95 / sd_at(0.1))), "se_min": se_min, "se_small": float(np.median(R["se"][ordinary & small])),
             "large_flagged": int(R["flag0"][ordinary & large].sum()), "small_flagged": int(R["flag0"][ordinary & small].sum())},
    "null": {"spreads": spreads, "centres": centres, "bounds": bounds, "predicted": predicted, "redraws": REDRAWS, "standard_rate": float(np.mean(r0)), "empirical_rate": float(np.mean(r1)),
             "limits_280": [float(R["lower0"][i280]), float(R["upper0"][i280]), float(R["lower1"][i280]), float(R["upper1"][i280])], "precision_280": float(R["precision"][i280]),
             "groups_z": {str(g): hist(R["z"][(R["group"] == g) & ordinary]) for g in (1, 2, 3)}, "funnel_spreads": f_spreads, "funnel_centres": f_centres,
             "outside": [int(R["out0"][ordinary].sum()), int(R["out1"][ordinary].sum())]},
    "dots": [{"precision": float(R["precision"][i]), "ratio": float(R["ratio"][i]), "n": int(n[i]), "planted": int(R["planted"][i]), "group": int(R["group"][i]), "out0": bool(R["out0"][i]), "out1": bool(R["out1"][i]),
              "flag0": bool(R["flag0"][i]), "flag1": bool(R["flag1"][i])} for i in range(M)],
    "cost": {"planted": [{"kind": "worse" if R["planted"][i] == 1 else "better", "n": int(n[i]), "standard": bool(R["flag0"][i]), "empirical": bool(R["flag1"][i])} for i in np.where(R["planted"] != 0)[0]],
             "zero": {"spreads": spreads0, "empirical": int(Z0["flag1"][ordinary].sum()), "standard": int(Z0["flag0"][ordinary].sum()), "redraw_standard": float(np.mean(s0)), "redraw_empirical": float(np.mean(s1))},
             "one_group": {"spread": float(one["null_sd"][0]), "ordinary": tally(one["flag1"])[1], "planted": tally(one["flag1"])[2]}},
}

if __name__ == "__main__":
    print("knob      flags", flags, " spread of z", fl(sds))
    print(f"size      200 or more {share(large):.3f}; under 50 {share(small):.3f}; SE 0.1: sd {sd_at(0.1):.3f}, flagged {2 * norm.sf(Z95 / sd_at(0.1)):.3f}")
    print(f"null      spreads {fl(spreads)}; centres {fl(centres)}; formula {fl(predicted)}; flags {tally(R['flag1'])} against {tally(R['flag0'])}")
    print(f"redraws   at 0.3: {100 * np.mean(r0):.1f}% -> {100 * np.mean(r1):.1f}%; at 0: {100 * np.mean(s0):.1f}% and {100 * np.mean(s1):.1f}%")
    print(f"funnel    280 patients: {R['lower0'][i280]:.3f}, {R['upper0'][i280]:.3f} -> {R['lower1'][i280]:.3f}, {R['upper1'][i280]:.3f}; outside the funnel: {int(R['out0'][ordinary].sum())} then {int(R['out1'][ordinary].sum())} ordinary")
    print(f"cost      lost {lost}; at zero: spreads {fl(spreads0)}, flags {int(Z0['flag1'][ordinary].sum())} against {int(Z0['flag0'][ordinary].sum())}; one group: {OUT['cost']['one_group']}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e19_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
