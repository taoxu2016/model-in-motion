# Model in Motion · The Logistic Fixed-Effect Model · Episode 2: Odds and the S-Curve

*how risk factors become a probability*

Narration script with timestamps. 723 words, running time 05:00. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *Last episode's patient, with three risk-factor tags, above a probability ruler from 0 to 100%.*

> [00:00.0] Last time, we ended with a wish: one ruler for risk, where everything we know about a patient turns into a single probability.  

**00:08.7 · s1_2** — *The chip settles on the ruler at 20%.*

> [00:08.7] Here's the obvious way to build it.  
> [00:11.0] Start a typical patient at 20%, then add points for each risk factor.  

**00:16.3 · s1_3** — *Each tag drops in and the chip hops right: 45%, 75%, then off the end of the ruler.*

> [00:16.3] Age 81: plus 25. Diabetes: plus 30. A third hospital stay this year: plus 35.  

**00:24.0 · s1_4** — *The chip hangs past the end of the ruler at 110%, marked in coral.*

> [00:24.0] That's 110%.  
> [00:26.2] A probability can't do that. Adding points was the wrong move, on the wrong ruler.  

## S02_Title  (00:33)

**00:33.1 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:33.1] Welcome back to Model in Motion.  
> [00:35.3] Today: odds, and the curve that turns any patient into a probability.  

## S03_Odds · Odds  (00:42)

**00:42.0 · s3_1** — *Ten chips in a row; two fill.*

> [00:42.0] Let's try a different ruler.  
> [00:43.9] Take ten patients who each have a 20% chance of coming back. On average, two do, and eight don't.  

**00:50.9 · s3_2** — *A bracket over all ten: probability 20%. Then the two set against the eight: odds 1 to 4.*

> [00:50.9] Probability compares the two with all ten.  
> [00:53.7] Odds compare the two with the eight: one to four, or a quarter.  

**00:57.9 · s3_3** — *A probability ruler and an odds ruler with linked markers; the chips refill to five, then eight.*

> [00:57.9] At 50%, it's five against five: odds of one.  
> [01:01.8] At 80%, eight against two: odds of four.  

**01:05.4 · s3_4** — *The probability marker creeps toward 100% while the odds marker runs off the end: 9, 99, 999.*

> [01:05.4] And as the probability creeps toward 100%, the odds just keep running: 9, 99, 999.  
> [01:14.2] This ruler has no ceiling.  

## S04_LogOdds · Log-odds  (01:17)

**01:17.6 · s4_1** — *On the odds ruler, the short stretch from 0 to 1 is bracketed: everyone below fifty-fifty.*

> [01:17.6] But it's a lopsided ruler.  
> [01:19.5] Every patient below fifty-fifty is squeezed between zero and one, while everyone above gets all the room in the world.  

**01:27.2 · s4_2** — *A copy of the ruler stretches: the ticks at 1/4, 1/2, 1, 2, 4 slide until they are evenly spaced.*

> [01:27.2] The cure is a logarithm.  
> [01:29.2] On a log scale, every doubling of the odds is one equal step: a quarter, a half, one, two, four.  

**01:35.8 · s4_3** — *Three rulers stacked: probability, odds, log-odds, with one patient tracked on all three at 50%, 20% and 80%.*

> [01:35.8] This is the log-odds ruler. Fifty-fifty sits at zero.  
> [01:39.7] 20% is about minus 1.4, and 80% is plus 1.4: perfectly symmetric.  

**01:47.3 · s4_4** — *The patient slides far left and far right; the log-odds ruler never ends.*

> [01:47.3] And it runs forever in both directions. No floor, no ceiling, nothing to bump into.  

## S05_Steps · Where risks add  (01:54)

**01:54.6 · s5_1** — *A yellow arrow of length 1.39 on the log-odds ruler.*

> [01:54.6] Here's why that matters. On the log-odds ruler, a risk factor is simply a step.  
> [01:59.8] Take one that multiplies the odds by four: a step of 1.4 to the right.  

**02:05.6 · s5_2** — *Four patients at 5%, 20%, 50% and 80% each take the same step on the log-odds ruler.*

> [02:05.6] Now give that same step to four different patients.  

**02:09.0 · s5_3** — *On the probability ruler their jumps appear one by one: +12, +30, +30, +14 points.*

> [02:09.0] On the probability ruler, 5% becomes 17%. 20% becomes 50%. 50% becomes 80%. And 80% becomes 94%.  

**02:18.4 · s5_4** — *The four equal yellow steps pulse, then the four unequal jumps; the 100% end stays untouched.*

> [02:18.4] Same step, very different jumps: big in the middle, small near the ends.  
> [02:22.9] And nobody ever goes past one hundred.  

## S06_Curve · The S-curve  (02:27)

