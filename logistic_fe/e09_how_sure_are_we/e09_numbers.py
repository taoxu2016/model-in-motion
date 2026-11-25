"""Model in Motion · The Logistic Fixed-Effect Model · Episode 9: How sure are we?

Every number the episode shows or says is computed here, checked, and written to e09_numbers.json.
Scenes and narration read e09_numbers.json; nothing numeric is typed into scene code or the script.

    python e09_numbers.py        # from this folder: prints the ledger, runs every check, writes e09_numbers.json
"""
from __future__ import annotations

import json
import sys
import warnings
from math import erfc, sqrt
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, expit, fit, logit, rows  # noqa: E402

ALL = list(CAST)
M = len(ALL)
PROV, X01, Y = rows(ALL)
CHECKS: list[tuple[str, bool, str]] = []
fl = lambda a, k=3: [round(float(v), k) for v in a]
p_chi1 = lambda q: erfc(sqrt(q / 2.0))                  # upper tail of chi-square with 1 degree of freedom


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


g_fit, beta, cov4, ll_fit = fit()
E6 = json.loads((HERE.parent / "e06_fitting_by_balance" / "e06_numbers.json").read_text())
E8 = json.loads((HERE.parent / "e08_the_arrow_matrix" / "e08_numbers.json").read_text())
gam = np.array([g_fit[k] for k in FINITE] + [E8["table"]["elm_gamma"]])       # Elm where the package's fit left its slider


def pieces(gam, beta, x):
    p = expit(gam[PROV] + x * beta)
    w = p * (1 - p)
    V = np.bincount(PROV, weights=w, minlength=M)                              # each clinic's own wobble
    B = np.bincount(PROV, weights=w * x, minlength=M)
    S = float((x * x) @ w) - float((B * B / V).sum())                          # the folded number
    return V, B / V, S                                                         # wobble, each clinic's weighted mean of x, S


V, xb, S = pieces(gam, beta, X01)
se_beta = 1.0 / np.sqrt(S)

# ----------------------------------------------------------------------------- 1. the dial (S03)
check("the folded number is Episode 8's 2.93; the dial's standard error is 0.58 (blueprint: 0.585)", abs(S - E8["fold"]["S"]) < 1e-9 and round(se_beta, 2) == 0.58 and abs(se_beta - 0.585) < 1e-3,
      f"S {S:.4f}, SE {se_beta:.4f}")
check("it equals the dial's standard error from inverting the whole table of the four fitted clinics", abs(se_beta - float(np.sqrt(cov4[-1, -1]))) < 1e-9)
lo, hi = beta - 1.959964 * se_beta, beta + 1.959964 * se_beta
check("95% interval for the dial: 0.87 to 3.16; as an odds ratio, 2.4 to 23.6 around 7.5 (blueprint)",
      (round(lo, 2), round(hi, 2)) == (0.87, 3.16) and (round(float(np.exp(lo)), 1), round(float(np.exp(hi)), 1), round(float(np.exp(beta)), 1)) == (2.4, 23.6, 7.5),
      f"{lo:.3f} to {hi:.3f}; {np.exp(lo):.2f} to {np.exp(hi):.2f}")
HILL = E6["hill"]
drop = {round(b, 1): HILL["peak"] - h for b, h in HILL["profile"]}
par = {b: 0.5 * S * (b - beta) ** 2 for b in (1.5, 2.5, 3.0)}
check("near its top the hill is the parabola with curvature 2.93 (within 0.05 half a unit either side)",
      abs(drop[1.5] - par[1.5]) < 0.05 and abs(drop[2.5] - par[2.5]) < 0.05, f"hill {drop[1.5]:.3f}, {drop[2.5]:.3f}; parabola {par[1.5]:.3f}, {par[2.5]:.3f}")

