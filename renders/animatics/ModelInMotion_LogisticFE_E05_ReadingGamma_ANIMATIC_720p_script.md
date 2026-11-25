# Model in Motion · The Logistic Fixed-Effect Model · Episode 5: Reading γ

*what a gap between two clinics means for a patient*

Narration script with timestamps. 735 words, running time 05:26. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *The log-odds panel with Alder's and Cedar's lines. A bracket between them reads 0.87 and slides from one end to the other without changing.*

> [00:00.0] Last time, every clinic got a line of its own, all with the same tilt.  
> [00:04.6] Alder's line sits 0.87 above Cedar's. At the lower-risk end, at the higher-risk end, anywhere you look: the same 0.87.  

**00:15.2 · s1_2** — *Beside the panel: a step of 0.87 becomes odds × 2.4. Then the question: 2.4 times what?*

> [00:15.2] On the log-odds ruler, a step of 0.87 multiplies the odds by 2.4.  
> [00:22.0] So in some sense, Alder is 2.4 times Cedar. But 2.4 times what?  

**00:28.2 · s1_3** — *Three cards, numbered 1 to 3, each finishing the sentence a different way.*

> [00:28.2] Here are three ways to finish that sentence.  
> [00:30.9] One: Alder has 2.4 times as many readmissions.  
> [00:34.7] Two: at Alder, each patient is 2.4 times as likely to be readmitted.  
> [00:40.6] Three: at Alder, each patient's odds of readmission are 2.4 times as high.  
> [00:46.6] Only one of them is right. Pick one before we go on.  

## S02_Title  (00:51)

**00:51.9 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:51.9] Welcome back to Model in Motion.  
> [00:54.1] Today: reading gamma.  

## S03_Three · Three readings  (00:58)

**00:58.1 · s3_1** — *Reading 1 as a header. Two rate bars: Alder 13 of 30, 43%; Cedar 8 of 20, 40%. A cross.*

> [00:58.1] Start with the first, and count.  
> [01:00.3] Alder had 13 readmissions among 30 patients. Cedar had 8 among 20. That is 43% against 40%: almost level.  
> [01:09.7] And we already know why raw counts settle nothing: they depend on who each clinic treats.  

**01:15.0 · s3_2** — *Reading 2 as a header. Two rows of risk chips: lower-risk 18% and 34%, × 1.9; higher-risk 62% and 80%, × 1.3. A note: 2.4 × 62% is nearly 150%. A cross.*

> [01:15.0] The second reading: each patient is 2.4 times as likely to come back.  
> [01:20.5] Take a lower-risk patient. The model gives 18% at Cedar and 34% at Alder. That is 1.9 times, not 2.4.  
> [01:30.2] For a higher-risk patient, 62% becomes 80%: only 1.3 times.  
> [01:36.1] And it could never be 2.4. That would be a chance of nearly 150%.  

**01:42.0 · s3_3** — *Reading 3 as a header. The same two rows as odds: 0.22 and 0.52, × 2.4; 1.64 and 3.91, × 2.4. A tick, then the gap written as an odds ratio.*

> [01:42.0] Now the third. Turn those probabilities into odds.  
> [01:45.5] For the lower-risk patient: 0.22 at Cedar, 0.52 at Alder. 2.4 times.  
> [01:53.4] For the higher-risk patient: 1.64 and 3.91. 2.4 times again.  
> [02:00.2] That is what a gap between two gammas means. For patients who look the same on paper, one at each clinic, the odds differ by a single multiplier: the odds ratio.  

## S04_Slide · One odds ratio, many effects  (02:13)

**02:13.1 · s4_1** — *Cedar's and Alder's S-curves on the probability panel. A marker appears on each curve at the same risk score, joined by a yellow segment.*

> [02:13.1] Here are the two clinics as S-curves: one shape, slid sideways by that gap.  
> [02:18.2] Now slide a patient along, from low risk to high, and read both curves.  

**02:23.3 · s4_2** — *The patient stops five times. Each stop leaves a pair of dots on the curves and a row in a table: at Cedar, at Alder, difference.*

