import numpy as np, pandas as pd, warnings, logging, io, contextlib
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit, logit
from scipy.stats import norm
from cast import CAST, build
from pprof_py import LogisticFixedEffectModel
np.set_printoptions(precision=5, suppress=True, linewidth=160)
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)

d = build()
names = list(CAST)
n0 = np.array([CAST[k][0] for k in names]); e0 = np.array([CAST[k][1] for k in names])
n1 = np.array([CAST[k][2] for k in names]); e1 = np.array([CAST[k][3] for k in names])
n = n0 + n1; O = e0 + e1
print("== 1. cast"); print(pd.DataFrame({"n_low": n0, "ev_low": e0, "n_high": n1, "ev_high": e1, "n": n, "O": O, "raw": O / n,
      "rate_low": e0 / n0, "rate_high": np.where(n1 > 0, e1 / np.maximum(n1, 1), np.nan), "share_high": n1 / n}, index=names).round(4))
N = n.sum(); Otot = O.sum(); ybar = Otot / N
print("N", N, "O", Otot, "ybar", ybar, "logit", logit(ybar))
print("low:", e0.sum(), n0.sum(), e0.sum() / n0.sum(), "high:", e1.sum(), n1.sum(), e1.sum() / n1.sum())

print("\n== 3. pooled model (no provider effects)")
pl, ph = e0.sum() / n0.sum(), e1.sum() / n1.sum()
print("alpha", logit(pl), "beta_pooled", logit(ph) - logit(pl), "OR", np.exp(logit(ph) - logit(pl)))
Epool = n0 * pl + n1 * ph
print(pd.DataFrame({"O": O, "E_pooled": Epool, "O/E_pooled": O / Epool}, index=names).round(4))
import statsmodels.api as smapi
pm = smapi.Logit(d.y, smapi.add_constant(d[["x"]])).fit(disp=0)
print("statsmodels pooled:", pm.params.values, "se", pm.bse.values)

print("\n== 4. FE fit (pprof_py defaults)")
m = LogisticFixedEffectModel().fit(d, y_var="y", x_vars=["x"], provider_var="clinic")
beta = float(np.ravel(m.coefficients_["beta"])[0]); gam = np.ravel(m.coefficients_["gamma"]).copy()
print("beta", beta, "OR", np.exp(beta), "gamma", gam, "iters", m.algorithm.iter)
mb = LogisticFixedEffectModel(algorithm="Ban").fit(d, y_var="y", x_vars=["x"], provider_var="clinic")
print("BAN beta", np.ravel(mb.coefficients_["beta"]), "gamma", np.ravel(mb.coefficients_["gamma"]), "iters", mb.algorithm.iter)
print("loglik", m.algorithm._loglikelihood(gam[m.provider_indices_], np.array([beta])), "aic", m.aic_, "bic", m.bic_, "auc", m.auc_)
# statsmodels cross-check on clinics with events
d4 = d[d.clinic != "Elm"]
Xd = pd.get_dummies(d4.clinic).astype(float); Xd["x"] = d4.x.values
g4 = smapi.GLM(d4.y.values, Xd.values, family=smapi.families.Binomial()).fit(tol=1e-12, maxiter=200)
print("statsmodels (4 clinics with events): ", g4.params, "se", g4.bse)
print("max |diff| gamma", np.max(np.abs(g4.params[:4] - gam[:4])), "beta diff", abs(g4.params[4] - beta))
# sklearn cross-check (unpenalised)
from sklearn.linear_model import LogisticRegression
sk = LogisticRegression(penalty=None, fit_intercept=False, tol=1e-12, max_iter=10000).fit(Xd.values, d4.y.values)
print("sklearn:", sk.coef_.ravel())

print("\n== 6. fitted cell probabilities")
p0 = expit(gam); p1 = expit(gam + beta)
print(pd.DataFrame({"gamma": gam, "p_low": p0, "p_high": p1, "fit_events": n0 * p0 + n1 * p1, "O": O,
                    "odds_ratio_vs_Cedar": np.exp(gam - gam[2])}, index=names).round(5))
print("high-risk fitted events", (n1 * p1).sum(), "observed", e1.sum())

print("\n== 7. information at the MLE")
w0 = p0 * (1 - p0); w1 = p1 * (1 - p1)
D = n0 * w0 + n1 * w1; B = n1 * w1; A = (n1 * w1).sum()
S = A - (B ** 2 / D).sum()
xbar_i = B / D; xbar = n1.sum() / N
print("D", D, "B", B, "A", A, "S", S, "Var beta", 1 / S, "SE beta", S ** -0.5)
print("per-provider Schur pieces n1*w1 - B^2/D:", n1 * w1 - B ** 2 / D)
varg = 1 / D + xbar_i ** 2 / S; varcm = 1 / D + (xbar_i - xbar) ** 2 / S
print(pd.DataFrame({"D": D, "xbar_w": xbar_i, "1/D": 1 / D, "beta_part": xbar_i ** 2 / S, "SE_gamma": np.sqrt(varg), "SE_casemix": np.sqrt(varcm),
                    "pp_SE": np.sqrt(np.ravel(m.variances_["gamma"])), "pp_SE_cm": np.sqrt(np.ravel(m.variances_["gamma_case_mix"]))}, index=names).round(5))
print("pprof var beta", m.variances_["beta"], "xbar", xbar)
# dense inverse check
Xfull = np.c_[np.eye(5)[m.provider_indices_], d.sort_values("clinic").x.values] if False else None

