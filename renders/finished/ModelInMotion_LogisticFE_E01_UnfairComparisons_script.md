# Model in Motion · The Logistic Fixed-Effect Model · Episode 1: Unfair Comparisons

*case mix and raw rates*

Narration script with timestamps. 878 words, running time 05:52. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *Five clinic trays fade in. Chips pop in as hollow rings, then some fill. The question appears on top.*

> [00:00.0] Here's a question that sounds simple.  
> [00:02.3] Five clinics send their patients home. Some of those patients are back in hospital within thirty days. Which clinic is doing the best job?  

**00:11.3 · s1_2** — *Legend: filled chip = readmitted, hollow chip = not readmitted.*

> [00:11.3] Each chip is one patient. A filled chip is a patient who was readmitted.  

**00:16.4 · s1_3** — *A rate bar and a percentage grow under each tray in turn.*

> [00:16.4] The obvious move is to count. At Alder, 13 of 30 patients came back: that's 43%.  
> [00:23.4] Birch, 47%. Cedar, 40%. Dune, 58%. And at Elm, nobody at all.  

**00:30.3 · s1_4** — *The trays slide into rank order: Elm, Cedar, Alder, Birch, Dune. Rank numbers appear.*

> [00:30.3] Line them up from lowest to highest, and we have a league table.  
> [00:34.0] Elm in first place, Dune in last, and Alder just ahead of Birch.  

**00:38.5 · s1_5** — *Everything dims except Alder and Birch; a swap mark hangs between them.*

> [00:38.5] It looks like an answer. But for those two, the table has it backwards.  

## S02_Title  (00:44)

**00:44.5 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:44.5] Welcome to Model in Motion, where we build statistical models one moving piece at a time.  
> [00:50.2] This is the start of a new story: how to compare providers fairly. Today, unfair comparisons, and what a fair one would need.  

## S03_CaseMix · Who walked in the door  (01:00)

**01:00.7 · s3_1** — *Alder and Birch as two large trays of jumbled chips.*

> [01:00.7] Let's look more closely at Alder and Birch.  
> [01:03.3] So far, we've treated every patient as interchangeable. They aren't.  

**01:08.3 · s3_2** — *A pale ring grows around every higher-risk patient.*

> [01:08.3] Some are frail, or going home after a long and complicated stay. Patients like that are more likely to come back, wherever they're treated.  
> [01:17.4] Let's mark those higher-risk patients with a ring.  

**01:20.4 · s3_3** — *Chips sort inside each tray: lower-risk left, higher-risk right.*

> [01:20.4] Now sort the chips: lower-risk patients on the left, higher-risk on the right.  

**01:25.4 · s3_4** — *Counts appear under each pile; Alder's big lower-risk pile and Birch's big higher-risk pile light up.*

> [01:25.4] Look at who each clinic is caring for. At Alder, 24 of the 30 patients are lower-risk.  
> [01:31.9] Birch is the mirror image: 24 of its 30 are higher-risk.  

**01:36.5 · s3_5** — *The term 'case mix' appears.*

> [01:36.5] This is a clinic's case mix: the kind of patients it serves. And these two could hardly be more different.  

## S04_LikeWithLike · Like with like  (01:44)

**01:44.0 · s4_1** — *The higher-risk piles dim.*

> [01:44.0] So let's compare like with like, starting with the lower-risk patients.  

**01:48.0 · s4_2** — *Row one of a scoreboard: 8 of 24 = 33% against 1 of 6 = 17%; Birch's number turns green.*

> [01:48.0] At Alder, 8 of 24 were readmitted: one in three. At Birch, 1 of 6: about 17%.  
> [01:55.6] For these patients, Birch does better.  

**01:58.4 · s4_3** — *Row two: 5 of 6 = 83% against 13 of 24 = 54%; Birch's number turns green.*

> [01:58.4] Now the higher-risk patients. Alder: 5 of 6, or 83%. Birch: 13 of 24, or 54%.  
> [02:07.3] Birch does better again.  

**02:09.4 · s4_4** — *Row three, everyone: 43% against 47%; this time Alder's number is the lower one.*

> [02:09.4] Lower-risk patients do better at Birch. Higher-risk patients do better at Birch.  
> [02:14.4] And yet, put everyone back together, and it's Alder with the lower rate.  

**02:18.9 · s4_5** — *The label 'Simpson's paradox' appears under the scoreboard.*

> [02:18.9] Nothing is wrong with the arithmetic. This is Simpson's paradox, and it lies in wait wherever groups with different mixes are compared.  

## S05_Balance · A balancing act  (02:28)

**02:28.9 · s5_1** — *Two beams marked 0 to 100%. Each clinic's chips fly from its tray onto its beam, as a pile at each group's rate.*

> [02:28.9] Here's what's going on. Give each clinic a beam, marked from zero to one hundred percent.  
> [02:34.7] Each group of patients sits on the beam at its own readmission rate.  

**02:39.3 · s5_2** — *A pivot appears under Alder's beam; the beam tips toward the heavy pile.*

> [02:39.3] A clinic's overall rate is the point where its beam balances. And that depends on how much weight sits at each end.  

