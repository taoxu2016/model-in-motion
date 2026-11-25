import numpy as np, pandas as pd, warnings, logging
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit, logit
from pprof_py import LogisticFixedEffectModel

BETA = np.array([0.8, 0.5]); G0 = -1.5; RHO = -0.6; SD_MU = 0.6; M = 200
def design(seed=2026, m=M, lo=20, hi=500):
    """Fixed part of the crowd: sizes, case mix, covariates, standardised provider deviations, planted outliers."""
    rng = np.random.default_rng(seed)
    n = np.round(np.exp(rng.uniform(np.log(lo), np.log(hi), m))).astype(int)
    mu = rng.normal(0, SD_MU, m)
    eps = rng.normal(size=m)
    u = RHO * mu / SD_MU + np.sqrt(1 - RHO ** 2) * eps            # unit-variance deviation, corr RHO with case mix
    prov = np.repeat(np.arange(m), n)
    x1 = rng.normal(mu[prov], 1.0); x2 = rng.binomial(1, 0.3, prov.size).astype(float)
    order = np.argsort(n, kind="stable")
    # planted outliers: three above, three below, at small / middle / large sizes
    pos = [order[int(q * (m - 1))] for q in (0.15, 0.50, 0.85)]
    neg = [order[int(q * (m - 1)) + 1] for q in (0.15, 0.50, 0.85)]
    return dict(n=n, mu=mu, u=u, prov=prov, x1=x1, x2=x2, pos=np.array(pos), neg=np.array(neg), seed=seed)
def outcomes(D, tau=0.3, seed_y=None, plant=0.8):
    rng = np.random.default_rng(D["seed"] + 1 if seed_y is None else seed_y)
    gamma = G0 + tau * D["u"]
    gamma[D["pos"]] = G0 + plant; gamma[D["neg"]] = G0 - plant
    eta = gamma[D["prov"]] + BETA[0] * D["x1"] + BETA[1] * D["x2"]
    y = (rng.random(D["prov"].size) < expit(eta)).astype(int)
    df = pd.DataFrame({"y": y, "x1": D["x1"], "x2": D["x2"], "prov": D["prov"]})
    return df, gamma
def fit(df, xv=("x1", "x2"), **kw):
    return LogisticFixedEffectModel(use_dataprep=False, **kw).fit(df, y_var="y", x_vars=list(xv), provider_var="prov")

if __name__ == "__main__":
    D = design(); n = D["n"]
    print("providers", M, "patients", n.sum(), "size min/median/max", n.min(), np.median(n), n.max(), "under 50:", (n < 50).sum(), "over 200:", (n > 200).sum())
    print("planted + sizes", n[D["pos"]], "planted - sizes", n[D["neg"]])
    for tau in (0.0, 0.3):
        df, gamma = outcomes(D, tau)
        f = fit(df)
        b = np.ravel(f.coefficients_["beta"]); g = np.ravel(f.coefficients_["gamma"])
        print(f"tau={tau}: events {df.y.sum()} rate {df.y.mean():.4f}; beta_hat {b.round(4)} se {np.sqrt(np.diag(f.variances_['beta'])).round(4)}; iters {f.algorithm.iter}; "
              f"no-event providers {(df.groupby('prov').y.sum() == 0).sum()}; SD true gamma {gamma.std():.3f}; SD gamma_hat {g.std():.3f}; corr(gamma, mu) {np.corrcoef(gamma, D['mu'])[0,1]:.3f}")
