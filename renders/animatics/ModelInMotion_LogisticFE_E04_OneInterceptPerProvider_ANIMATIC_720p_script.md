# Model in Motion · The Logistic Fixed-Effect Model · Episode 4: One Intercept per Provider

*the model, as parallel lines*

Narration script with timestamps. 1092 words, running time 07:19. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *The log-odds panel: a vertical log-odds ruler with probability labels, and two positions along the bottom, lower-risk and higher-risk. Two grey dots at the pooled rates, joined by a dashed grey line.*

> [00:00.0] Last time, we pooled all five clinics into a single standard.  
> [00:04.1] Drawn on the log-odds ruler, that standard is one line: lower-risk patients start at 23%, and higher risk is one step up, to 63%.  

**00:14.2 · s1_2** — *Each clinic's own dots appear in its colour, sized by number of patients. Alder and Dune sit above the line at both ends; Birch and Cedar below at both. Elm's marker rests on the bottom edge with a down arrow: 0 of 11.*

> [00:14.2] Now put the clinics back.  
> [00:16.0] Alder's patients sit above the line, at both ends. So do Dune's.  
> [00:20.2] Birch and Cedar sit below it, at both ends. And Elm, with no readmissions at all, is off the bottom of the chart.  

**00:28.0 · s1_3** — *Short vertical ticks mark each miss, in the clinic's colour. The question appears.*

> [00:28.0] One line for everyone misses, and it misses clinic by clinic.  
> [00:31.9] So here is today's question: what is the smallest change that fixes it?  

## S02_Title  (00:38)

**00:38.1 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:38.1] Welcome back to Model in Motion.  
> [00:40.3] Today: one intercept per provider.  

## S03_OwnLines · What should clinics share?  (00:45)

**00:46.1 · s3_1** — *Each clinic's two dots are joined by a line of its own. Cedar's carries a small tag: Episode 2.*

> [00:46.1] The obvious fix is to give every clinic a line of its own: its own starting point, and its own step.  
> [00:52.6] That's what we did for Cedar, two episodes ago.  

**00:55.9 · s3_2** — *Alder's higher-risk dot pulses: 6 patients. Brackets mark the gap between Alder's and Cedar's lines at each end: 0.69 on the left, 1.20 on the right.*

> [00:55.9] But look at what it costs.  
> [00:57.6] Each line now rests on one clinic's patients alone. Alder's higher-risk end is just 6 people.  
> [01:04.0] And the gap between two clinics is no longer one number. Alder sits further above Cedar for higher-risk patients than for lower-risk ones.  

**01:13.0 · s3_3** — *A question mark hangs between the two brackets; the two piles of chips split into four, eight, sixteen.*

> [01:13.0] So the question 'how much higher is Alder?' would have two answers. With a dozen risk factors, it would have thousands.  

**01:20.4 · s3_4** — *The four lines pivot until they are parallel. Caption: the bet, one step for everyone.*

> [01:20.4] So let's make a bet instead.  
> [01:22.3] Suppose a risk factor works the same way in every clinic: the same step on the log-odds ruler, wherever you are treated.  
> [01:30.0] Then clinics can differ in only one way: where they start.  

## S04_Model · The model  (01:35)

**01:36.2 · s4_1** — *A yellow dial labelled beta. Turning it tilts every line together.*

> [01:36.2] Here is that bet as a machine.  
> [01:38.3] One dial, beta, sets the step for everyone. Turn it, and every line tilts together.  

**01:44.3 · s4_2** — *One slider per clinic, in its colour, labelled gamma. Moving Alder's slider moves only Alder's line; the tilt does not change.*

> [01:44.3] And every clinic gets a slider of its own. It moves that clinic's line up or down, and leaves the tilt alone.  
> [01:51.4] We'll call that number gamma.  

**01:53.4 · s4_3** — *The word intercept labels the left end of a line, at the lower-risk position.*

> [01:53.4] Statisticians call a line's starting point its intercept.  
> [01:57.2] So that's the whole idea: one intercept per provider, and one shared step.  

**02:02.4 · s4_4** — *The equation assembles from labels already on screen: log-odds = gamma (clinic) + beta × (higher-risk). Then the compact form, logit(p_ij) = gamma_i + beta·x_ij. Then three yellow steps stack, as in Episode 2.*