print("\n== 9. beta tests")
with contextlib.redirect_stdout(io.StringIO()):
    tw = m.summary(test_method="wald")
print(tw.round(5).to_string())
# profile log-likelihood of beta (maximise over gamma for each beta), by 1-D Newton per provider
def prof(b, bound=30.0):
    g = np.full(5, logit(ybar))
    for _ in range(200):
        p0_, p1_ = expit(g), expit(g + b)
        U = O - n0 * p0_ - n1 * p1_; I = n0 * p0_ * (1 - p0_) + n1 * p1_ * (1 - p1_)
        g = np.clip(g + U / np.maximum(I, 1e-300), -bound, bound)
    eta0, eta1 = g, g + b
    ll = (e0 * eta0 - n0 * np.logaddexp(0, eta0) + e1 * eta1 - n1 * np.logaddexp(0, eta1)).sum()
    return ll, g
ll_hat, _ = prof(beta); ll_0, g_tilde = prof(0.0)
print("profile loglik at beta_hat", ll_hat, "at 0", ll_0, "LR", 2 * (ll_hat - ll_0))
pt = O / n; pt = np.clip(pt, 1e-12, 1 - 1e-12)
U0 = (e1 - n1 * pt).sum(); w = pt * (1 - pt); I0 = (n1 * w - (n1 * w) ** 2 / np.maximum(n * w, 1e-300)).sum()
print("score at beta=0:", U0, "info", I0, "score chi2", U0 ** 2 / I0, "z", U0 / I0 ** .5)
print("wald chi2", (beta / S ** -0.5) ** 2, "z", beta * S ** 0.5)
from scipy.stats import chi2
print("p: wald", chi2.sf((beta * S ** .5) ** 2, 1), "LR", chi2.sf(2 * (ll_hat - ll_0), 1), "score", chi2.sf(U0 ** 2 / I0, 1))
print("profile loglik grid:")
for b in [-1, -0.5, 0, 0.5, 1, 1.5, 1.7533, 2, 2.0164, 2.5, 3, 3.5, 4, 5]:
    print("  beta", b, "ll", round(prof(b)[0], 4))
print("beta CI wald", beta - 1.96 * S ** -.5, beta + 1.96 * S ** -.5, "OR CI", np.exp(beta - 1.96 * S ** -.5), np.exp(beta + 1.96 * S ** -.5))

print("\n== 10. standardized measures")
sm = m.calculate_standardized_measures(stdz=["indirect", "direct"])
print(sm["indirect"].round(4).to_string()); print(sm["direct"].round(4).to_string())
smm = m.calculate_standardized_measures(stdz=["indirect", "direct"], reference="mean")
print("reference=mean gamma0:", np.average(gam, weights=m.provider_sizes_)); print(smm["indirect"].round(4).to_string())
g0 = np.median(gam); print("gamma0 median", g0, "p_low_ref", expit(g0), "p_high_ref", expit(g0 + beta))

print("\n== 11. tests")
for t in ["poibin_exact", "score", "wald"]:
    r = m.test(test_method=t); print(t); print(r[["estimate", "se", "z_raw", "p_value", "flag", "ci_lower", "ci_upper"]].round(4).to_string())
r = m.test(test_method="bootstrap_exact", n_resample=10000, seed=2026); print("bootstrap"); print(r[["z_raw", "p_value", "flag"]].round(4).to_string())
for alt in ["greater", "less"]:
    r = m.test(test_method="poibin_exact", alternative=alt); print("exact", alt, r[["z_raw", "p_value", "flag"]].round(4).to_dict("list"))

print("\n== 12. Poisson-binomial pmf under the reference")
from scipy.stats import binom
pr0, pr1 = expit(g0), expit(g0 + beta)
def pmf(a, b):
    f = np.convolve(binom.pmf(np.arange(a + 1), a, pr0), binom.pmf(np.arange(b + 1), b, pr1)); return f
for k, nm in enumerate(names):
    f = pmf(n0[k], n1[k]); o = O[k]
    up = f[o + 1:].sum() + 0.5 * f[o]; lo = f[:o].sum() + 0.5 * f[o]
    E = n0[k] * pr0 + n1[k] * pr1; V = n0[k] * pr0 * (1 - pr0) + n1[k] * pr1 * (1 - pr1)
    print(nm, "E", round(E, 4), "V", round(V, 4), "sd", round(V ** .5, 4), "P(S=O)", round(f[o], 5), "P(S>=O)", round(f[o:].sum(), 5), "P(S<=O)", round(f[:o + 1].sum(), 5),
          "midp two-sided", round(2 * min(up, lo), 5), "score z", round((o - E) / V ** .5, 4))
    if nm in ("Alder", "Dune", "Elm"): print("   pmf", np.round(f, 4))

print("\n== 13. confidence intervals")
for tm in ["exact", "score", "wald"]:
    ci = m.calculate_confidence_intervals(option="gamma", test_method=tm); print(tm); print(ci["gamma_ci"].round(4).to_string())
for tm in ["exact", "score", "wald"]:
    ci = m.calculate_confidence_intervals(option="SM", stdz="indirect", measure="ratio", test_method=tm); print("ISR CI", tm); print(ci["indirect_ratio"].round(4).to_string())

print("\n== 14. funnel (score)")
fl = m.funnel_limits(); print(fl.providers[["observed", "expected", "estimate", "precision", "lower", "upper", "flag"]].round(4).to_string())
fle = m.funnel_limits(test_method="poibin_exact"); print(fle.providers[["observed", "expected", "estimate", "precision", "lower", "upper", "flag"]].round(4).to_string())
