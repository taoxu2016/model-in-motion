# Model in Motion · The Logistic Fixed-Effect Model · Episode 8: The Arrow Matrix

*how thousands of sliders step at once*

Narration script with timestamps. 690 words, running time 04:52. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *Episode 7's map: the staircase of 54 rounds, then the straight path of five steps.*

> [00:00.0] Last time, taking turns took 54 rounds.  
> [00:03.3] And we ended on a promise: let the sliders and the dial step together, and it takes five.  

**00:09.2 · s1_2** — *Episode 6's machine in miniature: Dune's slider moves, and the dial's meter moves with it.*

> [00:09.2] But stepping together is harder than it sounds.  
> [00:12.1] When Dune's slider moved, two episodes ago, the dial's meter moved too.  
> [00:16.9] To step together, every control has to know how its move disturbs every meter.  

**00:22.4 · s1_3** — *A small 6 × 6 grid beside a vast one: 5 clinics, then 7,000 providers and 50 million cells.*

> [00:22.4] For five clinics, that is a small table. For 7,000 providers, it is 50 million numbers.  
> [00:28.8] So how can this possibly be fast?  

## S02_Title  (00:32)

**00:32.8 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:32.8] Welcome back to Model in Motion.  
> [00:35.0] Today: the arrow matrix.  

## S03_Table · Who disturbs whom  (00:39)

**00:39.1 · s3_1** — *An empty 6 × 6 table. Rows are the six meters, columns the six controls: five clinics and the dial.*

> [00:39.1] Here is that table for our five clinics, at the fit. One row for each meter, one column for each control.  
> [00:46.3] Each cell says how much that meter moves when that control does.  

**00:50.3 · s3_2** — *The diagonal fills in: 6.38, 6.66, 3.82, 2.31, 0.02. Then the corner: 10.20.*

> [00:50.3] Down the diagonal is each clinic's own wobble, from last time: 6.38 for Alder, 6.66 for Birch, down to 0.02 for Elm.  
> [01:01.7] In the corner is the dial's own: 10.2.  

**01:05.2 · s3_3** — *The last row and last column fill in: 0.97, 5.94, 2.35, 0.93, 0.*

> [01:05.2] Along the two edges is how strongly each clinic is tied to the dial.  
> [01:09.7] Birch, with 24 higher-risk patients, most of all: 5.94. Elm, with none: zero.  

**01:16.9 · s3_4** — *The twenty remaining cells show as empty. One is picked out: Alder's slider, Birch's meter. Then an outline traces the arrowhead.*

> [01:16.9] And everywhere else, nothing. Alder's slider cannot move Birch's meter, because no patient belongs to both.  
> [01:24.0] That is not an approximation. It is the model.  
> [01:27.3] Look at the shape it leaves: an arrowhead.  

## S04_Scale · Why the shape matters  (01:31)

**01:31.6 · s4_1** — *A square for the crowd's table, drawn as an arrow: 40,804 cells, 1,004 not zero.*

> [01:31.6] With five clinics, the shape hardly matters. So scale up.  
> [01:35.4] Our crowd of 200 providers, with two risk factors, has a table of 40,804 cells. Only 1,004 of them are not zero.  

**01:46.2 · s4_2** — *A larger square: 7,000 providers, 50 risk factors, 49,702,500 cells, 1.4% not zero.*

> [01:46.2] A national measure, with 7,000 providers and 50 risk factors, has almost 50 million cells. Nearly all of them are empty.  
> [01:55.1] Treat that as an ordinary table, and you are stuck. Use the arrow, and it is easy.  

## S05_Fold · Folding the arrow  (02:02)

**02:03.3 · s5_1** — *The 6 × 6 table again. One clinic's three cells are picked out: its diagonal cell and its two edge cells.*

> [02:03.3] Here is how. Take one clinic at a time.  
> [02:06.2] Square its tie to the dial, divide by its own wobble, and take that away from the corner.  