> [02:23.3] A patient with a 5% chance at Cedar has 11% at Alder: 6 points more.  
> [02:29.2] At 18%, where Cedar's lower-risk patients sit, Alder gives 34%: 16 points.  
> [02:35.9] At 50%, it is 70%: 20 points.  
> [02:39.0] At 62%, Cedar's higher-risk patients: 80%. That's 18 points.  
> [02:44.5] And at 90%, 96%: back down to 6.  

**02:48.3 · s4_3** — *The difference column is highlighted; a ratio column appears beside it, from × 2.2 down to × 1.06.*

> [02:48.3] One gap, one odds ratio. But the difference in probability swells in the middle and fades at both ends.  
> [02:55.5] The ratio of probabilities shrinks all the way: 2.2 at the low end, 1.06 at the top. Only when readmission is rare does it come close to 2.4.  
> [03:07.6] So what a gap costs in readmissions depends on which patients a clinic sees.  

## S05_Zero · Gammas move. Gaps don't.  (03:14)

**03:15.1 · s5_1** — *The log-odds panel with the four fitted lines. A yellow zero mark stands at the lower-risk position; a ring on each line marks where its gamma is read. Sliders show the four values.*

> [03:15.1] Last time we said: read the gaps, not the gammas themselves. Here is why.  
> [03:19.9] A gamma is read where every risk factor is zero. So far, zero has meant a lower-risk patient.  

**03:27.0 · s5_2** — *The zero mark slides to the higher-risk position, and the rings ride up their lines: every slider value rises by 2.02. Then it slides back to the midpoint: 1.01 above the start.*

> [03:27.0] But that was our choice. Call the higher-risk patient zero instead.  
> [03:31.2] Every gamma climbs by 2.02: the whole step.  
> [03:35.2] Or put zero halfway between, at a patient who doesn't exist. Now every gamma is 1.01 above where it started.  

**03:43.9 · s5_3** — *The lines have not moved. The bracket between Alder and Cedar, which travelled with the zero mark, still reads 0.87.*

> [03:43.9] Through all of this, no line has moved, and no patient's probability has changed.  
> [03:49.1] And the gap between Alder and Cedar is 0.87 every time.  
> [03:54.0] A gamma depends on where we put zero. A gap doesn't.  

## S06_Averages · A warning about averages  (03:59)

**03:59.3 · s6_1** — *Two rows. All 103 patients at Cedar's level: 57 lower-risk at 18% and 46 higher-risk at 62% give 38%. At Alder's level: 34% and 80% give 55%.*

> [03:59.3] One warning before we finish.  
> [04:01.3] Suppose all 103 patients went to Cedar. The model says 38% would come back. All of them at Alder: 55%.  

**04:11.2 · s6_2** — *A log-odds ruler with the two average rates as dots, 0.69 apart. Beside it, two bars to compare: 0.87 for each patient, 0.69 between the two averages.*

> [04:11.2] Put those two rates on the log-odds ruler. They are 0.69 apart, not 0.87.  
> [04:18.3] Nothing has gone wrong. The 0.87 compares one kind of patient at a time. The 0.69 compares two averages, taken over patients of very different risk.  
> [04:31.0] Those are different questions, and the second gives the smaller answer whenever patients differ in risk.  

**04:37.5 · s6_3** — *One line of text under the bars.*

> [04:37.5] So if a gap from a model looks bigger than the gap between two overall rates, that alone is no contradiction.  

## S07_Recap · Recap  (04:45)

**04:45.8 · s7_1** — *Three recap cards, each with a small icon.*

> [04:45.8] Let's gather it up.  
> [04:47.4] A gap between gammas multiplies the odds, by the same amount for every patient.  
> [04:52.8] What that does to a probability depends on where the patient starts.  
> [04:56.8] And gammas depend on where zero is. Gaps do not.  

**05:00.6 · s7_2** — *A tag: 103 patients, rough estimates. Then the dial and sliders, drifting toward their fitted places; the next episode's title.*

> [05:00.6] One reminder: every gap we read today rests on 103 patients, so each one is rough. How rough is still to come.  
> [05:09.1] And all this time, the lines have simply appeared, already in place.  
> [05:13.2] Next time, we find out how the dial and the sliders settle where they do: fitting by balance.  

**05:19.3 · s7_3** — *Series end card with the next episode title.*

> [05:19.3] This has been Model in Motion. Thanks for following the story.  