**02:27.0 · s6_1** — *Axes: earlier hospital stays along the bottom, log-odds up the side. Nine dots climb in equal steps.*

> [02:27.0] Now picture a risk factor that comes in amounts, like the number of earlier hospital stays.  
> [02:32.8] Suppose each extra stay is one more equal step in log-odds.  

**02:37.4 · s6_2** — *A straight line through the dots; a yellow slope triangle labelled beta.*

> [02:37.4] On this scale, the pattern is a straight line. Its slope is the size of the step, and we'll call it beta.  

**02:44.0 · s6_3** — *The vertical axis becomes probability; the dots move and the line bends into an S.*

> [02:44.0] Now switch the vertical axis back to probability.  
> [02:47.3] The line bends into an S: steep in the middle, flat at both ends, and always between zero and one.  

**02:54.1 · s6_4** — *A tangent slides along the curve; a bar shows p(1 - p), longest at 50%.*

> [02:54.1] How steep it is depends on where you stand. The steepness is proportional to p times one minus p: greatest at fifty-fifty, fading to nothing at the ends.  
> [03:04.5] Keep that in your pocket. It comes back when we fit the model.  

**03:08.4 · s6_5** — *A yellow beta dial turns and the S steepens; then the curve slides left and right.*

> [03:08.4] Turn beta up, and the S gets steeper.  
> [03:11.1] Shift the starting point, and the whole curve slides sideways.  

## S07_Cedar · One real clinic  (03:16)

**03:16.8 · s7_1** — *Cedar's twenty chips in two blocks of ten: 2 filled on the left, 6 on the right.*

> [03:16.8] Let's fit one of these by hand. Remember Cedar?  
> [03:20.0] Ten lower-risk patients, 2 readmitted. Ten higher-risk patients, 6 readmitted.  

**03:25.9 · s7_2** — *Under each block: 2 : 8, odds 0.25; and 6 : 4, odds 1.5.*

> [03:25.9] So the odds are 2 to 8, a quarter; and 6 to 4, one and a half.  

**03:30.5 · s7_3** — *Between them: times 6, the odds ratio.*

> [03:30.5] Divide one by the other, and you get an odds ratio of six. At Cedar, higher risk multiplies the odds by six.  

**03:38.7 · s7_4** — *A log-odds ruler: a chip at -1.39, a yellow step of 1.79 to +0.41; the model written underneath.*

> [03:38.7] On the log-odds ruler, that's a step of 1.79, starting from minus 1.39.  
> [03:45.4] Those two numbers are a complete logistic model of Cedar.  

**03:49.4 · s7_5** — *Between the two probabilities: times 3. The 6 and the 3 sit one above the other.*

> [03:49.4] One caution. Six times the odds is not six times the risk.  
> [03:53.8] Cedar's rate went from 20% to 60%: three times, not six.  

## S08_RiskChip · The risk chip  (04:00)

**04:00.0 · s8_1** — *The patient again, on two rulers: probability above, log-odds below; a faded 110% past the end.*

> [04:00.0] Now, back to our patient. This time, we add on the right ruler.  

**04:04.5 · s8_2** — *Three yellow steps stack on the log-odds ruler; the probability marker moves 45%, 77%, 94%.*

> [04:04.5] Each risk factor is a step in log-odds, and the steps simply stack, one after another.  

**04:10.2 · s8_3** — *94% lights up; the old 110% is struck through.*

> [04:10.2] And the probability? 94%.  
> [04:13.1] High, but still a probability.  

**04:15.5 · s8_4** — *The chip gains a shaded slice of 94%; chips with 20% and 50% slices appear beside it.*

> [04:15.5] From now on, every chip carries its probability with it, as a shaded slice.  
> [04:20.5] A sliver for a low-risk patient; nearly the whole disc for this one.  

## S09_Recap · Recap  (04:26)

**04:26.4 · s9_1** — *Three recap cards, each with a small icon.*

> [04:26.4] Let's gather it up.  
> [04:27.9] Odds compare the patients who come back with those who don't.  
> [04:31.4] Log-odds is the ruler where risk factors add.  
> [04:34.6] And the S-curve carries the sum back to a probability.  

**04:38.0 · s9_2** — *Cedar's twenty chips, each with its slice; the slices pour into one bar: expected 8.0.*

> [04:38.0] So now every patient has a probability.  
> [04:40.9] Add them up across a clinic, and you get a number of patients: the readmissions we should expect.  

**04:47.0 · s9_3** — *Beside the bar, Cedar's eight filled chips: observed. Next episode title.*

> [04:47.0] Next time, we'll set that number beside what actually happened. Observed, versus expected.  

**04:53.4 · s9_4** — *Series end card with the next episode title.*

> [04:53.4] This has been Model in Motion. Thanks for following the story.  