# ----------------------------------------------------------------------------- 2. is the step there at all? (S04)
wald = (beta / se_beta) ** 2
lr = 2.0 * (ll_fit - HILL["at_zero"])
g_null = np.array([float(logit((CAST[k][1] + CAST[k][3]) / (CAST[k][0] + CAST[k][2]))) for k in FINITE] + [-30.0])     # beta = 0: each clinic at its own rate
V0, xb0, S0 = pieces(g_null, 0.0, X01)
U0 = float(X01 @ (Y - expit(g_null[PROV])))
score = U0 ** 2 / S0
check("three ways of asking whether the step is zero: 11.90 across, 14.55 down, 13.78 from the slope at zero (blueprint)",
      (round(wald, 2), round(lr, 2), round(score, 2)) == (11.9, 14.55, 13.78), f"{wald:.3f}, {lr:.3f}, {score:.3f}")
check("all three put the chance of such a step arising with no real effect below 1 in 1,000", max(p_chi1(wald), p_chi1(lr), p_chi1(score)) < 0.001,
      f"{p_chi1(wald):.5f}, {p_chi1(lr):.5f}, {p_chi1(score):.5f}")
check("zero is about three and a half standard errors from the top, and the hill is 7.3 lower there", abs(beta / se_beta - 3.5) < 0.06 and round(lr / 2, 1) == 7.3,
      f"{beta / se_beta:.3f}, {lr / 2:.3f}")
mh_num, mh_var = 0.0, 0.0
for k in FINITE:                                                              # Mantel-Haenszel across clinics, for the record (not narrated)
    n0, e0, n1, e1 = CAST[k]
    n, e = n0 + n1, e0 + e1
    mh_num += e1 - n1 * e / n
    mh_var += n1 * n0 * e * (n - e) / (n * n * (n - 1))
mh = mh_num ** 2 / mh_var
check("for the record: the Mantel-Haenszel statistic across clinics is 13.14 (blueprint)", round(mh, 2) == 13.14, f"{mh:.3f}")

# ----------------------------------------------------------------------------- 3. one clinic (S05)
own = 1.0 / np.sqrt(V)
check("a clinic's own standard error is 1 over the root of its wobble: Alder 0.40, Birch 0.39, Cedar 0.51, Dune 0.66 (blueprint: 0.396, 0.658)",
      fl(own[:4], 2) == [0.4, 0.39, 0.51, 0.66] and abs(own[0] - 0.396) < 1e-3 and abs(own[3] - 0.658) < 1e-3, str(fl(own[:4])))
heads = [CAST[k][0] + CAST[k][2] for k in ALL]
check("information is not head count: Elm's 11 patients carry 0.02, Dune's 12 carry 2.31", heads[4] == 11 and heads[3] == 12 and fl(V, 2)[3:] == [2.31, 0.02])
rare = 100 * 0.02 * 0.98
check("a hundred patients at 2% carry less than Dune's twelve (1.96 against 2.31)", round(rare, 2) == 1.96 and rare < V[3])

# ----------------------------------------------------------------------------- 4. the dial's share (S06)
def se_at(shift, at):
    """Standard error of gamma_i + at * beta when the risk factor is recorded `shift` units higher."""
    Vs, xbs, Ss = pieces(gam - shift * beta, beta, X01 + shift)
    return np.sqrt(1.0 / Vs + (xbs - at) ** 2 / Ss)


text = se_at(0.0, 0.0)                                                        # read at zero, a lower-risk patient
check("read at zero, the dial's uncertainty is added: Alder 0.41 against 0.40, Birch 0.65 against 0.39 (blueprint: 0.406, 0.650)",
      fl(text[:2], 2) == [0.41, 0.65] and abs(text[0] - 0.406) < 1e-3 and abs(text[1] - 0.650) < 1e-3, str(fl(text[:4])))
