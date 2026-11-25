"""Model in Motion · The Logistic Fixed-Effect Model · Episode 4: One Intercept per Provider.

Every number the episode shows or says is computed here, checked, and written to e04_numbers.json.
Scenes and narration read e04_numbers.json; nothing numeric is typed into scene code or the script.

    python e04_numbers.py        # prints the ledger, runs every check, writes e04_numbers.json

Three independent routes to the fit:
  1. a plain Newton-Raphson on the joint likelihood, written out below;
  2. statsmodels GLM with one dummy variable per clinic;
  3. pprof_py's LogisticFixedEffectModel (the package the series explains), if it is installed.
The blueprint appendix (computed earlier with pprof_py 0.7.0) is the fourth reference.
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
expit = lambda z: 1.0 / (1.0 + np.exp(-z))
logit = lambda p: np.log(p / (1.0 - p))

# ----------------------------------------------------------------------------- the cast (blueprint)
# clinic -> (lower-risk patients, of whom readmitted, higher-risk patients, of whom readmitted)
CAST = {
    "Alder": (24, 8, 6, 5),
    "Birch": (6, 1, 24, 13),
    "Cedar": (10, 2, 10, 6),
    "Dune": (6, 2, 6, 5),
    "Elm": (11, 0, 0, 0),
}
NAMES = list(CAST)
FINITE = ["Alder", "Birch", "Cedar", "Dune"]          # clinics whose intercept has a finite estimate

CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append((name, bool(ok), detail))


def rows(cast=CAST, names=NAMES):
    """Patient-level arrays: clinic index, x (1 = higher-risk), y (1 = readmitted)."""
    g, x, y = [], [], []
    for i, k in enumerate(names):
        n0, e0, n1, e1 = cast[k]
        for xx, n, e in ((0, n0, e0), (1, n1, e1)):
            g += [i] * n
            x += [xx] * n
            y += [1] * e + [0] * (n - e)
    return np.array(g), np.array(x, float), np.array(y, float)


# ----------------------------------------------------------------------------- 1. observed points
n0 = np.array([CAST[k][0] for k in NAMES]); e0 = np.array([CAST[k][1] for k in NAMES])
n1 = np.array([CAST[k][2] for k in NAMES]); e1 = np.array([CAST[k][3] for k in NAMES])
N, O = int((n0 + n1).sum()), int((e0 + e1).sum())
check("cast totals: 103 patients, 42 readmissions", N == 103 and O == 42, f"{N}, {O}")

obs = {}
for i, k in enumerate(NAMES):
    lo = e0[i] / n0[i]
    hi = e1[i] / n1[i] if n1[i] else None
    obs[k] = {
        "n_low": int(n0[i]), "events_low": int(e0[i]), "n_high": int(n1[i]), "events_high": int(e1[i]),
        "rate_low": float(lo), "rate_high": None if hi is None else float(hi),
        "logodds_low": None if lo in (0.0, 1.0) else float(logit(lo)),
        "logodds_high": None if hi in (None, 0.0, 1.0) else float(logit(hi)),
    }
    if obs[k]["logodds_low"] is not None and obs[k]["logodds_high"] is not None:
        obs[k]["own_step"] = obs[k]["logodds_high"] - obs[k]["logodds_low"]       # within-clinic log odds ratio
        obs[k]["own_odds_ratio"] = float(np.exp(obs[k]["own_step"]))

check("Alder and Dune have identical observed rates in both risk groups (their dots coincide)",
      obs["Alder"]["rate_low"] == obs["Dune"]["rate_low"] and obs["Alder"]["rate_high"] == obs["Dune"]["rate_high"],
      f"{obs['Alder']['rate_low']:.4f}, {obs['Alder']['rate_high']:.4f}")
check("Elm: no readmissions and no higher-risk patients", e0[4] == 0 and n1[4] == 0)

# ----------------------------------------------------------------------------- 2. the pooled line (Episode 3)
p_low, p_high = e0.sum() / n0.sum(), e1.sum() / n1.sum()
pooled = {"rate_low": float(p_low), "rate_high": float(p_high), "start": float(logit(p_low)),
          "step": float(logit(p_high) - logit(p_low)), "odds_ratio": float(np.exp(logit(p_high) - logit(p_low))),
          "counts": [int(e0.sum()), int(n0.sum()), int(e1.sum()), int(n1.sum())]}
check("pooled rates are 13/57 and 29/46", pooled["counts"] == [13, 57, 29, 46])
check("pooled line matches the blueprint (start -1.219, step 1.753, odds ratio 5.77)",
      abs(pooled["start"] + 1.219) < 5e-4 and abs(pooled["step"] - 1.753) < 5e-4 and abs(pooled["odds_ratio"] - 5.77) < 5e-3,
      f"{pooled['start']:.4f}, {pooled['step']:.4f}, {pooled['odds_ratio']:.3f}")

side = {}
for k in FINITE:
    a = obs[k]["logodds_low"] - pooled["start"]
    b = obs[k]["logodds_high"] - (pooled["start"] + pooled["step"])
    side[k] = "above" if (a > 0 and b > 0) else "below" if (a < 0 and b < 0) else "mixed"
check("cold open: Alder and Dune sit above the pooled line at both ends, Birch and Cedar below at both",
      side == {"Alder": "above", "Birch": "below", "Cedar": "below", "Dune": "above"}, str(side))

# ----------------------------------------------------------------------------- 3. a line of its own per clinic (the foil)
gap_low = obs["Alder"]["logodds_low"] - obs["Cedar"]["logodds_low"]
gap_high = obs["Alder"]["logodds_high"] - obs["Cedar"]["logodds_high"]
check("with separate lines the Alder-Cedar gap is larger for higher-risk patients (0.69 against 1.20)",
      abs(gap_low - 0.693) < 1e-3 and abs(gap_high - 1.204) < 1e-3, f"{gap_low:.4f}, {gap_high:.4f}")
check("within-clinic steps are 2.30, 1.78, 1.79, 2.30 (odds ratios 10, 5.9, 6, 10)",
      np.allclose([obs[k]["own_step"] for k in FINITE], [2.3026, 1.7765, 1.7918, 2.3026], atol=5e-5)
      and np.allclose([obs[k]["own_odds_ratio"] for k in FINITE], [10, 65 / 11, 6, 10]),
      str([round(obs[k]["own_step"], 4) for k in FINITE]))


# ----------------------------------------------------------------------------- 4. the fixed-effect fit
def fit_newton(names=FINITE, tol=1e-13, maxit=100):
    """Joint maximum likelihood for logit(p_ij) = gamma_i + beta x_ij by Newton-Raphson."""
    g, x, y = rows(names=names)
    m = len(names)
    Z = np.zeros((len(y), m + 1))
    Z[np.arange(len(y)), g] = 1.0
    Z[:, m] = x
    th = np.zeros(m + 1)
    th[:m] = logit(y.mean())
    for it in range(1, maxit + 1):
        p = expit(Z @ th)
        U = Z.T @ (y - p)
        I = Z.T @ (Z * (p * (1 - p))[:, None])
        step = np.linalg.solve(I, U)
        th = th + step
        if np.max(np.abs(step)) < tol:
            break
    p = expit(Z @ th)
    ll = float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return th[:m], float(th[m]), np.linalg.inv(I), ll, it, (Z.T @ (y - p))


gamma, beta, cov, loglik, iters, score = fit_newton()
check("Newton converged with a zero score", np.max(np.abs(score)) < 1e-10, f"{iters} iterations")
check("fit matches the blueprint appendix: beta 2.0164; gamma -0.6520, -1.8217, -1.5228, -0.5804",
      abs(beta - 2.0164) < 5e-5 and np.allclose(gamma, [-0.6520, -1.8217, -1.5228, -0.5804], atol=5e-5),
      f"{beta:.4f}; {np.round(gamma, 4)}")
check("odds ratio 7.51 and its 95% interval 2.39 to 23.62 (blueprint)",
      abs(np.exp(beta) - 7.51) < 5e-3 and abs(np.exp(beta - 1.959964 * np.sqrt(cov[-1, -1])) - 2.39) < 5e-3
      and abs(np.exp(beta + 1.959964 * np.sqrt(cov[-1, -1])) - 23.62) < 5e-3,
      f"{np.exp(beta):.3f}, se {np.sqrt(cov[-1, -1]):.3f}")

# route 2: statsmodels GLM with clinic dummies
try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import statsmodels.api as sm
        g4, x4, y4 = rows(names=FINITE)
        D = np.zeros((len(y4), 5)); D[np.arange(len(y4)), g4] = 1.0; D[:, 4] = x4
        r = sm.GLM(y4, D, family=sm.families.Binomial()).fit(tol=1e-13, maxiter=200)
    d_sm = float(np.max(np.abs(np.r_[gamma, beta] - r.params)))
    check("statsmodels dummy-variable GLM agrees with the Newton fit", d_sm < 1e-8, f"max difference {d_sm:.1e}")
except ImportError:                                                     # pragma: no cover
    check("statsmodels dummy-variable GLM agrees with the Newton fit", False, "statsmodels not installed")

# route 3: pprof_py itself (all five clinics, package defaults)
PPROF = None
try:
    import logging
    logging.disable(logging.CRITICAL)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import pandas as pd
        import pprof_py
        from pprof_py import LogisticFixedEffectModel
        g5, x5, y5 = rows()
        df = pd.DataFrame({"clinic": np.array(NAMES)[g5], "x": x5, "y": y5})
        mod = LogisticFixedEffectModel().fit(df, y_var="y", x_vars=["x"], provider_var="clinic")
        pg = np.ravel(mod.coefficients_["gamma"]).astype(float)
        pb = float(np.ravel(mod.coefficients_["beta"])[0])
    PPROF = {"version": pprof_py.__version__, "beta": pb, "gamma": [float(v) for v in pg]}
    check(f"pprof_py {pprof_py.__version__} gives the same beta and the same four finite gammas",
          abs(pb - beta) < 1e-6 and np.allclose(pg[:4], gamma, atol=1e-6),
          f"beta difference {abs(pb - beta):.1e}; gamma difference {np.max(np.abs(pg[:4] - gamma)):.1e}")
    check("pprof_py's printed value for Elm is far below every other clinic (no finite estimate)",
          pg[4] < min(gamma) - 3, f"Elm printed as {pg[4]:.2f}")
except ImportError:                                                     # pragma: no cover
    check("pprof_py agrees with the Newton fit", False, "pprof_py not installed (clone github.com/UM-KevinHe/pprof_py)")

fit = {}
for i, k in enumerate(FINITE):
    fit[k] = {"gamma": float(gamma[i]), "p_low": float(expit(gamma[i])), "p_high": float(expit(gamma[i] + beta)),
              "logodds_high": float(gamma[i] + beta),
              "expected": float(obs[k]["n_low"] * expit(gamma[i]) + obs[k]["n_high"] * expit(gamma[i] + beta)),
              "observed": int(obs[k]["events_low"] + obs[k]["events_high"])}
check("fitted probabilities match the blueprint: Alder 34/80, Birch 14/55, Cedar 18/62, Dune 36/81 percent",
      [round(100 * fit[k]["p_low"]) for k in FINITE] == [34, 14, 18, 36]
      and [round(100 * fit[k]["p_high"]) for k in FINITE] == [80, 55, 62, 81],
      str([(round(100 * fit[k]["p_low"], 1), round(100 * fit[k]["p_high"], 1)) for k in FINITE]))
check("order of the finite gammas: Birch < Cedar < Alder < Dune",
      fit["Birch"]["gamma"] < fit["Cedar"]["gamma"] < fit["Alder"]["gamma"] < fit["Dune"]["gamma"])
check("Alder and Dune are close together at the top (0.07 apart) although their dots coincide",
      abs((fit["Dune"]["gamma"] - fit["Alder"]["gamma"]) - 0.0716) < 5e-4, f"{fit['Dune']['gamma'] - fit['Alder']['gamma']:.4f}")
check("fitted lines do not pass through the dots: Alder observed 33.3/83.3 percent, fitted 34.3/79.6",
      abs(fit["Alder"]["p_low"] - obs["Alder"]["rate_low"]) > 0.005 and abs(fit["Alder"]["p_high"] - obs["Alder"]["rate_high"]) > 0.02)
check("each finite clinic's expected count equals its observed count at the fit (kept for Episode 6)",
      all(abs(fit[k]["expected"] - fit[k]["observed"]) < 1e-8 for k in FINITE))

# ----------------------------------------------------------------------------- 5. where beta comes from
steps = np.array([obs[k]["own_step"] for k in FINITE])
check("the shared step lies inside the range of the four within-clinic steps", steps.min() < beta < steps.max(),
      f"{steps.min():.3f} < {beta:.3f} < {steps.max():.3f}")
check("the shared step (2.02) is larger than the pooled step (1.75)", beta > pooled["step"] + 0.2)
# an inverse-variance (Woolf) average shows which clinics carry the weight
cells = {k: (CAST[k][3], CAST[k][2] - CAST[k][3], CAST[k][1], CAST[k][0] - CAST[k][1]) for k in FINITE}
w = np.array([1.0 / sum(1.0 / c for c in cells[k]) for k in FINITE])
woolf = float((w * steps).sum() / w.sum())
check("it leans toward the better-informed clinics: below the plain average of the four steps, near the weighted one",
      beta < steps.mean() and abs(beta - woolf) < 0.03, f"plain {steps.mean():.3f}, weighted {woolf:.3f}, fit {beta:.3f}")
gE, xE, yE = rows()
check("Elm cannot inform beta: all of its patients have x = 0", float(xE[gE == 4].sum()) == 0.0)
# Elm's rows have x = 0 and belong to no other clinic, so whatever its gamma is they add nothing to the
# score for beta or for the other four gammas: the four-clinic fit stays the solution with Elm included.
pE = expit(-30.0)
check("adding Elm changes neither beta nor the other gammas (its patients add zero to beta's score)",
      abs(float((xE[gE == 4] * (yE[gE == 4] - pE)).sum())) == 0.0 and (PPROF is None or abs(PPROF["beta"] - beta) < 1e-6))

# ----------------------------------------------------------------------------- 6. no overall intercept
c = 0.5
p_a = np.array([[expit(fit[k]["gamma"] + beta * xx) for xx in (0, 1)] for k in FINITE])
p_b = np.array([[expit((0.0 + c) + (fit[k]["gamma"] - c) + beta * xx) for xx in (0, 1)] for k in FINITE])
check("raising an overall intercept by 0.5 and lowering every gamma by 0.5 changes no probability", np.allclose(p_a, p_b, atol=1e-15))

# ----------------------------------------------------------------------------- 7. Elm never settles
elm_lik = {g: float((1 - expit(g)) ** 11) for g in (-2.0, -4.0, -6.0, -8.0)}
vals = list(elm_lik.values())
check("Elm's likelihood keeps rising as its gamma falls (no maximum)", all(b > a for a, b in zip(vals, vals[1:])) and vals[-1] < 1.0,
      str({k: round(v, 4) for k, v in elm_lik.items()}))

# ----------------------------------------------------------------------------- 8. what gamma is; the next episode's gap
gapAC = fit["Alder"]["gamma"] - fit["Cedar"]["gamma"]
check("Alder's gamma is a log-odds: -0.65 is 34 percent for a lower-risk patient", round(100 * expit(fit["Alder"]["gamma"])) == 34)
check("teaser: Alder's line is 0.87 above Cedar's, an odds ratio of 2.4", abs(gapAC - 0.8708) < 5e-5 and abs(np.exp(gapAC) - 2.389) < 5e-4,
      f"{gapAC:.4f}, {np.exp(gapAC):.3f}")
check("a shared step makes the gap the same at both risk levels",
      abs((fit["Alder"]["logodds_high"] - fit["Cedar"]["logodds_high"]) - gapAC) < 1e-12)

# ----------------------------------------------------------------------------- 9. the middle clinic (recap)
order5 = ["Elm"] + sorted(FINITE, key=lambda k: fit[k]["gamma"])          # Elm sits below every finite gamma
check("lined up, the middle of the five gammas is Cedar's (pprof_py's default reference, the median)",
      order5 == ["Elm", "Birch", "Cedar", "Alder", "Dune"] and order5[2] == "Cedar"
      and (PPROF is None or abs(float(np.median(PPROF["gamma"])) - fit["Cedar"]["gamma"]) < 1e-6), " < ".join(order5))
check("spoken roundings: pooled 23% and 63%; steps 1.75 and 2.02; odds x 7.5; gammas -1.82, -1.52, -0.65, -0.58; gap 0.87",
      (round(100 * p_low), round(100 * p_high)) == (23, 63) and round(pooled["step"], 2) == 1.75 and round(beta, 2) == 2.02
      and round(float(np.exp(beta)), 1) == 7.5 and [round(fit[k]["gamma"], 2) for k in ("Birch", "Cedar", "Alder", "Dune")] == [-1.82, -1.52, -0.65, -0.58]
      and round(gapAC, 2) == 0.87)

# ----------------------------------------------------------------------------- 10. the crowd (S09)
def fit_pooled(X, y):
    """One logistic model for everyone: an intercept and the covariates, no provider terms."""
    Z = np.column_stack([np.ones(len(y)), X]); th = np.zeros(Z.shape[1])
    for _ in range(100):
        p = expit(Z @ th)
        step = np.linalg.solve(Z.T @ (Z * (p * (1 - p))[:, None]), Z.T @ (y - p)); th = th + step
        if np.max(np.abs(step)) < 1e-12:
            break
    return th


def fit_fixed_effects(prov, X, y):
    """One intercept per provider. Newton steps go through the Schur complement, so nothing m x m is formed."""
    m = int(prov.max()) + 1
    g = np.full(m, logit(y.mean())); b = np.zeros(X.shape[1])
    for _ in range(200):
        p = expit(g[prov] + X @ b); w = p * (1 - p); r = y - p
        Ug, Igg = np.bincount(prov, weights=r, minlength=m), np.bincount(prov, weights=w, minlength=m)
        Igb = np.column_stack([np.bincount(prov, weights=w * X[:, k], minlength=m) for k in range(X.shape[1])])
        S = X.T @ (X * w[:, None]) - Igb.T @ (Igb / Igg[:, None])
        db = np.linalg.solve(S, X.T @ r - Igb.T @ (Ug / Igg)); dg = (Ug - Igb @ db) / Igg
        g, b = g + dg, b + db
        if max(np.max(np.abs(db)), np.max(np.abs(dg))) < 1e-11:
            break
    return g, b


CROWD = {"status": "not computed: run this file inside the repository, where mim.crowd can be imported"}
try:
    sys.path.insert(0, str(HERE.parents[1]))
    from mim.crowd import BETA as TRUE_BETA, simulate
    c = simulate()                                        # seed 2026, tau = 0.3: the crowd Episode 1 showed
    Xc, yc, pc = np.column_stack([c["x1"], c["x2"]]), c["y"].astype(float), c["prov"]
    Oc, nc = np.bincount(pc, weights=yc), np.bincount(pc)
    inside = (Oc > 0) & (Oc < nc)                         # a provider with no events (or only events) has no finite intercept
    keep, relabel = inside[pc], np.cumsum(inside) - 1
    pooled_c = fit_pooled(Xc, yc)
    g_c, b_c = fit_fixed_effects(relabel[pc[keep]], Xc[keep], yc[keep])
    CROWD = {"true_step": float(TRUE_BETA[0]), "pooled_step": float(pooled_c[1]), "fixed_effect_step": float(b_c[0]),
             "second_covariate": {"true": float(TRUE_BETA[1]), "pooled": float(pooled_c[2]), "fixed_effect": float(b_c[1])},
             "providers": int(len(nc)), "patients": int(len(yc)), "events": int(yc.sum()),
             "providers_without_a_finite_intercept": int((~inside).sum()),
             "case_mix_effect_correlation": float(np.corrcoef(c["mu"], c["gamma"])[0, 1]),
             "gamma_hat": [round(float(v), 4) for v in g_c] if bool(inside.all()) else None,   # fitted intercepts, for the 200 lines of S09
             "status": "computed here from mim.crowd (seed 2026, tau 0.3)"}
    check("crowd is the series' crowd: 200 providers, 28,848 patients, 6,601 events",
          (CROWD["providers"], CROWD["patients"], CROWD["events"]) == (200, 28848, 6601),
          f"{CROWD['providers']}, {CROWD['patients']}, {CROWD['events']}")
    check("crowd: pooled step 0.710 and fixed-effect step 0.814 against a true 0.80 (blueprint appendix)",
          abs(CROWD["pooled_step"] - 0.710) < 5e-4 and abs(CROWD["fixed_effect_step"] - 0.814) < 5e-4,
          f"{CROWD['pooled_step']:.4f}, {CROWD['fixed_effect_step']:.4f}")
    check("crowd: second covariate 0.506 pooled and 0.514 fixed-effect against a true 0.50",
          abs(pooled_c[2] - 0.506) < 5e-4 and abs(b_c[1] - 0.514) < 5e-4, f"{pooled_c[2]:.4f}, {b_c[1]:.4f}")
    check("crowd: providers with sicker patients do a little better (why pooling flattens the step)",
          CROWD["case_mix_effect_correlation"] < -0.3, f"correlation of case mix with provider effect {CROWD['case_mix_effect_correlation']:.2f}")
    check("spoken roundings for the crowd: 0.8, 0.71, 0.81",
          (round(CROWD["true_step"], 1), round(CROWD["pooled_step"], 2), round(CROWD["fixed_effect_step"], 2)) == (0.8, 0.71, 0.81))
    if PPROF is not None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            dfc = pd.DataFrame({"prov": pc, "x1": c["x1"], "x2": c["x2"], "y": yc})
            mc = LogisticFixedEffectModel().fit(dfc, y_var="y", x_vars=["x1", "x2"], provider_var="prov")
            bp = np.ravel(mc.coefficients_["beta"]).astype(float)
        check("crowd: pprof_py gives the same two fixed-effect steps", np.allclose(bp, b_c, atol=1e-5), f"largest difference {np.max(np.abs(bp - b_c)):.1e}")
except ImportError as err:
    check("crowd figures recomputed from the series' generator", False, str(err))

# ----------------------------------------------------------------------------- write and report
OUT = {
    "episode": 4, "title": "One Intercept per Provider",
    "cast_totals": {"patients": N, "readmissions": O},
    "observed": obs, "pooled": pooled,
    "separate_lines": {"alder_minus_cedar_low": gap_low, "alder_minus_cedar_high": gap_high},
    "fit": {"beta": beta, "odds_ratio": float(np.exp(beta)), "se_beta": float(np.sqrt(cov[-1, -1])),
            "ci_odds_ratio": [float(np.exp(beta - 1.959964 * np.sqrt(cov[-1, -1]))), float(np.exp(beta + 1.959964 * np.sqrt(cov[-1, -1])))],
            "loglik": loglik, "clinics": fit, "elm": {"gamma": None, "likelihood_at_gamma": elm_lik}},
    "within_clinic_steps": {k: obs[k]["own_step"] for k in FINITE},
    "weighted_average_step": woolf, "plain_average_step": float(steps.mean()),
    "next_episode": {"alder_minus_cedar": gapAC, "odds_ratio": float(np.exp(gapAC))},
    "gamma_order": order5, "middle_clinic": order5[2],
    "crowd": CROWD, "pprof_py": PPROF,
}

if __name__ == "__main__":
    print(f"pooled line     start {pooled['start']:+.4f} ({100 * p_low:.1f}%)   step {pooled['step']:.4f}   odds ratio {pooled['odds_ratio']:.2f}")
    print(f"shared step     beta  {beta:.4f}   odds ratio {np.exp(beta):.2f}   (95% interval {OUT['fit']['ci_odds_ratio'][0]:.2f} to {OUT['fit']['ci_odds_ratio'][1]:.2f})")
    print(f"{'clinic':8s}{'gamma':>9s}{'fit low':>9s}{'fit high':>9s}{'obs low':>9s}{'obs high':>9s}{'own step':>10s}{'vs pooled':>11s}")
    for k in FINITE:
        print(f"{k:8s}{fit[k]['gamma']:9.4f}{100 * fit[k]['p_low']:8.1f}%{100 * fit[k]['p_high']:8.1f}%"
              f"{100 * obs[k]['rate_low']:8.1f}%{100 * obs[k]['rate_high']:8.1f}%{obs[k]['own_step']:10.4f}{side[k]:>11s}")
    print(f"{'Elm':8s}{'none':>9s}{'':>9s}{'':>9s}{0.0:8.1f}%{'':>9s}{'':>10s}{'off chart':>11s}")
    print(f"gap Alder - Cedar: separate lines {gap_low:.3f} (lower-risk) and {gap_high:.3f} (higher-risk); shared step {gapAC:.4f} (odds ratio {np.exp(gapAC):.2f})")
    print(f"compromise: plain average {steps.mean():.3f}, weighted {woolf:.3f}, fitted {beta:.3f}")
    if "pooled_step" in CROWD:
        print(f"crowd: true step {CROWD['true_step']:.2f}, pooled {CROWD['pooled_step']:.3f}, fixed-effect {CROWD['fixed_effect_step']:.3f} "
              f"({CROWD['providers']} providers, {CROWD['patients']} patients, {CROWD['providers_without_a_finite_intercept']} without a finite intercept)")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e04_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
