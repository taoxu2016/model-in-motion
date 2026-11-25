# Model in Motion · The Logistic Fixed-Effect Model · Episode 14: Three Shortcuts

*when can a faster test replace the exact one?*

Narration script with timestamps. 615 words, running time 04:40. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *Alder's exact pile from last time, its tail shaded, and the p-value: 0.035.*

> [00:00.0] Last time we built Alder's pile coin by coin, and read its p-value from the tail: 3.5%.  
> [00:07.4] Exact, and a fair amount of work.  

**00:10.1 · s1_2** — *Three small pictures in a row: a bell curve, a ruler, and a scatter of flipped coins.*

> [00:10.1] In practice, people often skip the pile. Three shortcuts are in everyday use: a bell curve, a ruler, and brute-force flipping.  

**00:18.8 · s1_3** — *Under each picture, an empty slot for Alder's p-value, with a line at 5%.*

> [00:18.8] Each gives Alder a p-value of its own. Will all three land on the same side of 5%? And is there a clinic where a shortcut goes badly wrong?  

## S02_Title  (00:30)

**00:30.2 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:30.2] Welcome back to Model in Motion.  
> [00:32.4] Today: three shortcuts.  

## S03_Bell · One: a bell curve  (00:36)

**00:36.5 · s3_1** — *Alder's pile with a bell curve laid over it: the same centre, 8.02, and the same spread, 2.22.*

> [00:36.5] The first shortcut replaces the pile with a bell curve of the same centre and the same spread.  
> [00:42.4] For Alder, that is centred on 8.02, with a standard deviation of 2.22.  

**00:48.9 · s3_2** — *A marker at 13 and an arrow from the centre: 4.98, or 2.24 spreads. The curve's two tails beyond that are shaded: 2.5%.*

> [00:48.9] Alder's 13 is 4.98 above the centre. Divide by the spread: 2.24 standard deviations out.  
> [00:57.4] The bell curve's two tails beyond that hold 2.5%.  

**01:01.5 · s3_3** — *The formula with Alder's numbers: (13 − 8.02) ÷ 2.22 = 2.24. A tag: the score test.*

> [01:01.5] That is the score test. It needs just three numbers: observed, expected, and the spread.  
> [01:07.2] It is our old friend, observed minus expected, measured in standard units.  

## S04_Ruler · Two: a ruler on the gamma axis  (01:14)

**01:14.1 · s4_1** — *The log-odds ruler with the reference at −1.52 and Alder at −0.65. A bracket between them: 0.87. Whiskers on Alder: its standard error, 0.43.*

> [01:14.1] The second shortcut never looks at the count. It goes back to the sliders.  
> [01:18.7] Alder's gamma sits 0.87 above the reference, and Episode 9 gave it a standard error of 0.43.  

**01:27.4 · s4_2** — *The gap measured off in standard errors: 0.87 ÷ 0.43 = 2.02. The p-value: 0.044. A tag: the Wald test.*

> [01:27.4] 0.87 over 0.43 is 2.02 standard errors, and a p-value of 4.4%. That is the Wald test.  

## S05_Flip · Three: just flip  (01:40)

**01:40.3 · s5_1** — *Alder's thirty coins above a histogram that fills in: 100 rounds, 1,000, then 10,000. The exact pile is outlined behind it. The p-value: 0.038.*

> [01:40.3] The third shortcut takes last episode's opening idea seriously. Flip Alder's thirty coins ten thousand times, and simply count.  
> [01:49.2] This run gives a p-value of 3.8%.  

**01:52.9 · s5_2** — *A note on the far tail: nothing rarer than 1 in 10,000 can be reported. A tag: the software calls it a bootstrap.*

> [01:52.9] It homes in on the exact pile as the rounds add up. But with ten thousand rounds, it cannot report anything rarer than one in ten thousand.  
> [02:02.4] The software calls this one a bootstrap.  