full = np.zeros((len(Y), 5)); g4, x4, y4 = rows(FINITE); full = np.zeros((len(y4), 5)); full[np.arange(len(y4)), g4] = 1.0; full[:, 4] = x4
check("those are the standard errors from inverting the whole table", np.allclose(text[:4], np.sqrt(np.diag(cov4)[:4]), atol=1e-9))
check("Birch's patients are mostly higher-risk: 24 of 30", CAST["Birch"][2] == 24 and heads[1] == 30)
xbar = float(X01.mean())
avg = se_at(0.0, xbar)
three, sixty5 = se_at(3.0, 0.0), se_at(65.0, 0.0)
check("record the factor three units higher and Alder's standard error swells to 1.9; sixty-five higher, 38.1 (blueprint: 1.89, 38.1)",
      round(three[0], 1) == 1.9 and abs(three[0] - 1.89) < 6e-3 and round(sixty5[0], 1) == 38.1, f"{three[0]:.4f}, {sixty5[0]:.2f}")
check("at the average case mix the standard errors are 0.43, 0.47, 0.52, 0.66 (blueprint: 0.432, 0.467, 0.521, 0.658)",
      fl(avg[:4], 2) == [0.43, 0.47, 0.52, 0.66] and np.allclose(avg[:4], [0.432, 0.467, 0.521, 0.658], atol=6e-4), str(fl(avg[:4])))
check("and they do not change however the factor is recorded", np.allclose(se_at(3.0, xbar + 3.0), avg, atol=1e-9) and np.allclose(se_at(65.0, xbar + 65.0)[:4], avg[:4], atol=1e-6))
PKG = None
try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import logging
        logging.disable(logging.CRITICAL)
        import pandas as pd
        from pprof_py import LogisticFixedEffectModel
        mod = LogisticFixedEffectModel().fit(pd.DataFrame({"clinic": np.array(ALL)[PROV], "x": X01, "y": Y}), y_var="y", x_vars=["x"], provider_var="clinic")
        cm = np.sqrt(np.ravel(mod.variances_["gamma_case_mix"]).astype(float))
    PKG = {"se_case_mix": fl(cm, 4)}
    check("pprof_py's own comparison-ready standard errors are these four", np.allclose(cm[:4], avg[:4], atol=1e-4), str(fl(cm[:4])))
except Exception as err:                                                       # pragma: no cover
    check("pprof_py's comparison-ready standard errors compared", False, repr(err)[:140])

# ----------------------------------------------------------------------------- 5. the caterpillar (S07)
cat = [{"clinic": k, "gamma": float(gam[i]), "se": float(avg[i]), "low": float(gam[i] - 1.959964 * avg[i]), "high": float(gam[i] + 1.959964 * avg[i])} for i, k in enumerate(ALL)]
check("Elm's printed interval runs from -19.7 to +7.2: not an estimate (blueprint)", (round(cat[4]["low"], 1), round(cat[4]["high"], 1)) == (-19.7, 7.2), f"{cat[4]['low']:.2f}, {cat[4]['high']:.2f}")
check("every pair of the four intervals overlaps", all(cat[i]["low"] < cat[j]["high"] and cat[j]["low"] < cat[i]["high"] for i in range(4) for j in range(4)))
widths = [c["high"] - c["low"] for c in cat[:4]]
check("the intervals are 1.7 to 2.6 wide on the log-odds ruler, Alder's the narrowest and Dune's the widest", fl([min(widths), max(widths)], 1) == [1.7, 2.6]
      and int(np.argmin(widths)) == 0 and int(np.argmax(widths)) == 3, str(fl(widths, 2)))

