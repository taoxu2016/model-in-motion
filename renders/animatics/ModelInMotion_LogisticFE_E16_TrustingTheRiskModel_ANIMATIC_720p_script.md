# Model in Motion · The Logistic Fixed-Effect Model · Episode 16: Trusting the Risk Model

*the same meter, on new groups*

Narration script with timestamps. 675 words, running time 04:45. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *Two hundred small meters in a grid, one per provider. Every one is level. A label: observed minus expected is zero for each.*

> [00:00.0] Every picture in the last act leaned on the risk model. So here is a comforting fact about it.  
> [00:05.9] For every one of our two hundred providers, observed equals expected, exactly. Every meter is level.  

**00:13.0 · s1_2** — *A second grid of two hundred meters beside the first, for a second crowd. These are level too.*

> [00:13.0] Here is a second crowd, fitted the same way. Its two hundred meters are level too.  
> [00:18.4] One of these two models is badly wrong. From here, you cannot tell which.  

**00:23.2 · s1_3** — *Across both grids: level by construction. Under them: a check that every model passes is no check.*

> [00:23.2] That is because the fit itself levels these meters. Episode 6 showed how: balancing is what fitting means.  
> [00:30.6] A check that every model passes is no check at all. We need to cut the patients another way.  

## S02_Title  (00:38)

**00:38.1 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:38.1] Welcome back to Model in Motion.  
> [00:40.3] Today: trusting the risk model.  

## S03_Tenths · Cut by risk  (00:44)

**00:44.7 · s3_1** — *A long strip for all 28,848 patients, in order of predicted risk, cut into ten equal parts. Under each part, a meter.*

> [00:44.7] Forget the providers for a moment. Line up all 28,848 patients by the risk the model gives them, from lowest to highest.  
> [00:55.2] Cut the line into ten equal groups, and give each group a meter of its own.  

**01:00.2 · s3_2** — *The first crowd's ten meters, each with its ratio: all between 0.95 and 1.05. Beside them, observed against expected for the ten groups, on the diagonal.*

> [01:00.2] For the first crowd, the ten meters barely tilt. Observed over expected runs from 0.95 to 1.05.  
> [01:09.8] Every one of those is within what luck allows. This model passes.  

## S04_Wrong · A model that is wrong  (01:15)

**01:16.6 · s4_1** — *The second crowd's ten meters. The first tips hard: 339 observed against 136 expected, a ratio of 2.50. The middle ones tip the other way: 0.77 to 0.79.*

> [01:16.6] Now the second crowd. In its lowest-risk tenth, the model expected 136 readmissions. There were 339: two and a half times as many.  
> [01:28.3] In the middle, the meters tilt the other way: more than a fifth fewer than expected.  

**01:33.3 · s4_2** — *The truth and the model, on the log-odds scale against the first risk factor: a curve that bends upward at both ends, and the straight line fitted to it.*

> [01:33.3] Here is what went wrong. In this crowd, risk does not rise in a straight line with the first risk factor. It bends: patients at either extreme are at higher risk than a straight line allows.  
> [01:45.7] The model was given a straight line, and did the best it could.  

**01:49.5 · s4_3** — *The ten meters again, after a squared term is added to the model: ratios from 0.92 to 1.08.*

> [01:49.5] Give it the bend, as a squared term, and the ten meters settle: from 0.92 to 1.08.  

## S05_Cost · What it cost  (01:58)

**01:58.5 · s5_1** — *Each provider's ratio under the wrong model against its ratio under the corrected one. Sixteen that change their flag are ringed. The fifth with the most unusual case mix are coloured: they sit to one side of the diagonal.*

> [01:58.5] Did the bend matter for the providers? It did. Between the two fits, 16 of the 200 change their flag.  
> [02:05.7] And the fifth of providers with the most unusual case mix had ratios 16% too high. They were being blamed for the model's mistake.  

## S06_AUC · What the AUC saw  (02:16)

**02:16.5 · s6_1** — *Four pairs of patients, one readmitted and one not, each with the risk the model gave them; three pairs are in the right order. Below, a thousand such pairs as coloured squares: 738 in the right order.*

> [02:16.5] There is a famous one-number summary of a risk model: the AUC. Take one patient who was readmitted and one who was not. The AUC is the chance that the model gave the first the higher risk.  

**02:29.8 · s6_2** — *Two bars on a scale from 0.5 to 1: the wrong model at 0.74, the corrected one at 0.76. Beside them, the lowest-risk tenth's ratio: 2.50.*

> [02:29.8] For the wrong model, it is 0.74. For the corrected one, 0.76.  
> [02:36.3] A tenth of the patients were off by a factor of two and a half, and the AUC barely noticed. It measures ranking, not whether the risks are right.  

**02:45.5 · s6_3** — *Two more bars for the first crowd: 0.72 from the risk factors alone, 0.74 with the provider terms.*

> [02:45.5] One more caution. In the first crowd, the AUC is 0.72 from the risk factors alone, and 0.74 once the model knows each patient's provider.  
> [02:57.8] That gain says providers differ. It does not say the risk rule got any better.  

## S07_Slope · One slope for all  (03:04)

**03:04.3 · s7_1** — *The largest provider, 484 patients. Two curves of risk against the first risk factor: the shared rule's, and this provider's own, twice as steep.*

> [03:04.3] A third cut: inside one provider. Our largest has 484 patients, and for them, in this experiment, risk climbs twice as steeply as the shared rule allows.  

**03:16.9 · s7_2** — *Three meters for this provider. All its patients: 143 against 143.0, level. Its lower-risk half: 18 against 41.2. Its higher-risk half: 125 against 101.8.*

> [03:16.9] Its total balances, as it must: 143 observed, 143 expected.  
> [03:24.1] But split its patients into a lower-risk half and a higher-risk half. 18 against 41. And 125 against 102.  

**03:33.9 · s7_3** — *A note: one gamma, an average over the patients this provider happens to treat.*

> [03:33.9] One gamma cannot describe this provider. It is an average over the patients it happens to treat, and a direct rate built on it would mislead.  

## S08_Limits · What no check sees  (03:44)

**03:44.4 · s8_1** — *A card of checks the software runs before fitting: missing values; a risk factor that never varies; pairs correlated above 0.9; variance inflation above 10.*

> [03:44.4] Software can catch some trouble before fitting: missing values, a risk factor that never varies, two that say nearly the same thing.  

**03:53.1 · s8_2** — *Two cards: a risk factor nobody recorded, which no check can see; and a consequence of care used as a risk factor, which adjusts performance away.*

> [03:53.1] But every check today compared the model with data we have. None can see a risk factor that nobody recorded.  
> [04:00.1] And more is not always better. Adjust for something a provider causes, such as a complication, and you adjust its performance away.  

## S09_Recap · Recap  (04:10)

**04:10.7 · s9_1** — *Three recap cards, each with a small icon.*

> [04:10.7] Let's gather it up.  
> [04:12.2] Provider meters are level by construction. They prove nothing.  
> [04:16.4] So take the same meter to new groups: tenths of risk, and halves within a provider.  
> [04:21.7] And the AUC measures ranking, not fairness.  

**04:24.8 · s9_2** — *A row of providers, each with its own separate estimate; then the small ones drawn toward a common line. The next episode's title.*

> [04:24.8] Throughout this series, each provider has had a number of its own, estimated on its own. Many analysts would do it differently, and pull the small providers toward the average.  
> [04:35.9] Next time: fixed or random?  

**04:38.4 · s9_3** — *Series end card with the next episode title.*

> [04:38.4] This has been Model in Motion. Thanks for following the story.  