> [02:02.4] Written out: a patient's log-odds is their clinic's gamma, plus beta if they are higher-risk.  
> [02:08.2] With more risk factors there are more steps, each with its own beta. There is still just one gamma per clinic.  

**02:15.1 · s4_5** — *Name card: the logistic fixed-effect model. Under the word fixed: each gamma is its own unknown number.*

> [02:15.1] This is the logistic fixed-effect model.  
> [02:18.0] 'Fixed' means only that each gamma is its own unknown number. We assume nothing about how those numbers are spread across clinics.  

## S05_Fit · Where the lines land  (02:27)

**02:28.9 · s5_1** — *The dial and the sliders drift, then settle.*

> [02:28.9] How the dial and the sliders find their best positions is a story for a later episode. For now, here is where they land.  

**02:37.0 · s5_2** — *The dial reads beta = 2.02; beside it, odds × 7.5.*

> [02:37.0] The shared step is 2.02.  
> [02:39.6] That is the bet at work: in every clinic, higher risk multiplies the odds of readmission by about seven and a half.  

**02:47.3 · s5_3** — *Gamma labels at the left end of each line: Birch −1.82, Cedar −1.52, Alder −0.65, Dune −0.58.*

> [02:47.3] Four sliders settle. Birch is lowest, at minus 1.82. Then Cedar. Then Alder and Dune, close together at the top.  

**02:56.6 · s5_4** — *Elm's line keeps sliding down and leaves the panel. A hatched tag: 0 of 11, no finite gamma.*

> [02:56.6] Elm's never does. With no readmissions at all, a lower line always fits better, so it slides off the chart.  
> [03:03.7] Elm gets an episode of its own.  

**03:06.2 · s5_5** — *The ruler switches from log-odds to probability. The lines bend into S-curves of one shape, slid sideways. Markers at the two risk positions: Birch 14% and 55%, Alder 34% and 80%.*

> [03:06.2] Switch to the probability ruler, and the parallel lines become S-curves: one shape, slid sideways.  
> [03:13.0] For a lower-risk patient, the model gives 14% at Birch and 34% at Alder.  
> [03:18.7] For a higher-risk patient, 55% at Birch and 80% at Alder.  

**03:23.6 · s5_6** — *A small tag under the dial: 103 patients, rough estimates.*

> [03:23.6] One caution. With 103 patients, these are rough estimates. How rough is a question for later.  

## S06_WhereBeta · A rule learned inside clinics  (03:32)

**03:33.4 · s6_1** — *The dashed pooled line returns beside the fitted lines: a step of 1.75 against 2.02.*

> [03:33.4] Notice that the step has grown. The pooled line climbed 1.75. These lines climb 2.02.  

**03:41.5 · s6_2** — *Inside each clinic, a bracket from its lower-risk dot to its higher-risk dot: Alder 2.30, Birch 1.78, Cedar 1.79, Dune 2.30. Elm has one dot and no bracket.*

> [03:41.5] Here's why. Each clinic is now compared only with itself: its own higher-risk patients against its own lower-risk patients.  
> [03:49.6] Inside Alder, the step is 2.3. Inside Birch, 1.78. Cedar, 1.79. Dune, 2.3.  

**03:59.3 · s6_3** — *The four brackets feed the dial; its needle rests at 2.02. Elm stays dim.*

> [03:59.3] Beta is a compromise among those four, weighted by how much each clinic's patients can tell us.  
> [04:05.4] Elm has no say. All of its patients are lower-risk, so it has no step to offer.  

**04:10.9 · s6_4** — *Episode 3's two phrases, how sick and where treated. The where arrows flow into the sliders.*

> [04:10.9] Last time, the pooled rule mixed up how sick patients are with where they were treated.  
> [04:16.1] Now the 'where' has a place of its own: the gammas.  
> [04:19.2] That is the first thing we asked for: a risk rule learned from patients who share a clinic.  

## S07_NoIntercept · No overall intercept  (04:26)

**04:27.1 · s7_1** — *A grey knob labelled beta-zero appears beside the sliders.*

> [04:27.1] You might expect one more number: an overall starting point, with each clinic measured from it.  

**04:33.0 · s7_2** — *The grey knob rises by 0.5 while every slider drops by 0.5. The lines and every probability stay exactly where they were. The grey knob is struck out.*