## S06_Board · The scoreboard  (02:06)

**02:06.5 · s6_1** — *Alder's p-value four ways: 3.5% exact, 2.5% bell curve, 4.4% ruler, 3.8% flipping, all under a line at 5%.*

> [02:06.5] So, Alder four ways: 3.5% exact, 2.5% by the bell curve, 4.4% by the ruler, 3.8% by flipping.  
> [02:18.3] All below 5%. All four flag Alder, and none of the tests flags anyone else.  

**02:24.2 · s6_2** — *A table of standard units for four clinics by exact, bell curve and ruler. Elm's row: −1.58, −1.55, and −0.69 boxed in red.*

> [02:24.2] But look at Elm. Exact and bell curve agree: about one and a half standard units below the reference.  
> [02:30.7] The ruler says only 0.7. It is measuring from a gamma that does not exist.  

## S07_Fail · Where they fail  (02:38)

**02:38.3 · s7_1** — *Two rows for Alder's ruler test. With the textbook standard error and the risk factor recorded 65 units higher: 38, and 0.02. With the standard error at the average case mix: 0.43, and 2.02.*

> [02:38.3] That is the ruler's first weakness. Its second is one we have met: which standard error?  
> [02:44.0] Record the risk factor sixty-five units higher, as an age in years might be, and the textbook standard error of Alder's gamma becomes 38. The test collapses to 0.02.  
> [02:57.0] Taken at the average case mix, it stays at 2.02.  

**03:01.5 · s7_2** — *Elm's pile with a bell curve over it. The curve runs on to the left of zero; that part is shaded: 6%.*

> [03:01.5] The bell curve's weakness is small numbers. Elm expects fewer than two readmissions, and a bell curve centred there spills below zero.  

**03:10.5 · s7_3** — *Three bars against a line at 5%, for providers under 50 patients who truly equal the reference: exact 4.7%, bell curve 4.9%, ruler 4.0%.*

> [03:10.5] In our crowds where every provider equals the reference, among those with fewer than fifty patients, the exact test flags 4.7%, the bell curve 4.9%, and the ruler only 4.0%.  

## S08_Choose · Which one, when  (03:27)

**03:27.5 · s8_1** — *Three intervals for Alder's ratio on one axis: 1.04 to 2.26 exact, 1.07 to 2.25 bell curve, 1.02 to 2.31 ruler.*

> [03:27.5] Each test also turns inside out into an interval. For Alder's ratio: 1.04 to 2.26, exact. 1.07 to 2.25 by the bell curve. 1.02 to 2.31 by the ruler.  

**03:45.4 · s8_2** — *A card with four rows: exact, for flags; bell curve, for a formula and smooth limits; ruler, for anything built on gamma; flipping, as a check.*

> [03:45.4] So which one, when? The exact test for flags: it is the software's default.  
> [03:50.6] The bell curve when you need a formula. It costs almost nothing, and next time it will draw smooth limits.  
> [03:57.2] The ruler for anything built on gamma itself. And flipping, as a check on the others.  

## S09_Recap · Recap  (04:04)

**04:04.5 · s9_1** — *Three recap cards, each with a small icon.*

> [04:04.5] Let's gather it up.  
> [04:06.1] The bell curve swaps the pile for a normal curve with the same centre and spread.  
> [04:11.0] The ruler measures the gap between sliders in standard errors.  
> [04:15.0] Flipping rebuilds the pile by brute force. On Alder, all three agree with the exact test. On small clinics, they can part ways.  

**04:23.9 · s9_2** — *Five verdicts in a row, then a field of two hundred dots; the next episode's title.*

> [04:23.9] We now have a verdict for every clinic. Five verdicts are easy to read. What about two hundred, or seven thousand?  
> [04:31.2] Next time: the funnel.  

**04:33.3 · s9_3** — *Series end card with the next episode title.*

> [04:33.3] This has been Model in Motion. Thanks for following the story.  
