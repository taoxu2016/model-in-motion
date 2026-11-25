import numpy as np, pandas as pd, warnings, logging
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit, logit
from scipy.stats import norm, chi2
from cast import CAST, build
from pprof_py import LogisticFixedEffectModel
np.set_printoptions(precision=4, suppress=True, linewidth=170)
names = list(CAST); n0 = np.array([CAST[k][0] for k in names]); e0 = np.array([CAST[k][1] for k in names]); n1 = np.array([CAST[k][2] for k in names]); e1 = np.array([CAST[k][3] for k in names]); n = n0 + n1; O = e0 + e1
d = build(); m = LogisticFixedEffectModel().fit(d, y_var="y", x_vars=["x"], provider_var="clinic")
beta = float(np.ravel(m.coefficients_["beta"])[0]); gam = np.ravel(m.coefficients_["gamma"]); g0 = np.median(gam)
print("== CMH for beta=0")
a_exp = n1 * O / n; var = n1 * n0 * O * (n - O) / (n ** 2 * (n - 1))
print("sum(a - E)", (e1 - a_exp).sum(), "CMH var", var.sum(), "CMH chi2 (no continuity corr.)", (e1 - a_exp).sum() ** 2 / var.sum(), "score chi2", (e1 - a_exp).sum() ** 2 / (n1 * n0 * O * (n - O) / n ** 3).sum())
mh_or = (e1 * (n0 - e0) / n).sum() / (e0 * (n1 - e1) / n).sum(); print("Mantel-Haenszel OR", mh_or, "log", np.log(mh_or))
print("within-clinic ORs", (e1 / np.maximum(n1 - e1, 1e-9)) / (e0 / (n0 - e0)))

print("\n== M1 weights swap")
ra0, ra1 = e0[0] / n0[0], e1[0] / n1[0]; rb0, rb1 = e0[1] / n0[1], e1[1] / n1[1]
print("Alder rates with Birch mix", 0.2 * ra0 + 0.8 * ra1, "Birch rates with Alder mix", 0.8 * rb0 + 0.2 * rb1)
print("Alder rates on whole cast mix (57 low, 46 high):", (57 * ra0 + 46 * ra1) / 103, "Birch:", (57 * rb0 + 46 * rb1) / 103)

print("\n== M5 translations for OR Alder vs Cedar", np.exp(gam[0] - gam[2]), "gap", gam[0] - gam[2])
for p in (0.05, expit(g0), 0.5, expit(g0 + beta), 0.9):
    q = expit(logit(p) + gam[0] - gam[2]); print(f"  p_ref {p:.3f} -> {q:.3f}  diff {q - p:.3f}  ratio {q / p:.3f}")
sm = m.calculate_standardized_measures(stdz=["direct"])["direct"]; dr = sm.direct_rate.to_numpy() / 100
print("marginal log OR Alder vs Cedar from direct rates", logit(dr[0]) - logit(dr[2]), "; Dune vs Cedar", logit(dr[3]) - logit(dr[2]), "conditional", gam[3] - gam[2])
print("centring x at 0.5: gamma shift", 0.5 * beta)
dc = d.assign(x=d.x - 0.5); mc = LogisticFixedEffectModel().fit(dc, y_var="y", x_vars=["x"], provider_var="clinic")
print("  refit: beta", np.ravel(mc.coefficients_["beta"]), "gamma", np.ravel(mc.coefficients_["gamma"]), "SE gamma", np.sqrt(np.ravel(mc.variances_["gamma"])).round(4), "SE case mix", np.sqrt(np.ravel(mc.variances_["gamma_case_mix"])).round(4))
print("  ISR", mc.calculate_standardized_measures()["indirect"].indirect_ratio.round(4).to_numpy(), "exact p", mc.test().p_value.round(4).to_numpy())

