import numpy as np, pandas as pd, warnings, logging, time
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit
from scipy.stats import spearmanr
from crowd import *
from pprof_py import LogisticRandomEffectModel
np.set_printoptions(precision=4, suppress=True, linewidth=160)
D = design(); n = D["n"]; mu = D["mu"]; planted = np.r_[D["pos"], D["neg"]]
df, gamma = outcomes(D, 0.3)
f = fit(df); bh = np.ravel(f.coefficients_["beta"]); gh = np.ravel(f.coefficients_["gamma"])
t0 = time.time(); re = LogisticRandomEffectModel().fit(df, y_var="y", x_vars=["x1", "x2"], provider_var="prov"); print("RE fit time", round(time.time() - t0, 1))
print("RE coefficient keys", list(re.coefficients_.keys()))
for k, v in re.coefficients_.items():
    if k != "alpha": print(" ", k, np.round(np.ravel(np.asarray(v, dtype=float)), 4) if not isinstance(v, dict) else v)
a = re.coefficients_["alpha"]["prov"].to_numpy(); sig = re.sigma_["prov"]
print("sigma_hat", round(float(sig), 4), "true SD of gamma (incl. planted)", gamma.std().round(4), "SD of alpha_hat", a.std().round(4), "SD of gamma_hat", gh.std().round(4))
print("FE beta", bh.round(4), "truth", BETA)
# errors relative to the truth, on a common centring (deviation from the size-weighted mean of true gamma)
gt = gamma - np.average(gamma, weights=n)
fe_dev = gh - np.average(gh, weights=n); re_dev = a - np.average(a, weights=n)
small = n < 50; large = n >= 200
for nm, k in (("all", np.ones(M, bool)), ("n<50", small), ("n>=200", large)):
    print(f"{nm:7s} RMSE FE {np.sqrt(np.mean((fe_dev[k] - gt[k]) ** 2)):.3f}  RE {np.sqrt(np.mean((re_dev[k] - gt[k]) ** 2)):.3f}")
print("corr(error, case mix): FE", np.corrcoef(fe_dev - gt, mu)[0, 1].round(3), " RE", np.corrcoef(re_dev - gt, mu)[0, 1].round(3))
hi = mu > np.quantile(mu, 0.8); lo = mu < np.quantile(mu, 0.2)
print("mean error (estimate - truth): sickest fifth FE", (fe_dev - gt)[hi].mean().round(3), "RE", (re_dev - gt)[hi].mean().round(3), "| healthiest fifth FE", (fe_dev - gt)[lo].mean().round(3), "RE", (re_dev - gt)[lo].mean().round(3))
# reliability and shrinkage
se2 = np.ravel(f.variances_["gamma"]); rho = sig ** 2 / (sig ** 2 + se2)
print("reliability rho: n<50 median", np.median(rho[small]).round(3), "n>=200 median", np.median(rho[large]).round(3))
shr = rho * (gh - np.average(gh, weights=1 / (sig ** 2 + se2))); print("corr(BLUP, rho*(gamma_hat - mean))", np.corrcoef(a, shr)[0, 1].round(4))
# flags
fe_ex = f.test(test_method="poibin_exact").flag.to_numpy().astype(float); re_w = re.test(test_method="wald").flag.to_numpy().astype(float)
print("flags: FE exact", int((fe_ex != 0).sum()), "RE wald", int((re_w != 0).sum()))
print("planted sizes", n[planted], "FE flags", fe_ex[planted], "RE flags", re_w[planted])
print("planted: gamma_hat dev", fe_dev[planted].round(2), "RE dev", re_dev[planted].round(2), "truth", gt[planted].round(2))
# Dune-like illustration: reliability at SE 0.66 and sigma_hat
print("example reliability at SE=0.66:", round(float(sig ** 2 / (sig ** 2 + 0.66 ** 2)), 3), "at SE=0.12:", round(float(sig ** 2 / (sig ** 2 + 0.12 ** 2)), 3))

print("\n== same comparison with tau=0.3 but no correlation with case mix (rho=0)")
import crowd
D0 = design(); D0["u"] = np.random.default_rng(777).normal(size=M)
df0, gamma0 = outcomes(D0, 0.3)
f0 = fit(df0); re0 = LogisticRandomEffectModel().fit(df0, y_var="y", x_vars=["x1", "x2"], provider_var="prov")
a0 = re0.coefficients_["alpha"]["prov"].to_numpy(); g0h = np.ravel(f0.coefficients_["gamma"])
gt0 = gamma0 - np.average(gamma0, weights=n); fe0 = g0h - np.average(g0h, weights=n); re0d = a0 - np.average(a0, weights=n)
for k, v in re0.coefficients_.items():
    if k != "alpha": print(" RE", k, np.round(np.ravel(np.asarray(v, dtype=float)), 4))
print(" FE beta", np.ravel(f0.coefficients_["beta"]).round(4), "corr(gamma, mu)", np.corrcoef(gamma0, mu)[0, 1].round(3))
for nm, k in (("all", np.ones(M, bool)), ("n<50", small), ("n>=200", large)):
    print(f" {nm:7s} RMSE FE {np.sqrt(np.mean((fe0[k] - gt0[k]) ** 2)):.3f}  RE {np.sqrt(np.mean((re0d[k] - gt0[k]) ** 2)):.3f}")
print(" corr(error, case mix): FE", np.corrcoef(fe0 - gt0, mu)[0, 1].round(3), " RE", np.corrcoef(re0d - gt0, mu)[0, 1].round(3))