**02:11.9 · s5_2** — *Clinic by clinic, a small amount leaves the corner: 0.15, 5.30, 1.45, 0.38, 0. The corner counts down from 10.20 to 2.93.*

> [02:11.9] Alder takes away 0.15. Birch, 5.30. Cedar, 1.45. Dune, 0.38. Elm, nothing.  
> [02:22.8] The corner falls from 10.2 to 2.93.  

**02:26.8 · s5_3** — *The clinic rows and columns dim. Only the corner cell stays lit: 2.93.*

> [02:26.8] And now the sliders are out of the problem. What is left is one small number, for the dial alone.  

**02:33.3 · s5_4** — *The same 2.93 built another way: 0.82 + 0.64 + 0.90 + 0.56 + 0, one piece per clinic.*

> [02:33.3] That number has a meaning. It adds up, clinic by clinic, how much patients differ in risk from others in their own clinic.  
> [02:41.1] Elm, where every patient is lower-risk, adds nothing. It is Episode 4's idea again: the risk rule is learned inside clinics.  

**02:50.0 · s5_5** — *Two bars: 10.20 before folding, 2.93 after. A label: 3.5 times.*

> [02:50.0] It is also a warning. Ignore the clinics, and the data would seem to say three and a half times as much about the dial as they really do.  

## S06_Step · One step, together  (03:00)

**03:01.2 · s6_1** — *The machine at the plain guess. Beside the dial: its first step, 1.81.*

> [03:01.2] So the dial's step takes one division. From the plain guess, it is 1.81.  
> [03:06.8] Then each clinic takes its own step, corrected for what the dial just did.  

**03:11.7 · s6_2** — *Sliders and dial move at once. A step counter: 1, 2, 3, then 5. The meters level.*

> [03:11.7] Watch the machine. One joint step, and the dial reads 1.81. A second: 2.00. A third: 2.0164, the top.  
> [03:23.0] Five steps until the dial stops moving, where taking turns needed 54.  

**03:28.3 · s6_3** — *Three rows: the risk factor recorded as 0 and 1, as 5 and 6, as 50 and 51. Five steps each time.*

> [03:28.3] And the trouble with where we put zero? Record the risk factor five units higher, or fifty. The joint path does not change at all.  

## S07_Cost · What it buys  (03:38)

**03:38.3 · s7_1** — *Three jobs in a row: add up over patients, fold once per provider, solve one small system. Then a test: 2,000 providers, 205,367 patients, under a second.*

> [03:38.3] Each step is three cheap jobs: add up over the patients, fold once for each provider, and solve one small system.  
> [03:45.9] We tried it on 2,000 providers and about 200,000 patients. The fit took well under a second.  

**03:53.3 · s7_2** — *The same data as an ordinary table: 2,002 columns wide, 3.3 gigabytes.*

> [03:53.3] Written out as an ordinary table, with a column for every provider, the same data would fill 3.3 gigabytes before any fitting began.  

**04:03.0 · s7_3** — *A caution card: one patient, one provider. A second grouping drawn across the first, and the empty cells fill in.*

> [04:03.0] So a separate number for every provider is not a computing problem. It only looked like one.  
> [04:08.8] One caution. The arrow needs every patient to belong to exactly one provider. A second grouping that cuts across the first would break it.  

## S08_Recap · Recap  (04:19)

**04:19.9 · s8_1** — *Three recap cards, each with a small icon.*

> [04:19.9] Let's gather it up.  
> [04:21.4] Clinics disturb each other only through the dial, so the table is an arrow.  
> [04:26.0] Fold each clinic into the corner, and one small system is left.  
> [04:30.3] Nothing is approximated. It is last episode's step, taken for everything at once.  

**04:36.1 · s8_2** — *The folded number, 2.93, large; the next episode's title.*

> [04:36.1] And keep an eye on that folded number, 2.93. It says how firmly the data hold the dial in place.  
> [04:43.5] Next time: how sure are we?  

**04:45.8 · s8_3** — *Series end card with the next episode title.*

> [04:45.8] This has been Model in Motion. Thanks for following the story.  