print("\n== M7 one-dimensional Newton for Dune at beta_hat, starting from the reference")
g = g0
for it in range(6):
    p0_, p1_ = expit(g), expit(g + beta); E = 6 * p0_ + 6 * p1_; V = 6 * p0_ * (1 - p0_) + 6 * p1_ * (1 - p1_)
    print(f"  iter {it}: gamma {g:.5f}  E {E:.4f}  O-E {7 - E:.4f}  V {V:.4f}  step {(7 - E) / V:.5f}  ll {2*np.log(p0_)+4*np.log(1-p0_)+5*np.log(p1_)+1*np.log(1-p1_):.5f}")
    g = g + (7 - E) / V
print("  same for Alder from the reference:")
g = g0
for it in range(5):
    p0_, p1_ = expit(g), expit(g + beta); E = 24 * p0_ + 6 * p1_; V = 24 * p0_ * (1 - p0_) + 6 * p1_ * (1 - p1_)
    print(f"  iter {it}: gamma {g:.5f}  E {E:.4f}  O-E {13 - E:.4f}  V {V:.4f}  step {(13 - E) / V:.5f}"); g = g + (13 - E) / V

print("\n== M10 Fen screening")
fen = pd.DataFrame([("Fen", 0, 1)] * 1 + [("Fen", 0, 0)] * 4 + [("Fen", 1, 1)] * 2 + [("Fen", 1, 0)] * 1, columns=["clinic", "x", "y"])
d6 = pd.concat([d, fen], ignore_index=True); m6 = LogisticFixedEffectModel().fit(d6, y_var="y", x_vars=["x"], provider_var="clinic")
print("providers kept", m6.provider_ids_, "excluded:"); print(m6.excluded_providers_)
print("beta with Fen screened", np.ravel(m6.coefficients_["beta"]))
m6b = LogisticFixedEffectModel(cutoff=5).fit(d6, y_var="y", x_vars=["x"], provider_var="clinic"); print("cutoff=5 keeps", m6b.provider_ids_, "beta", np.ravel(m6b.coefficients_["beta"]), "gamma", np.ravel(m6b.coefficients_["gamma"]).round(3))
m11 = LogisticFixedEffectModel(cutoff=11).fit(d, y_var="y", x_vars=["x"], provider_var="clinic"); print("cutoff=11 keeps", m11.provider_ids_)
print("Elm counterfactual: P(0 of 30) =", (1 - expit(g0)) ** 30, " P(0 of 11) =", (1 - expit(g0)) ** 11, "; Elm Newton step -1/(1-p) at gamma=-3:", -1 / (1 - expit(-3)))
from pprof_py.inference import degenerate_providers, at_bound
print(degenerate_providers(m)); print("at_bound", at_bound(m))

print("\n== binomial rows (n_var): 9 rows instead of 103")
rows = []
for k in names:
    a0, b0, a1, b1 = CAST[k]
    rows.append((k, 0, b0, a0))
    if a1 > 0: rows.append((k, 1, b1, a1))
db = pd.DataFrame(rows, columns=["clinic", "x", "events", "trials"]); print(db.to_string())
mbn = LogisticFixedEffectModel(use_dataprep=False).fit(db, y_var="events", x_vars=["x"], provider_var="clinic", n_var="trials")
print("beta", np.ravel(mbn.coefficients_["beta"]), "gamma", np.ravel(mbn.coefficients_["gamma"]), "exact p", mbn.test().p_value.round(4).to_numpy(), "ISR", mbn.calculate_standardized_measures()["indirect"].indirect_ratio.round(4).to_numpy())

print("\n== Wald variance and the covariates' origin (cast): SE from variances_['gamma'] when x is recorded as x, x+3, x+65")
for c in (0, 3, 65):
    mm = LogisticFixedEffectModel().fit(d.assign(x=d.x + c), y_var="y", x_vars=["x"], provider_var="clinic")
    gg = np.ravel(mm.coefficients_["gamma"]); se_r = np.sqrt(np.ravel(mm.variances_["gamma"])); se_c = np.sqrt(np.ravel(mm.variances_["gamma_case_mix"])); gg0 = np.median(gg)
    print(f"  x+{c}: gamma {gg[:4].round(3)} SE(gamma) {se_r[:4].round(3)} z with it {((gg - gg0) / se_r)[:4].round(3)} | SE case mix {se_c[:4].round(3)} z {((gg - gg0) / se_c)[:4].round(3)}")
