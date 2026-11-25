import numpy as np, pandas as pd, warnings, logging, time
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit
from pprof_py import LogisticFixedEffectModel
from statsmodels.discrete.conditional_models import ConditionalLogit
rng = np.random.default_rng(2026)
print("== M18 incidental parameters: 4,000 patients, beta=0.5, gamma_i ~ N(-0.5, 1), x ~ N(0,1); 100 replicates")
R = 100
for size in (2, 5, 10, 25, 100):
    est, cov, cest, ccov, sef = [], [], [], [], []
    for rep in range(R):
        m_s = 4000 // size; prov = np.repeat(np.arange(m_s), size); x = rng.normal(size=prov.size)
        y = rng.binomial(1, expit(rng.normal(-0.5, 1, m_s)[prov] + 0.5 * x))
        f = LogisticFixedEffectModel(use_dataprep=False).fit(pd.DataFrame({"y": y, "x": x, "p": prov}), y_var="y", x_vars=["x"], provider_var="p")
        b = float(np.ravel(f.coefficients_["beta"])[0]); se = float(np.sqrt(f.variances_["beta"][0, 0]))
        est.append(b); cov.append(abs(b - 0.5) < 1.96 * se); sef.append(se)
        if rep < 40:
            cl = ConditionalLogit(y, x[:, None], groups=prov).fit(disp=0)
            cest.append(float(cl.params[0])); ccov.append(abs(cl.params[0] - 0.5) < 1.96 * cl.bse[0])
    print(f"size {size:3d} ({4000 // size:4d} providers): joint ML mean beta_hat/beta {np.mean(est) / 0.5:.3f}, coverage {np.mean(cov):.2f}, mean SE {np.mean(sef):.3f} | conditional ML {np.mean(cest) / 0.5:.3f}, coverage {np.mean(ccov):.2f}")
