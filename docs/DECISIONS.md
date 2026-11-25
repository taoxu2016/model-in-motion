# Open decisions, by episode

Each script review ends with the choices it needs from its reader. They are gathered here so that all of them can be
settled in one sitting: 86 choices across fifteen draft scripts, as the reviews stood on 25 November 2026.

The review docs are the working copies. If a doc has moved on, the doc is right and this file is stale. Scene numbers
(S03, S07) refer to the scenes of that episode; “the blueprint” is `docs/blueprints/logistic_fixed_effect_blueprint.md`.

Episode 4's script was approved as written, so its review left nothing open ([review doc](https://claude.ai/artifact/CTx3BUU8yhMrfH7d3cWDab)).
Its voice does share the pronunciation question under “Across episodes”. Episodes 1 to 3 are finished.

## Across episodes

One choice, found by a check of the repository on 25 November 2026 rather than by a script review.

| Question | What the voice does now | Alternative |
| --- | --- | --- |
| How “readmissions” sounds | Episodes 2 and 3 respell it “re-admissions” in `pronunciations`. Episodes 4 to 19 respell only “readmission” and “readmitted”, and a respelling matches whole words only, so 28 sentences were voiced from the plain spelling: 3 in Episode 4, 3 in 5, 2 in 6, 6 in 10, 4 in 11, 3 in 12, 4 in 13, and 1 each in 14, 16 and 18. No person has heard them yet. | Listen first: the first sentence of Episode 3 (“8 expected readmissions”) against Episode 4's animatic at 0:20 (“no readmissions at all”). If the plain word sounds wrong, add `"readmissions": "re-admissions"` to those ten episodes' `pronunciations` and `/revoice` each; only the 28 sentences are re-voiced. Episode 4's script is approved, so its change needs your word. |

## Episode 5 · Reading γ

