# Model in Motion · The Logistic Fixed-Effect Model · Episode 10: No Events, No Peak

*what a clinic with no readmissions can tell us*

Narration script with timestamps. 617 words, running time 04:31. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *Five bars, one per clinic: the share of patients readmitted. Elm's bar is empty: 0 of 11.*

> [00:00.0] One clinic has waited six episodes for its turn.  
> [00:03.2] Elm: 11 patients, all lower-risk, and not one readmission. The best record in the cast.  

**00:09.8 · s1_2** — *Two printouts side by side, one from each fitting routine: Elm's gamma as −6.25, and as −11.52.*

> [00:09.8] So what is Elm's gamma? Ask the software, and it prints minus 6.25.  
> [00:15.1] Ask again with its other fitting routine, and it prints minus 11.52.  
> [00:20.6] Same patients. Same model. Two answers.  

**00:23.8 · s1_3** — *Both printouts are struck through. One word: neither.*

> [00:23.8] Which one is right? Neither. And seeing why shows us what to trust instead.  

## S02_Title  (00:30)

**00:30.2 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:30.2] Welcome back to Model in Motion.  
> [00:32.4] Today: no events, no peak.  

## S03_Ramp · A hill with no top  (00:36)

**00:36.7 · s3_1** — *Elm's own hill: height against the position of its slider. Three points are marked: −2.17 at the middle clinic's level, −0.53 at −3, −0.02 at −6.25.*

> [00:36.7] Here is Elm's own hill: the height, for each position of its slider.  
> [00:41.1] With the slider at the middle clinic's level, the height is minus 2.17. At minus 3, it is minus 0.53. At minus 6.25, minus 0.02.  

**00:54.6 · s3_2** — *A dashed ceiling at zero. The curve runs on to the left under it, with a fourth point: −0.0001 at −11.5.*

> [00:54.6] It keeps rising, more and more slowly, toward a ceiling at zero that it never reaches.  
> [01:00.2] A ramp, not a hill. There is no top to find.  

**01:03.6 · s3_3** — *A dot slides down the ramp. Beside it, Elm's meter: observed 0, expected falling from 1.97 to 0.02 and never reaching zero.*

> [01:03.6] The meter tells the same story. Elm observed no readmissions. But wherever the slider sits, the model expects more than none.  
> [01:12.2] So expected always exceeds observed, and the meter always says: lower.  

## S04_March · Where the slider stops  (01:18)

**01:18.9 · s4_1** — *Elm's slider on a long track, stepping left: −2.06, −3.19, −4.23, −5.24, −6.25. A flag at −6.25: stepping together, 5 steps.*

> [01:18.9] So the slider marches, about one unit a step, for as long as the fitting runs.  
> [01:24.0] Stepping together stops once the dial has settled. That takes five steps, and leaves Elm's slider at minus 6.25.  

**01:32.4 · s4_2** — *The slider marches on until it meets a wall drawn at −11.52, ten units below the middle clinic. A note: without the wall, still running after 10,000 rounds.*

> [01:32.4] Taking turns waits for every slider to settle, and Elm's never will.  
> [01:36.8] So the software builds a wall, ten units below the middle clinic. Elm's slider runs into it and stops: minus 11.52.  

**01:46.0 · s4_3** — *Two more flags on the track: −5.24 with a looser stopping rule, −7.25 with a tighter one.*

> [01:46.0] Even the stopping rule matters. Loosen it, and stepping together prints minus 5.24. Tighten it: minus 7.25.  

**01:55.6 · s4_4** — *Four printed values for Elm in a row. Under them, the dial and the other four clinics: the same in every run.*

> [01:55.6] Each of these numbers records when an algorithm stopped. None of them is an estimate.  
> [02:00.9] And nothing else is harmed. The dial and the other four sliders finish in the same place every time.  

## S05_Breaks · What breaks  (02:09)

**02:09.0 · s5_1** — *Episode 9's hatched interval for Elm: −19.7 to +7.2.*

> [02:09.0] What breaks is anything built on that number.  
> [02:11.6] Last episode's interval, from minus 19.7 to plus 7.2, was one casualty.  

**02:18.7 · s5_2** — *A long log-odds ruler with all five clinics. A marker for the size-weighted average sits at −1.75; Elm moves from −6.25 to −11.52 and the marker slides to −2.31. Alder's ratio changes from 1.87 to 2.76.*

> [02:18.7] Here is a worse one. Suppose the reference is the average gamma, weighted by size.  
> [02:24.2] That average is minus 1.75 after one routine, and minus 2.31 after the other.  
> [02:31.5] Measured against it, Alder's readmissions come out at 1.87 times expected, or 2.76 times. Alder's patients did not change. Elm's stopping point did.  

**02:44.4 · s5_3** — *One line: a clinic with no readmissions has moved the yardstick for everyone.*

> [02:44.4] A clinic with no readmissions has quietly moved the yardstick for everyone.  

## S06_Survives · What survives  (02:50)

**02:50.8 · s6_1** — *The same ruler. The middle clinic's marker stays at −1.52 while Elm moves between −6.25 and −11.52.*

> [02:50.8] What survives is anything built on the count.  
> [02:53.6] Take the middle clinic as the reference instead. The median does not care how far out Elm's slider went: minus 1.52, either way.  

**03:03.3 · s6_2** — *Elm's 11 patients as a row of markers, each labelled 82%. Expected 1.97 against observed 0. The product: 11%.*

> [03:03.3] At that reference, Elm's 11 patients would expect 1.97 readmissions. Elm had none.  
> [03:10.3] How surprising is none? Each patient has an 82% chance of staying out. For all eleven, that comes to 11%.  

**03:19.1 · s6_3** — *A verdict: 11%, not flagged.*

> [03:19.1] Eleven percent is not rare. So Elm is not flagged. Zero is not automatically excellent.  

**03:25.8 · s6_4** — *A curve: the chance of no readmissions against the number of such patients, with a line at 5%. Points at 11 patients, at 16 and at 30.*

> [03:25.8] But thirty such patients with no readmissions would be another matter: about three chances in a thousand.  
> [03:32.5] The count speaks, even when gamma cannot.  

## S07_Footnotes · Two footnotes  (03:36)

**03:36.9 · s7_1** — *The track again, with a wall at each end, ten units either side of the middle clinic. A second slider runs right, into the upper wall.*

> [03:36.9] Two footnotes. First, the mirror image: a clinic where every patient is readmitted runs to an upper wall instead.  

**03:45.0 · s7_2** — *Six clinics by size: 30, 30, 20, 12, 11, and Fen with 8. A line marks the screen: more than 10 records. Fen falls below it.*

> [03:45.0] Second, there was a sixth clinic. Fen, with 8 patients, never entered the fit, because the software screens out any provider with 10 records or fewer.  
> [03:54.8] Elm, with 11, stayed in by a single patient.  

## S08_Recap · Recap  (03:59)

**03:59.7 · s8_1** — *Three recap cards, each with a small icon.*

> [03:59.7] Let's gather it up.  
> [04:01.3] No readmissions means a hill with no top, and a printed gamma that only records where the fitting stopped.  
> [04:08.0] Anything built on that gamma breaks. Anything built on the count survives.  
> [04:12.6] And zero, from a handful of patients, is weak evidence.  

**04:16.5 · s8_2** — *Observed 0 against expected 1.97, large; the next episode's title.*

> [04:16.5] That count, set against what the reference would expect, is the measure this whole series has been heading for.  
> [04:22.8] Next time: swap the curve.  

**04:25.1 · s8_3** — *Series end card with the next episode title.*

> [04:25.1] This has been Model in Motion. Thanks for following the story.  