**02:46.9 · s5_3** — *Alder's pivot slides left until the beam levels at 43%.*

> [02:46.9] Alder's patients are mostly lower-risk, so its balance point sits near the low end: 43%.  

**02:53.6 · s5_4** — *Guides show both of Birch's piles left of Alder's. Birch's pivot slides right to 47%.*

> [02:53.6] Birch's piles both sit further left: lower rates in both groups.  
> [02:58.1] But most of its weight is at the higher-risk end, and that drags the balance point up to 47%.  

**03:05.0 · s5_5** — *Two tags: where the piles sit = performance; how heavy they are = case mix.*

> [03:05.0] So a raw rate blends two things: how well a clinic performs, and who walked in the door.  

## S06_Trade · Trading patients  (03:11)

**03:11.6 · s6_1** — *The chips trade beams: Birch's blue piles rise to Alder's beam, Alder's orange piles drop to Birch's.*

> [03:11.6] Here's a way to feel the difference. Imagine the two clinics traded patients.  

**03:17.4 · s6_2** — *Alder's beam tips right; its pivot slides to 73%. A link joins it to Birch's own 47%.*

> [03:17.4] Alder's two rates stay where they were. But now it carries Birch's patients, and its balance point slides all the way up to 73%.  
> [03:26.5] With those same patients, Birch managed 47%.  

**03:30.1 · s6_3** — *Birch's pivot slides down to 24%. A second link joins it to Alder's own 43%.*

> [03:30.1] And Birch, with Alder's easier mix? Its balance point falls to 24%, where Alder had 43%.  

**03:37.5 · s6_4** — *Both links lean the same way: on the same patients, Birch is lower both times.*

> [03:37.5] Whichever set of patients you choose, Birch comes out well ahead. The league table had these two the wrong way round.  

## S07_Crowd · Two hundred providers  (03:46)

**03:46.1 · s7_1** — *200 dots appear as a block.*

> [03:46.1] Two clinics could be a fluke. So let's zoom out to 200 providers.  
> [03:50.3] They're simulated, which means we know how good each one truly is.  

**03:54.7 · s7_2** — *Dots line up along the bottom by true performance, then rise to their raw-rate rank.*

> [03:54.7] Line them up from truly best on the left to truly worst on the right.  
> [03:59.0] Then lift each one by its raw rate: lowest at the bottom, highest at the top.  

**04:04.4 · s7_3** — *A dashed diagonal; the readout shows rank correlation 0.16.*

> [04:04.4] If raw rates told the truth, the dots would hug the diagonal. Instead, they're scattered almost everywhere: a rank correlation of just 0.16.  

**04:15.2 · s7_4** — *A five-by-five grid; the diagonal blocks glow; dots outside them turn coral; 142 of 200.*

> [04:15.2] Cut the table into fifths, and 142 of the 200 providers land in the wrong one.  

**04:21.8 · s7_5** — *The x-axis is relabelled by how sick the patients are; dots slide sideways into a clear trend; 0.58.*

> [04:21.8] Now re-sort the very same providers by how sick their patients are.  
> [04:26.4] There's the pattern the raw rates were following all along: a correlation of 0.58.  

## S08_Luck · And then there's luck  (04:34)

**04:34.3 · s8_1** — *The league table returns; Elm and Dune light up.*

> [04:34.3] There's a second problem in that league table, and it has nothing to do with case mix. Look at the two extremes.  

**04:41.0 · s8_2** — *The patient counts under Dune and Elm pulse: 12 and 11.*

> [04:41.0] Dune's 58% rests on 12 patients. Elm's perfect zero, on 11.  

**04:47.1 · s8_3** — *Outcomes are re-dealt again and again; bars jump; a tick is left at every rate visited.*

> [04:47.1] So try an experiment. Suppose all five clinics were secretly identical: every patient with the same four-in-ten chance of coming back. Now deal out the luck. And again. And again.  
> [04:59.6] Even the bigger clinics wobble. The smallest swing much further.  

**05:03.6 · s8_4** — *A bracket spans each clinic's ticks.*

> [05:03.6] So before trusting any gap between providers, we'll have to ask how much of it chance alone could produce. That question gets an episode of its own.  

## S09_Recap · Recap  (05:14)

**05:14.4 · s9_1** — *Three recap cards, each with a small icon.*

> [05:14.4] Let's gather it up.  
> [05:16.0] A raw rate blends performance with case mix.  
> [05:18.9] Compare like with like, and a ranking can flip.  
> [05:21.8] And small providers swing with chance.  

**05:24.4 · s9_2** — *One chip sprouts many attribute tags; the two piles keep splitting into ever smaller ones.*

> [05:24.4] What we really want is to compare providers as if they had all treated the same patients.  
> [05:29.7] With one risk factor, sorting chips into two piles was enough. But real patients differ in dozens of ways at once.  

**05:37.6 · s9_3** — *The tags collapse onto one ruler from 0 to 100%; the chip slides along it. Next episode title.*

> [05:37.6] So next time, we'll build a single ruler for risk: a way to turn everything we know about a patient into one probability.  

**05:45.7 · s9_4** — *Series end card with the next episode title.*

> [05:45.7] This has been Model in Motion. Thanks for following the story.  