[Review doc](https://claude.ai/artifact/L35SjQNzgRoUE8gbUHJrXp) · 6 choices

Six choices need your call. The first changes how strong the episode's opening argument is.

| Question | What the draft does | Alternative |
| --- | --- | --- |
| How reading one is rejected | With raw counts: 13 of 30 against 8 of 20, 43% against 40%. Simple, and it recalls Episode 1. | With the model: Alder's own 30 patients would have 8.0 readmissions at Cedar's level against 13, a ratio of 1.6. Stronger, and it previews the standardized ratio. |
| Script and animatic together | The animatic is built before your read, so words and pictures are judged at once. A changed sentence is re-voiced alone. | Script first, animatic only after approval, as for Episode 4. |
| Beats left out | The β card and “what γ contains” are in Episode 4 and are not repeated. | A 20-second recall of either. |
| The averages warning | Kept: three clips, about 45 seconds. It is the hardest idea in the episode. | Move it to the episode on direct standardization (M12) and finish near 4½ minutes. |
| “Went to Cedar” | Plain hypothetical, with “the model says”. | “Had Cedar's level”: more exact, less natural. |
| The rare-event sentence | One sentence in s4_3. | Cut it and save about 6 seconds. |

## Episode 6 · Fitting by Balance

[Review doc](https://claude.ai/artifact/Lq7j8V32pEEta8nK1GRxy2) · 6 choices

Six choices need your call. The first two shape how the whole fitting act will sound.

| Question | What the draft does | Alternative |
| --- | --- | --- |
| The word for log-likelihood | “Height” in the narration, from S03 on. “Likelihood” is said once; “log-likelihood” appears only as a label under the bar. | Say “log-likelihood” throughout, as Episodes 7 to 9 will need the term. |
| Length | About 4¾ minutes for the module the blueprint calls the hub and budgets at 12. | Add a worked product for one clinic's chips to S03, about 40 seconds. |
| Which clinic shows one slider | Dune: the clearest tilt at the plain guess, +2.11. | Alder, the cast's lead, whose meter starts at only +0.77. |
| The hill | A 30-second closing picture that sets up Episode 7. | Move it to Episode 7's opening. |
| Beats left out | The dome over two covariates, and rows with N trials. | A short scene for either. |
| Script and animatic together | As for Episode 5: built in one pass, reviewed together. | Script first, animatic after approval. |

## Episode 7 · Climbing the Hill

[Review doc](https://claude.ai/artifact/AFCL9pJNsfSMQhcjTJs7mQ) · 5 choices

Five choices need your call. The first two set vocabulary that later episodes inherit.

| Question | What the draft does | Alternative |
| --- | --- | --- |
| The word for V | “Wobble”, in S04 and the recap, after the blueprint. | “Information” or “variance”, the words Episodes 9 and 14 will need. |
| Naming the methods | Neither “Newton” nor “BAN” is spoken or shown. | Name both once, for viewers who will meet them in the package's options. |
| Which routine the machine shows | Plain alternation in the 0-and-1 coding, 54 rounds, with pprof_py's centring told afterwards. | Show the centred routine from the start: 21 rounds, but slider values in centred units. |
| Backtracking | Left out. | One clip: a step that would overshoot is shortened. |
| Episode 8 | The last line promises the arrow matrix, an Extended module in the blueprint. | If Episode 8 is skipped, re-voice the line to point at Episode 9. |

## Episode 8 · The Arrow Matrix

[Review doc](https://claude.ai/artifact/L7TPKgtpLP3h5QC7gpTAC6) · 5 choices

Five choices need your call. The first is whether this episode should exist at all.

| Question | What the draft does | Alternative |
| --- | --- | --- |
| An Extended module as a full episode | Produced at about 4¾ minutes, because Episode 7 ended by promising it. | Fold S03 to S05 into Episode 9 as a two-minute prologue, and re-voice Episode 7's last line. |
| Naming | “The arrow matrix” is said. “Information matrix” is a small label. “SerBIN” is neither said nor shown. | Show “SerBIN” beside the step counter, since it is the package's default method. |
| Depth of the fold | A spoken recipe with its meaning; no matrix formula. | Add the blueprint's two block formulas as a closing card for methodologists. |
| The warning in S05 | “Three and a half times as much about the dial.” | As an interval: “almost twice too narrow”. |
| The timing claim | “Well under a second”, from a run in this sandbox. | Drop the timing and keep only the 3.3 GB comparison. |

## Episode 9 · How Sure Are We?

[Review doc](https://claude.ai/artifact/UqVkYFxTMt6d4Dp9AJQ9Ai) · 5 choices

Five choices need your call. The first decides what viewers must already know.

| Question | What the draft does | Alternative |
| --- | --- | --- |
| “Standard error” and “95% interval” | Used without definition, as terms this audience knows. | A 20-second definition before S03's formula. |
| Which standard error the caterpillar uses | At the average case mix, the one pprof_py's own test uses. | Read at zero, the one most software prints. |
| The three tests | One 35-second scene, without their names. | Name Wald, likelihood ratio and score on screen; or cut the scene. |
| The verdict in S07 | “An opinion … and very little confidence in it.” Strong, and accurate for 103 patients. | Soften to “cannot yet be told apart”. |
| Mantel–Haenszel | Left out; its value is in the numbers file. | One sentence in S04 linking the slope test to it. |

## Episode 10 · No Events, No Peak

[Review doc](https://claude.ai/artifact/1ppwveVzTHTo5WiUrQFrUE) · 6 choices

Six choices need your call. The first is whether this interlude should be an episode.

| Question | What the draft does | Alternative |
| --- | --- | --- |
| An Extended module as a full episode | Produced at about 4½ minutes, as Episode 9's last line promises. | A 90-second aside inside Episode 11, with Episode 9's last line re-voiced. |
| The routines' names | “Stepping together” and “taking turns” are said. The two printouts in S01 carry the package's own labels, Serbin and Ban, in small type. | Leave the labels off. |
| A ratio before its episode | S05 says “1.87 times expected, or 2.76 times”. | Use the gap on the log-odds ruler: Cedar sits 0.23 above that reference, or 0.79. |
| “Flagged” before Act IV | S06 says “Elm is not flagged”. | “Not unusual enough to single out.” |
| Fen | A sixth clinic appears for one footnote. | Keep the screening rule and drop Fen, or drop the footnote. |
| Remedies | Left for the shrinkage module. The exact interval, 0 to 1.33, is on screen only. | A closing card: report the count-based test and its interval, and mark such providers in every plot. |

## Episode 11 · Swap the Curve

[Review doc](https://claude.ai/artifact/UDTXUn14n9YYUXmsSFv3m1) · 6 choices

Six choices need your call. The first changes how every board in this act is drawn.

| Question | What the draft does | Alternative |
| --- | --- | --- |
| Curve or line | The boards use the probability panel, where each clinic is a curve, and the script says “curve” throughout, matching the title. | The log-odds panel of Episodes 4 to 9, where each clinic is a line. |
| The cold open | 99 words, the longest so far, because it recalls Episode 3's two answers and its two requirements. | Open on the thought experiment and move the recall to S05. |
| Naming the measure | Said as “ratio”. “Indirect standardized ratio” appears once on screen, in S04. | Say the full name aloud once. |
| The interval in S07 | One sentence carries Episode 9's interval through the curve. | Hold it for the episode on intervals and tests. |
| The totals in S05 | Two sentences on 42 against 38.8. | Leave it to the review doc's audit. |
| Episode 12 | Promised in the last line, though the blueprint marks it Extended. | Go straight to whether a count is surprising, and re-voice the last line. |

## Episode 12 · Swap the Patients

[Review doc](https://claude.ai/artifact/CLpwVHZ4XHs7UaLfjFps4x) · 6 choices

Six choices need your call. The third is the one least suited to settling without you.

| Question | What the draft does | Alternative |
| --- | --- | --- |
| An Extended module as a full episode | Produced at about 5 minutes, as Episode 11's last line promises. | Fold S04 and S05 into Episode 11 as a two-minute coda. |
| The order | Opens on the swap of places, as a puzzle to solve. | The blueprint's order: the definition first, the swap of places fourth. |
| Whether Alder and Dune really differ | Not addressed. The fitted curves are taken as given. | One sentence in S01: the two curves are far closer together than their uncertainty. |
| Which direct figure | Rates, and Alder's 1.45 against the reference clinic's rate. | Add the blueprint's direct ratio, 1.34. |
| Rates to one decimal | Said as 54.5, 32.2, 37.6 and 55.9, because whole numbers would hide Alder against Dune. | Round them, and say the two are a point apart. |
| The framing in S06 | “Held to account” against “choosing between clinics”. | Describe the two questions without saying who asks them. |

## Episode 13 · Unequal Coins

[Review doc](https://claude.ai/artifact/A3FmxbMsB9pi3qxitVbSca) · 6 choices

Six choices need your call. The second is the one most likely to divide statisticians.

| Question | What the draft does | Alternative |
| --- | --- | --- |
| Dune before Alder | The cold open asks about Alder, then works the example on Dune's twelve coins, where every coin can be seen. | Work Alder throughout and show its thirty coins from the start. |
| The half bar | Explained in two sentences, because it is what pprof_py reports. The name “mid-p” is on screen only. | Say “mid-p” aloud; or use the plain tail in the narration and leave the half bar to the screen. |
| “Pile” for the distribution | Used throughout; “distribution” appears once, in the recap. | Say “distribution” from S04 on. |
| The identical-coins scene | Uses Alder, where the verdict flips from 3.5% to 5.2%. | The blueprint's version: Dune's variances, 2.29 against 2.88, with no verdict at stake. |
| The calibration figure | “4.8%, against the 5% it promises”, from 50 crowds. | Run the blueprint's 100 crowds and say what that gives; or say “about 5%”. |
| Episode 14 | Promised in the last line, though the blueprint marks it Extended. | Go straight to the funnel, and re-voice the last line. |

## Episode 14 · Three Shortcuts

[Review doc](https://claude.ai/artifact/5yiMfeQu64TM6qP1nPcgQq) · 6 choices

Six choices need your call. The first runs through every sentence of the episode.

| Question | What the draft does | Alternative |
| --- | --- | --- |
| Working names | “Bell curve”, “ruler” and “flipping” throughout; “score test”, “Wald test” and “bootstrap” are each said once. | The formal names throughout. |
| An Extended module as a full episode | Produced at about 4¾ minutes, as Episode 13's last line promises. | Move the bell curve into Episode 15, which needs it for the funnel's limits, and drop the rest. |
| Why shortcuts at all | S01 says the exact test is “a fair amount of work”; S08 gives the real reasons. | Give the real reasons in S01: a formula, and a link to gamma. |
| The flipping figure | “This run gives 3.8%”, from the series seed. | “About 3½ to 4%, depending on the run.” |
| The small-provider figures | Said to one decimal: 4.7%, 4.9%, 4.0%. | “About 5%, about 5%, and only 4%”, since the first two cannot be told apart. |
| The order in S07 | The ruler's two weaknesses first, then the bell curve's, then the calibration. | Bell curve first, as in S03. |

## Episode 15 · The Funnel

[Review doc](https://claude.ai/artifact/QHHJr7eN65HHKzeH86P2GR) · 5 choices

| Question | What the draft does | Alternative |
| --- | --- | --- |
| The cold open | A league table, a secret six, and a pick of the top and bottom three that gets two right. | Say also that the top ten holds all three truly worse providers; or open on Dune's band, as the blueprint does. |
| Defining precision | “How much a clinic can tell us”, with the formula on screen. | One spoken sentence: the expected count squared, over its variance. |
| The redraw figure | “On average 5%”; the fifty redraws give 4.8%. | Say 4.8%, as Episode 13 did for its own run. |
| The exact-funnel footnote | One clip in S07. | Cut it, and leave it to the review doc's audit. |
| The promise in S08 | “It has an episode of its own”, which commits the series to the blueprint's last module. | “We will come back to it.” (Episode 19 has since been built, so the promise is kept.) |

## Episode 16 · Trusting the Risk Model

[Review doc](https://claude.ai/artifact/AwJpQAnD5ueHkitz7GM2Tb) · 6 choices

| Question | What the draft does | Alternative |
| --- | --- | --- |
| Whose figures | This episode's own, from the crowd's own random draws. Several differ a little from the blueprint's. | Supply the blueprint's original draws or code, and rebuild the episode on them. |
| Naming the two crowds | “The first crowd” and “the second crowd”. | Give them names that say what differs, such as the straight crowd and the bent crowd. |
| The AUC | Said as “A U C” and defined by a pair of patients. No ROC curve, and the name is not spelled out. | Spell it out once and show the curve. |
| “Tenths” | Used throughout; “deciles” is never said. | Say “deciles” once, as the term viewers will meet elsewhere. |
| The verdict in S05 | “They were being blamed for the model's mistake.” | “Their ratios carried the model's mistake.” |
| An Extended module as a full episode | Produced at about 4¾ minutes, as Episode 15's last line promises. | Keep S03 to S06 and move the slope and the limits to a later episode. |

## Episode 17 · Fixed or Random?

[Review doc](https://claude.ai/artifact/BkeDAtbAyoQdALoDg3EmCT) · 6 choices

| Question | What the draft does | Alternative |
| --- | --- | --- |
| The cast under the pull | Carries the pull through all five clinics, so the order flips and Elm gets −1.71. | Keep to Dune's reliability of 0.20 alone, as the blueprint does. |
| Where the cast's spread comes from | Borrows the crowd's 0.33. | Use pprof_py's fit of the five clinics: spread 0.41, Dune −1.12, Alder −0.99, Elm −1.65. |
| The word for it | “Pull” throughout; “shrinkage” is never said. | Say “shrinkage” once, as the term viewers will meet elsewhere. |
| The flags in S06 | Four against three, from two different tests. | Drop the flags and keep the distances, 0.67 against 0.46. |
| The mechanism in S07 | Names only the pull toward one centre. | Add a sentence on the shifted risk rule. |
| Length | About 4½ minutes for a module the blueprint sizes at 12. Left out: the model's formula in words, and that shrinkage is not a correction for multiple testing. | Add a scene for each. |

## Episode 18 · Too Many Intercepts

[Review doc](https://claude.ai/artifact/P71xgjDTSmoxyb5v5kAN2h) · 6 choices

| Question | What the draft does | Alternative |
| --- | --- | --- |
| Whose figures | This episode's own, from 400 worlds at each size. | The blueprint's, from 100: 24%, 12%, 6%, 1%, and intervals holding the truth 32% of the time with fives. |
| “It cannot profile a provider” | Says so flatly, as the blueprint does. | Add that intercepts can be fitted afterwards with the conditional coefficient held fixed, and that profiling packages do not take that route. |
| The explanation in S03 | “The intercept flatters them”, with the exact factor of two shown on screen. | Narrate the derivation: the fit sees only half the gap between the two patients. |
| The name | The incidental-parameter problem is never named. | Name it once, as the term viewers will meet elsewhere. |
| The straight-line contrast | Left to the review doc: a linear model with one intercept per pair is unbiased. | One sentence in S07, to show the bias belongs to the logistic curve. |
| Length | About 4 minutes for a module the blueprint sizes at 9. | Add a scene on what a biased rule does to expected counts for unusual case mixes. |

## Episode 19 · Wider than Chance

[Review doc](https://claude.ai/artifact/En4DrP7FPy3p4cmE4oeD8j) · 6 choices

| Question | What the draft does | Alternative |
| --- | --- | --- |
| Closing the arc | Two sentences in S09 that retrace the model in four steps, then the end card. | End on the recap; or a longer retrospective that names each act. |
| The knob at zero | Says the fitted curve “can miss”, and shows this crowd's 20 flags against 11. | The blueprint's stronger line: at zero the estimated null is too narrow and flags more. The redraws do not support it as a rule. |
| Counting flags | The funnel's 49 in the cold open, the exact test's 48 from S03 on. | One test throughout, at the price of a funnel whose dots do not match its counts. |
| “13 in place of 52” | Counts all 200 providers. | Count the 194 ordinary ones: 10 in place of 48, which matches the knob scene. |
| Naming the standard test | “The standard test” and “the bell curve”; the term theoretical null is never said. | Say “theoretical null” once, opposite “empirical null”. |
| What comes after | The end card names nothing. | Point to the Cox arc as the sibling series. |
