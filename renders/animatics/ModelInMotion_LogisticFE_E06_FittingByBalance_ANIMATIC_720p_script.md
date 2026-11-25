# Model in Motion · The Logistic Fixed-Effect Model · Episode 6: Fitting by Balance

*how the dial and the sliders find their places*

Narration script with timestamps. 710 words, running time 04:48. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *The log-odds panel. The dial and sliders drift from an unfitted position and settle; the lines settle with them.*

> [00:00.0] For two episodes, the dial and the sliders have simply known where to stop.  
> [00:04.6] Four sliders settled, the dial settled, and we read off the answers.  

**00:09.0 · s1_2** — *Beside the panel: 103 patients, and who came back.*

> [00:09.0] But nobody handed them those answers. All they had was the data: 103 patients, and who came back.  

**00:16.6 · s1_3** — *The question, in two lines.*

> [00:16.6] So what makes one setting of the dial and sliders better than another?  
> [00:20.7] And how do they find the best one?  

## S02_Title  (00:24)

**00:24.4 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:24.4] Welcome back to Model in Motion.  
> [00:26.6] Today: fitting by balance.  

## S03_Score · Scoring a guess  (00:30)

**00:30.8 · s3_1** — *All 103 patients as chips in five trays. A label: the plain guess, 41% for everyone.*

> [00:30.8] Start with any setting at all. Here is the plainest: every patient, at every clinic, gets the overall rate, 41%.  

**00:39.1 · s3_2** — *Two example chips: a filled one marked 41%, an empty one marked 59%.*

> [00:39.1] Now ask of each patient: what probability did this guess give to what actually happened?  
> [00:44.8] For a patient who was readmitted, 41%. For one who wasn't, 59%.  

**00:51.1 · s3_3** — *The product: 0.41 to the power 42 times 0.59 to the power 61, about 6 × 10⁻³¹. Then its logarithm: −69.6.*

> [00:51.1] Multiply those 103 numbers together, and you have the probability the guess gave to the whole story. That is its likelihood.  
> [00:59.5] It is tiny: a decimal point followed by thirty zeros. So we take its logarithm instead: minus 69.6.  

**01:08.5 · s3_4** — *A height bar, with its level at −69.63 near the bottom and an arrow pointing up.*

> [01:08.5] Think of that number as a height. A better guess stands higher.  
> [01:12.2] The height itself means nothing. Only the climb from one guess to another does.  

## S04_Meters · Which way is up?  (01:18)

**01:18.8 · s4_1** — *The machine: a slider and an observed-minus-expected meter for each clinic, the dial with its own meter, and the height bar. All set to the plain guess.*

> [01:18.8] So which way is up? Bring back the meter from Episode 3: observed on one side, expected on the other.  
> [01:25.7] Here is one for every clinic, under the plain guess.  

**01:29.1 · s4_2** — *Dune's, Birch's and Elm's meters are picked out in turn: +2.11, +1.77, −4.49.*

> [01:29.1] Dune expected 4.9 readmissions and saw 7. Birch expected 12.2 and saw 14. Elm expected 4.5 and saw none.  

**01:40.2 · s4_3** — *An arrow beside each slider: up where observed is above expected, down where it is below. Caption: tilt = slope.*

> [01:40.2] And here is the fact that makes fitting possible.  
> [01:43.2] Each meter's tilt is exactly the slope of the height in that clinic's gamma.  
> [01:48.1] Observed above expected: push the slider up. Observed below: pull it down.  

## S05_Moves · One at a time?  (01:54)

**01:55.8 · s5_1** — *Dune's slider rises. Of the clinic meters only Dune's moves; its expected count climbs to 7.0 and the height bar rises by 0.75. The dial's meter eases from +10.24 to +9.19.*

> [01:55.8] Try it with Dune. Push its slider up, and among the clinics, only Dune's meter responds.  
> [02:01.5] Its expected count climbs toward 7, and the height rises with it.  

**02:06.2 · s5_2** — *Dune's meter is level. Then the slider is pushed further: the meter tips the other way and the height bar drops. It returns to level.*

> [02:06.2] When the meter is level, the height is as high as this one slider can take it.  
> [02:11.0] Push further, and the meter tips the other way. The height falls.  