# ----------------------------------------------------------------------------- 6. what size buys (S08)
from mim.crowd import simulate  # noqa: E402
c = simulate()
Xc, yc, pc = np.column_stack([c["x1"], c["x2"]]), c["y"].astype(float), c["prov"]
m = int(pc.max()) + 1
gc, bc = np.full(m, float(logit(yc.mean()))), np.zeros(2)
for _ in range(100):                                                           # joint fit of the crowd through the fold
    p = expit(gc[pc] + Xc @ bc); w = p * (1 - p); r = yc - p
    Ug, Vg = np.bincount(pc, weights=r, minlength=m), np.bincount(pc, weights=w, minlength=m)
    Bg = np.column_stack([np.bincount(pc, weights=w * Xc[:, k], minlength=m) for k in range(2)])
    Sc = Xc.T @ (Xc * w[:, None]) - Bg.T @ (Bg / Vg[:, None])
    db = np.linalg.solve(Sc, Xc.T @ r - Bg.T @ (Ug / Vg)); dg = (Ug - Bg @ db) / Vg
    gc, bc = gc + dg, bc + db
    if max(np.max(np.abs(db)), np.max(np.abs(dg))) < 1e-10:
        break
dev = Bg / Vg[:, None] - Xc.mean(axis=0)
se_c = np.sqrt(1.0 / Vg + np.einsum("ij,jk,ik->i", dev, np.linalg.inv(Sc), dev))
n_c = np.bincount(pc, minlength=m)
med = lambda a, b: float(np.median(se_c[(n_c >= a) & (n_c <= b)]))
slope = float(np.polyfit(np.log(n_c), np.log(se_c), 1)[0])
check("the crowd: median standard error 0.55 at 20 to 30 patients, 0.26 near 100, 0.12 above 400 (blueprint)",
      (round(med(20, 30), 2), round(med(90, 110), 2), round(med(400, 500), 2)) == (0.55, 0.26, 0.12), f"{med(20, 30):.3f}, {med(90, 110):.3f}, {med(400, 500):.3f}")
check("on log axes the standard errors fall along a line of slope -0.5: four times the patients, half the error", round(slope, 2) == -0.5, f"{slope:.3f}")
plan = 1.0 / (0.1 ** 2 * 0.2 * 0.8)
check("planning: a standard error of 0.1 at a 20% rate needs 625 patients", round(plan) == 625)

OUT = {
    "episode": 9, "title": "How Sure Are We?", "clinics": ALL, "patients": int(len(Y)), "heads": heads,
    "dial": {"beta": beta, "S": S, "se": float(se_beta), "low": float(lo), "high": float(hi), "or": float(np.exp(beta)), "or_low": float(np.exp(lo)), "or_high": float(np.exp(hi))},
    "hill": HILL,
    "tests": {"wald": float(wald), "lr": float(lr), "score": float(score), "z": float(beta / se_beta), "drop": float(lr / 2), "slope_at_zero": U0, "mantel_haenszel": float(mh),
              "p": [p_chi1(wald), p_chi1(lr), p_chi1(score)]},
    "wobble": fl(V, 6), "own_se": fl(own, 6), "rare_example": rare,
    "share": {"text_se": fl(text, 6), "avg_se": fl(avg, 6), "three_higher": fl(three, 6), "xbar": xbar, "own_var": fl(1.0 / V, 6), "borrowed_var": fl(xb ** 2 / S, 6)},
    "caterpillar": cat,
    "crowd": {"n": [int(v) for v in n_c], "se": fl(se_c, 4), "medians": [med(20, 30), med(90, 110), med(400, 500)], "slope": slope, "plan": plan},
    "package": PKG,
}

if __name__ == "__main__":
    print(f"dial: {beta:.4f} +- {se_beta:.4f}; interval {lo:.3f} to {hi:.3f}; odds ratio {np.exp(lo):.2f} to {np.exp(hi):.2f}")
    print(f"tests: across {wald:.2f}, down {lr:.2f}, slope {score:.2f}; MH {mh:.2f}")
    print("own SE     ", fl(own)); print("at zero    ", fl(text)); print("at average ", fl(avg)); print("three up   ", fl(three))
    print("caterpillar", [(c_["clinic"], round(c_["low"], 2), round(c_["high"], 2)) for c_ in cat])
    print(f"crowd medians {med(20, 30):.3f}, {med(90, 110):.3f}, {med(400, 500):.3f}; slope {slope:.3f}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e09_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
