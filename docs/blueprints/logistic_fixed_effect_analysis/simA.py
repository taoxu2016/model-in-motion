import numpy as np, pandas as pd, warnings, logging, time
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit, logit
from scipy.stats import spearmanr, norm
import statsmodels.api as smapi
from crowd import *
np.set_printoptions(precision=4, suppress=True, linewidth=160)
D = design(); n = D["n"]; mu = D["mu"]
df, gamma = outcomes(D, 0.3)
f = fit(df); bh = np.ravel(f.coefficients_["beta"]); gh = np.ravel(f.coefficients_["gamma"])
print("== crowd (tau=0.3): N", len(df), "events", df.y.sum(), "rate", round(df.y.mean(), 4))
raw = df.groupby("prov").y.mean().to_numpy()
print("\n== M1: raw rates vs true effects")
print("spearman(raw, gamma_true)", spearmanr(raw, gamma)[0], "spearman(raw, case mix mu)", spearmanr(raw, mu)[0], "spearman(gamma_hat, gamma_true)", spearmanr(gh, gamma)[0])
q = lambda v: pd.qcut(pd.Series(v).rank(method="first"), 5, labels=False).to_numpy()
qr, qt, qh = q(raw), q(gamma), q(gh)
print("providers whose raw-rate quintile differs from true-effect quintile:", (qr != qt).sum(), "by 2+ quintiles:", (np.abs(qr - qt) >= 2).sum())
print("same for gamma_hat:", (qh != qt).sum(), "by 2+:", (np.abs(qh - qt) >= 2).sum())
top_raw = set(np.argsort(-raw)[:20]); top_true = set(np.argsort(-gamma)[:20]); top_hat = set(np.argsort(-gh)[:20])
print("worst-20 by raw rate that are in true worst-20:", len(top_raw & top_true), "; worst-20 by gamma_hat in true worst-20:", len(top_hat & top_true))
print("raw rate range", raw.min().round(3), raw.max().round(3))

print("\n== M3/M4: pooled vs fixed-effect risk rule (truth 0.8, 0.5)")
pm = smapi.Logit(df.y, smapi.add_constant(df[["x1", "x2"]])).fit(disp=0)
print("pooled:", pm.params.values.round(4), "se", pm.bse.values.round(4))
print("FE    :", bh.round(4), "se", np.sqrt(np.diag(f.variances_["beta"])).round(4))
# pooled O/E vs FE ISR vs truth
ppool = pm.predict(smapi.add_constant(df[["x1", "x2"]]))
O = df.groupby("prov").y.sum().to_numpy(); Epool = pd.Series(ppool).groupby(df.prov).sum().to_numpy()
sm = f.calculate_standardized_measures(stdz=["indirect", "direct"])
isr = sm["indirect"].indirect_ratio.to_numpy(); dsr = sm["direct"].direct_ratio.to_numpy()
# true ISR-like quantity: expected at true gamma_i / expected at true median gamma, on own patients with true beta
xb_true = BETA[0] * df.x1.to_numpy() + BETA[1] * df.x2.to_numpy(); prov = df.prov.to_numpy()
g0_true = np.median(gamma)
true_ratio = np.bincount(prov, weights=expit(gamma[prov] + xb_true)) / np.bincount(prov, weights=expit(g0_true + xb_true))
big = n >= 100
print("corr of log(O/E_pooled error) with case mix (n>=100):", np.corrcoef(np.log(O[big] / Epool[big]) - np.log(true_ratio[big]), mu[big])[0, 1].round(3),
      "; FE ISR error with case mix:", np.corrcoef(np.log(isr[big]) - np.log(true_ratio[big]), mu[big])[0, 1].round(3))
hi = mu > np.quantile(mu, 0.8); lo = mu < np.quantile(mu, 0.2)
print("mean O/E_pooled / true ratio: sickest fifth", np.exp(np.mean(np.log(O[hi & (O>0)] / Epool[hi & (O>0)]) - np.log(true_ratio[hi & (O>0)]))).round(3),
      "healthiest fifth", np.exp(np.mean(np.log(O[lo & (O>0)] / Epool[lo & (O>0)]) - np.log(true_ratio[lo & (O>0)]))).round(3))
print("mean FE ISR / true ratio: sickest fifth", np.exp(np.mean(np.log(isr[hi & (O>0)]) - np.log(true_ratio[hi & (O>0)]))).round(3),
      "healthiest fifth", np.exp(np.mean(np.log(isr[lo & (O>0)]) - np.log(true_ratio[lo & (O>0)]))).round(3))

print("\n== M9: SE vs size")
se = np.sqrt(np.ravel(f.variances_["gamma_case_mix"])); info = np.bincount(prov, weights=f.fitted_ * (1 - f.fitted_))
sl = np.polyfit(np.log(n), np.log(se), 1); print("slope of log SE on log n", sl.round(3), "corr(log se, -0.5 log info)", np.corrcoef(np.log(se), -0.5 * np.log(info))[0, 1].round(4))
for a, b_ in ((20, 30), (90, 110), (400, 500)):
    k = (n >= a) & (n <= b_); print(f"  sizes {a}-{b_}: n providers {k.sum()}, median SE {np.median(se[k]):.3f}, median info per patient {np.median(info[k] / n[k]):.3f}")
print("  1/sqrt(n*wbar) at n=25,100,450 with wbar", (info.sum() / n.sum()).round(4), ":", (1 / np.sqrt(np.array([25, 100, 450]) * info.sum() / n.sum())).round(3))
print("  max ratio own-info SE / total SE", (1 / np.sqrt(info) / se).min().round(4), (1 / np.sqrt(info) / se).max().round(4))

print("\n== M11/M12: indirect vs direct in the crowd")
print("corr(ISR, DSR)", np.corrcoef(isr, dsr)[0, 1].round(4), "spearman", spearmanr(isr, dsr)[0].round(4))
g0 = np.median(gh); dsr0 = dsr / (np.sum(expit(g0 + f.xbeta_)) / df.y.sum())      # direct ratio relative to the reference's direct ratio
rk_i = pd.Series(isr).rank().to_numpy(); rk_d = pd.Series(dsr).rank().to_numpy()
print("reference DSR", (np.sum(expit(g0 + f.xbeta_)) / df.y.sum()).round(4), "largest rank change", int(np.max(np.abs(rk_i - rk_d))), "providers moving 10+ ranks", int((np.abs(rk_i - rk_d) >= 10).sum()))
print("corr(log ISR - log DSR0, case mix mu) among O>0:", np.corrcoef((np.log(isr) - np.log(dsr0))[O > 0], mu[O > 0])[0, 1].round(3))
print("ISR range", isr.min().round(3), isr.max().round(3), "median", np.median(isr).round(3))