**02:14.8 · s5_3** — *Back at the plain guess. The dial's yellow meter is picked out: 29 observed, 18.8 expected.*

> [02:14.8] The dial has a meter too. It weighs only the higher-risk patients: 29 of them were readmitted, and the plain guess expected fewer than 19.  

**02:24.8 · s5_4** — *The dial turns to 0.91 and its meter levels. Four clinic meters shift as it turns; Elm's does not.*

> [02:24.8] Turn the dial up until that meter is level.  
> [02:27.6] But look at the clinics. Every one that has higher-risk patients has shifted.  

**02:32.3 · s5_5** — *Caption: nothing settles one piece at a time.*

> [02:32.3] So nothing can be settled one piece at a time. The dial and the sliders have to find their places together.  

## S06_Level · Level everything  (02:40)

**02:41.7 · s6_1** — *Dial and sliders move together to the fit. Four clinic meters and the dial's meter come level; the height bar climbs.*

> [02:41.7] And here is where they stop. The dial at 2.02, and the sliders where we found them two episodes ago.  
> [02:49.2] Four clinic meters are level, and so is the dial's.  

**02:52.8 · s6_2** — *The four expected counts are picked out: 13.0, 14.0, 8.0, 7.0.*

> [02:52.8] In each of those four clinics, expected now equals observed: 13, 14, 8 and 7.  
> [02:59.4] That is what fitting is: balancing.  

**03:02.1 · s6_3** — *A note under Alder: 8.2 + 4.8 expected, 8 + 5 observed.*

> [03:02.1] One detail. The balance holds for each clinic's total, not for each group inside it.  
> [03:07.9] Alder expected 8.2 among its lower-risk patients and 4.8 among its higher-risk ones. Not 8 and 5. But together, 13.  

**03:18.2 · s6_4** — *Elm's slider keeps sliding down, past the end of its track. Its meter approaches level and never reaches it; the height bar creeps up.*

> [03:18.2] And Elm? Its meter can never level. With no readmissions, expected stays above observed wherever the slider sits.  
> [03:25.8] So the slider keeps sliding, gaining a little less height each time. We'll come back to Elm.  

**03:31.5 · s6_5** — *Beside the height bar: −69.6 to −55.6.*

> [03:31.5] With Elm's slider run all the way down, the height has climbed from minus 69.6 to minus 55.6.  

## S07_Hill · The hill  (03:41)

**03:41.6 · s7_1** — *A chart: dial position along the bottom, height up the side. A dot traces the curve from left to right.*

> [03:41.6] One last picture. For each position of the dial, level the clinics' meters, and record the height.  

**03:47.9 · s7_2** — *The top is marked at 2.02. A second mark at 1.75, the pooled step, sits just below it on the left.*

> [03:47.9] The result is a hill, with one top, at 2.02.  
> [03:51.9] The pooled step from Episode 3, 1.75, sits a little way down the left side.  

**03:58.3 · s7_3** — *A bracket over the rounded top.*

> [03:58.3] And notice how gently the top is rounded. That gentleness is the roughness we keep promising to measure.  

## S08_Recap · Recap  (04:06)

**04:06.7 · s8_1** — *Three recap cards, each with a small icon.*

> [04:06.7] Let's gather it up.  
> [04:08.3] A guess is scored by the probability it gave to what actually happened.  
> [04:12.6] Each clinic's meter, observed minus expected, says which way its slider should move.  
> [04:18.0] And at the best fit, every meter that can level is level.  

**04:21.8 · s8_2** — *A caution card: level meters do not show the model is right.*

> [04:21.8] A caution. Level meters do not show that the model is right.  
> [04:25.7] Any model with a number for each clinic will level them. Whether it is right has to be judged inside the clinics, and that comes later.  

**04:34.0 · s8_3** — *The hill again, small, with a climber's path sketched toward the top; the next episode's title.*

> [04:34.0] We have seen where the top of the hill is, not how to get there. No formula gives it.  
> [04:39.2] Next time: climbing the hill.  

**04:41.5 · s8_4** — *Series end card with the next episode title.*

> [04:41.5] This has been Model in Motion. Thanks for following the story.  
