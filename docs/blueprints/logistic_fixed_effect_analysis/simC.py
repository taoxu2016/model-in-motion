import numpy as np, pandas as pd, warnings, logging, time
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit
from crowd import *
from pprof_py.utils.metrics import roc_auc_score
np.set_printoptions(precision=3, suppress=True, linewidth=170)
D = design(); n = D["n"]; mu = D["mu"]
df, gamma = outcomes(D, 0.3); f = fit(df)
def deciles(y, p):
    q = pd.qcut(pd.Series(p).rank(method="first"), 10, labels=False)
    t = pd.DataFrame({"y": y, "p": p, "q": q}).groupby("q").agg(O=("y", "sum"), E=("p", "sum"), n=("y", "size"), pbar=("p", "mean"))
    t["OE"] = t.O / t.E; t["z"] = (t.O - t.E) / np.sqrt(pd.DataFrame({"v": p * (1 - p), "q": q}).groupby("q").v.sum()); return t
print("== M16 (a) well-specified crowd"); t = deciles(df.y.to_numpy(), f.fitted_); print(t.round(3).to_string())
print("AUC", round(f.auc_, 4), " O/E range", t.OE.min().round(3), t.OE.max().round(3), "max |z|", np.abs(t.z).max().round(2))
# AUC without provider effects & with only provider effects
import statsmodels.api as smapi
pm = smapi.Logit(df.y, smapi.add_constant(df[["x1", "x2"]])).fit(disp=0); print("AUC pooled (no provider effects)", round(roc_auc_score(df.y.to_numpy(), pm.predict(smapi.add_constant(df[["x1", "x2"]])).to_numpy()), 4))
raw = df.groupby("prov").y.transform("mean").to_numpy(); print("AUC of provider raw rate alone", round(roc_auc_score(df.y.to_numpy(), raw), 4))

print("\n== M16 (b) wrong functional form: truth has + 0.3*(x1^2 - 1) on the log-odds scale; fitted linear in x1")
rng = np.random.default_rng(D["seed"] + 5)
prov = D["prov"]; g = gamma
eta = g[prov] + 0.8 * D["x1"] + 0.3 * (D["x1"] ** 2 - 1) + 0.5 * D["x2"]
yq = (rng.random(prov.size) < expit(eta)).astype(int)
dq = pd.DataFrame({"y": yq, "x1": D["x1"], "x2": D["x2"], "x1sq": D["x1"] ** 2, "prov": prov})
f1 = fit(dq); f2 = fit(dq, xv=("x1", "x2", "x1sq"))
t1 = deciles(yq, f1.fitted_); t2 = deciles(yq, f2.fitted_)
print("linear fit: O/E by decile", t1.OE.round(3).to_numpy(), "max |z|", np.abs(t1.z).max().round(2), "AUC", round(f1.auc_, 4))
print("with x1^2 : O/E by decile", t2.OE.round(3).to_numpy(), "max |z|", np.abs(t2.z).max().round(2), "AUC", round(f2.auc_, 4))
print("beta linear fit", np.ravel(f1.coefficients_["beta"]).round(3), "beta with square", np.ravel(f2.coefficients_["beta"]).round(3))
# residual smoother against x1: mean (y - p) in bins of x1
bins = pd.cut(dq.x1, [-10, -1.5, -0.5, 0.5, 1.5, 10])
r1 = pd.DataFrame({"r": yq - f1.fitted_, "p": f1.fitted_, "y": yq, "b": bins}).groupby("b").agg(O=("y", "sum"), E=("p", "sum"), n=("y", "size")); r1["OE"] = r1.O / r1.E
r2 = pd.DataFrame({"r": yq - f2.fitted_, "p": f2.fitted_, "y": yq, "b": bins}).groupby("b").agg(O=("y", "sum"), E=("p", "sum"), n=("y", "size")); r2["OE"] = r2.O / r2.E
print("O/E by x1 band, linear fit:", r1.OE.round(3).to_numpy(), " with square:", r2.OE.round(3).to_numpy())
e1 = f1.test(test_method="poibin_exact").flag.to_numpy().astype(float); e2 = f2.test(test_method="poibin_exact").flag.to_numpy().astype(float)
print("flags linear", int((e1 != 0).sum()), "flags with square", int((e2 != 0).sum()), "providers whose flag changes", int((e1 != e2).sum()))
i1 = f1.calculate_standardized_measures()["indirect"].indirect_ratio.to_numpy(); i2 = f2.calculate_standardized_measures()["indirect"].indirect_ratio.to_numpy()
ok = (i1 > 0) & (i2 > 0); spread = np.array([D["x1"][prov == k].var() + 0 for k in range(M)]); ext = np.array([np.mean(np.abs(D["x1"][prov == k]) > 1.5) for k in range(M)])
print("corr(log ISR_linear - log ISR_square, |case mix|)", np.corrcoef((np.log(i1) - np.log(i2))[ok], np.abs(mu)[ok])[0, 1].round(3), "; with share of extreme patients", np.corrcoef((np.log(i1) - np.log(i2))[ok], ext[ok])[0, 1].round(3))
far = np.abs(mu) > np.quantile(np.abs(mu), 0.8)
print("mean ISR_linear / ISR_square for the fifth with the most unusual case mix:", np.exp(np.mean((np.log(i1) - np.log(i2))[ok & far])).round(3), "; others:", np.exp(np.mean((np.log(i1) - np.log(i2))[ok & ~far])).round(3))

print("\n== M16 (c) one provider with a steeper slope (1.6 instead of 0.8) for x1")
big = int(np.argmax(n)); rng = np.random.default_rng(D["seed"] + 6)
dfc = df.copy(); k = (prov == big)
eta_b = gamma[big] - 0.35 + 1.6 * D["x1"][k] + 0.5 * D["x2"][k]
dfc.loc[k, "y"] = (rng.random(k.sum()) < expit(eta_b)).astype(int)
fc = fit(dfc); pk = fc.fitted_[k]; yk = dfc.y.to_numpy()[k]; xk = D["x1"][k]
lo = xk < np.median(D["x1"]); print("provider size", k.sum(), "total O", yk.sum(), "total E", pk.sum().round(3))
print("low-risk half:  n", lo.sum(), "O", yk[lo].sum(), "E", pk[lo].sum().round(2), "| high-risk half: n", (~lo).sum(), "O", yk[~lo].sum(), "E", pk[~lo].sum().round(2))
ter = pd.qcut(xk, 3, labels=False); print("by tercile of x1: O", [int(yk[ter == j].sum()) for j in range(3)], "E", [round(float(pk[ter == j].sum()), 1) for j in range(3)])
