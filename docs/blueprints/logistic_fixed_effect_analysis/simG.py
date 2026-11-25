import numpy as np, pandas as pd, warnings, logging, time
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit
import statsmodels.api as smapi
from crowd import *
D = design(); df, gamma = outcomes(D, 0.3)
t0 = time.time(); f = fit(df); t_ser = time.time() - t0
t0 = time.time(); fb = fit(df, algorithm="Ban"); t_ban = time.time() - t0
print("crowd: SerBIN", round(t_ser, 3), "s, iters", f.algorithm.iter, "| BAN", round(t_ban, 3), "s, iters", fb.algorithm.iter,
      "| max diff beta", np.max(np.abs(np.ravel(f.coefficients_["beta"]) - np.ravel(fb.coefficients_["beta"]))), "gamma", np.max(np.abs(np.ravel(f.coefficients_["gamma"]) - np.ravel(fb.coefficients_["gamma"]))))
Xd = np.c_[np.eye(M)[df.prov.to_numpy()], df[["x1", "x2"]].to_numpy()]
t0 = time.time(); g = smapi.GLM(df.y.to_numpy(), Xd, family=smapi.families.Binomial()).fit(tol=1e-12, maxiter=100); t_glm = time.time() - t0
print("statsmodels GLM with 200 dummy columns:", round(t_glm, 2), "s; max |diff| beta", np.max(np.abs(g.params[M:] - np.ravel(f.coefficients_["beta"]))), "gamma", np.max(np.abs(g.params[:M] - np.ravel(f.coefficients_["gamma"]))),
      "; SE beta diff", np.max(np.abs(g.bse[M:] - np.sqrt(np.diag(f.variances_["beta"])))), "SE gamma diff", np.max(np.abs(g.bse[:M] - np.sqrt(np.ravel(f.variances_["gamma"])))))
print("matrix cells: crowd (m+p)^2 =", (M + 2) ** 2, "non-zero:", M + 2 * 2 * M + 4)
# larger problem
rng = np.random.default_rng(2026); m2, p2 = 2000, 5; n2 = rng.integers(50, 151, m2); prov = np.repeat(np.arange(m2), n2)
X = rng.normal(size=(prov.size, p2)); b2 = np.array([0.5, -0.4, 0.3, 0.2, -0.1]); g2 = rng.normal(-1.2, 0.4, m2)
y = (rng.random(prov.size) < expit(g2[prov] + X @ b2)).astype(int)
d2 = pd.DataFrame(X, columns=[f"x{k}" for k in range(p2)]); d2["y"] = y; d2["prov"] = prov
t0 = time.time(); f2 = fit(d2, xv=[f"x{k}" for k in range(p2)]); t2 = time.time() - t0
print(f"2,000 providers, {prov.size} patients, 5 covariates: SerBIN {t2:.2f} s, iters {f2.algorithm.iter}; dense design would hold {prov.size * (m2 + p2) * 8 / 1e9:.1f} GB; information matrix {(m2 + p2) ** 2:,} cells, Schur complement {p2 * p2} cells")
print("national scale 7,000 providers, 50 covariates: (m+p)^2 =", f"{7050 ** 2:,}", "; p^2 =", 50 * 50)
