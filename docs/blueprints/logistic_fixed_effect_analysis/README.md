# The scripts behind the blueprint's numbers

These scripts computed the numbers in the logistic fixed-effect blueprint (`../logistic_fixed_effect_blueprint.md`):
the five-clinic cast with its fits, tests, intervals and standardized measures, and every simulation of the crowd of
200 providers. They call pprof_py 0.7.0 itself, and check the cast's fit against statsmodels and scikit-learn. They were
written on 23 November 2026, while the blueprint was drafted, and are kept as they were run, exploratory printing
included. A few illustrative figures in the blueprint are plain arithmetic and have no script here.

`output/` holds what each script prints, from a re-run on 25 November 2026 with the versions pinned in
`requirements.txt`. Every script ran without error, and the figures spot-checked against the blueprint all reproduce,
from β̂ = 2.0164 for the cast to the flag rates of the τ experiment. Only the timings printed by `simB.py` and
`simG.py` change from run to run.

## Run

From this folder, after `pip install -r requirements.txt` at the repository root:

    python cast_full.py > output/cast_full.txt

The cast scripts import `cast.py`, and the `sim*.py` scripts import `crowd.py`, both from this folder.

## What each script computes

| Script | Blueprint | What it prints | Run time |
| --- | --- | --- | --- |
| `cast.py` | The running example | The cast as one row per patient (`build()`, used by the other cast scripts) and a first fit | 4 s |
| `cast_full.py` | Appendix: cast fit, per-clinic data and fit, measures and tests, null distributions | Pooled and fixed-effect fits with cross-checks, information and standard errors, the three tests of β, the profile log-likelihood, standardized measures, provider tests and intervals, exact null distributions, funnel limits | 5 s |
| `trace.py` | Appendix: iterations for M6 to M8; M7, M8 and M10 variants | SerBIN and BAN step by step from pprof_py's start, the first step's scores and information, and where Elm's estimate stops under each algorithm and tolerance | 19 s |
| `extra.py` | M1, M5, M7, M9 and M10 variants | Mantel–Haenszel, the case-mix swap, odds-ratio translations, recentring, one-dimensional Newton steps, screening (Fen), binomial rows, the Wald variance against the covariate's origin | 2 s |
| `crowd.py` | Simulation specifications | The crowd generator (seed 2026) that every `sim*.py` uses, and a summary of the crowd | 1 s |
| `simA.py` | M1, M3–M4, M9, M11–M12 | Raw rates against true effects, pooled against fixed-effect slopes, standard error against size, indirect against direct ratios | 2 s |
| `simB.py` | M13–M15 | The level crowd's flags and funnel, and the calibration of the exact, score and Wald tests over 100 replicate crowds | 85 s |
| `simC.py` | M16 | Calibration by risk decile, the AUC, a wrong functional form, a provider with a steeper slope | 4 s |
| `simD.py` | M17 | Fixed against random effects (pprof_py's `LogisticRandomEffectModel`), with and without a link to case mix | 5 s |
| `simE.py` | M18 | The joint fit's bias by provider size, against conditional logistic regression (statsmodels) | 160 s |
| `simF.py` | M19 | The τ knob, pprof_py's empirical null, the widened funnel, 20 replicate crowds | 44 s |
| `simG.py` | M8 | SerBIN against BAN against a dummy-variable GLM, and a fit of 2,000 providers | 6 s |

Run times are from the re-run, on one core.

## Relation to `mim/`

The episodes' numbers files use `mim/castfit.py` and `mim/crowd.py`, which need only numpy and scipy, so that an
episode can be checked without pprof_py. `mim/crowd.py` draws the same crowd as `crowd.py` here: on the re-run, the two gave identical sizes, case mix,
covariates, effects and outcomes.