> [04:33.0] Try it. Raise that number by a half, and lower every gamma by a half.  
> [04:37.6] Nothing on screen moves. The data cannot tell those two descriptions apart, so the model keeps only the gammas.  

**04:45.0 · s7_3** — *Tags for size, ownership and neighbourhood drop into a clinic's slider and disappear inside it.*

> [04:45.0] The same goes for anything that is identical for every patient at a clinic: its size, its ownership, its neighbourhood.  
> [04:52.8] None of them can have a beta of its own. They are already inside gamma.  

## S08_Gamma · What gamma is, and isn't  (04:58)

**04:58.8 · s8_1** — *Alder's gamma, −0.65, on the log-odds ruler, linked to 34% on the probability ruler. A chip with a 34% slice: a lower-risk patient at Alder.*

> [04:58.8] So what is a gamma? Read it carefully.  
> [05:01.4] Alder's is minus 0.65. That is not a readmission rate. It is a position on the log-odds ruler: the log-odds for a patient with no risk factor switched on.  
> [05:13.6] Here, that's a lower-risk patient at Alder: 34%.  

**05:17.9 · s8_2** — *A dozen risk-factor tags, all switched off; the chip fades to an outline.*

> [05:17.9] With many risk factors, that patient may not exist at all. So we will mostly read the gaps between gammas, not the gammas themselves.  

**05:26.6 · s8_3** — *Card: gamma is not a pure measure of care. Inside the slider, two parts with no fixed boundary: care, and what we didn't measure about its patients.*

> [05:26.6] And gamma is not a pure measure of care.  
> [05:29.3] It holds everything that is constant within a clinic: how well it looks after patients, but also anything about its patients that we failed to measure. The data cannot separate the two.  

**05:42.0 · s8_4** — *Two identical chips, one at Alder and one at Birch, with different slices.*

> [05:42.0] So read a higher gamma this way: for patients who look the same on paper, more readmissions here than there. Why is a separate question.  

## S09_Crowd · Two hundred lines  (05:52)

**05:52.2 · s9_1** — *200 thin parallel lines. A short scale for the main risk factor's step, with a marker at the truth: 0.80.*

> [05:52.2] Does learning the rule inside providers really help?  
> [05:55.3] Go back to our simulated crowd of 200 providers, where we set the truth ourselves. The true step for the main risk factor is 0.8.  

**06:05.4 · s9_2** — *Two more markers on the scale: pooled 0.71, fixed-effect 0.81.*

> [06:05.4] Pool everyone, and the estimate is 0.71, because in this crowd, providers with sicker patients happen to do a little better.  
> [06:14.2] Give every provider its own gamma, and the estimate is 0.81.  

## S10_Recap · Recap  (06:20)

**06:20.7 · s10_1** — *Three recap cards, each with a small icon.*

> [06:20.7] Let's gather it up.  
> [06:22.2] Every provider gets its own intercept: gamma.  
> [06:25.5] All providers share one step for each risk factor: beta.  
> [06:29.7] And beta is learned from comparisons inside providers.  

**06:33.8 · s10_2** — *Assumption card, three lines: parallel lines (a bet); patients' outcomes independent, given clinic and risk factors; nothing assumed about how the gammas are spread or how they relate to case mix. One dashed line crosses the parallel ones.*

> [06:33.8] Remember what this rests on: the bet that the lines are parallel.  
> [06:37.8] A clinic that does well with lower-risk patients and badly with higher-risk ones would have a line that crosses the others. We will come back and check.  

**06:47.0 · s10_3** — *Episode 3's two requirements; the first is ticked. The gammas line up on the log-odds ruler: Elm off the end, then Birch, Cedar, Alder, Dune. Cedar, in the middle, is ringed.*

> [06:47.0] Last time, we asked for two things. The risk rule, we now have.  
> [06:51.2] And the yardstick? Line the gammas up, and one of them sits in the middle: Cedar's.  
> [06:56.4] A middle clinic is a yardstick that no clinic's size can pull toward itself. We'll build on it later.  

**07:02.8 · s10_4** — *A bracket between Alder's and Cedar's lines: 0.87. Next episode title.*

> [07:02.8] First, though: Alder's line sits 0.87 above Cedar's. What does that gap mean for an actual patient?  
> [07:10.3] Next time: reading gamma.  

**07:12.6 · s10_5** — *Series end card with the next episode title.*

> [07:12.6] This has been Model in Motion. Thanks for following the story.  
