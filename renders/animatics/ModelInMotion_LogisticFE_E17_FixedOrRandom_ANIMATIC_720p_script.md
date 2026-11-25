# Model in Motion · The Logistic Fixed-Effect Model · Episode 17: Fixed or Random?

*pull the estimates together, or let each stand alone*

Narration script with timestamps. 601 words, running time 04:29. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *The cast's four estimates on a line, highest at the top: Dune at −0.58, Alder at −0.65, Cedar at −1.52, Birch at −1.82. Dune is marked as the highest, with its 12 patients.*

> [00:00.0] Dune's number is minus 0.58: the highest of any clinic. On that number, Dune is the worst performer in the cast.  
> [00:08.7] It comes from 12 patients.  

**00:10.9 · s1_2** — *Alder beside it: −0.65, from 30 patients. Each clinic's patients shown as a block of chips. A question: which is truly the worst?*

> [00:10.9] Alder is just behind, at minus 0.65, from 30 patients.  
> [00:16.4] If you had to bet on which clinic is truly the worst, would you still pick Dune?  

**00:21.2 · s1_3** — *Faint arrows from every estimate toward the centre line, longest for the clinics with fewest patients.*

> [00:21.2] Many analysts would not. They would pull every estimate toward the average, and pull hardest where there is least to go on.  
> [00:28.6] That is the random-effect model, and this episode is about what it buys and what it costs.  

## S02_Title  (00:36)

**00:36.0 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:36.0] Welcome back to Model in Motion.  
> [00:38.2] Today: fixed or random?  

## S03_Assume · A different assumption  (00:42)

**00:42.3 · s3_1** — *Left: four separate dots, labelled fixed: nothing assumed. Right: the same dots under one bell curve with a centre and a spread, labelled random: draws from one curve.*

> [00:42.3] So far, each provider has had a number of its own, and we have assumed nothing about those numbers. That is what fixed means.  
> [00:50.3] The alternative assumes something: that the numbers are draws from one bell curve, with a centre and a spread.  

**00:57.3 · s3_2** — *Dune's estimate joined to the centre by a band. The formula for reliability: spread squared over spread squared plus standard error squared. With 0.33 and 0.66: 0.20.*

> [00:57.3] Then each estimate is a compromise between the provider's own data and the centre. The weight on its own data is called its reliability.  
> [01:06.4] For Dune, with a spread of 0.33 borrowed from our crowd, the reliability is 0.20. Dune keeps a fifth of its distance from the centre.  

**01:17.0 · s3_3** — *All five clinics, before and after the pull: Dune −0.58 to −1.33, Alder −0.65 to −1.18, Birch −1.82 to −1.65, Cedar unmoved at −1.52, and Elm, which had none, at −1.71.*

> [01:17.0] Do that for every clinic. Dune moves to minus 1.33. Alder, with more patients, keeps two fifths, and stops at minus 1.18.  
> [01:27.3] The order has flipped. And Elm, which had no estimate at all, now has one.  

## S04_Pull · The pull, in the crowd  (01:33)

**01:34.8 · s4_1** — *The two hundred providers by number of patients. For each, a line from its fixed-effect estimate to its random-effect one. The lines are long on the left and short on the right.*

> [01:34.8] Now the crowd of two hundred, fitted both ways. Each line joins a provider's fixed-effect estimate to its random-effect one.  
> [01:43.1] Small providers move most. Under 50 patients, a typical reliability is 0.37. Above 200, it is 0.83.  

**01:53.6 · s4_2** — *Three piles of two hundred values: fixed-effect estimates, spread 0.44; the truth, 0.33; random-effect estimates, 0.26.*

> [01:53.6] The estimates draw together. Their spread falls from 0.44 to 0.26.  
> [02:00.1] The true spread is 0.33. Fixed effects scatter wider than the truth; random effects, narrower.  

## S05_Buys · What it buys  (02:08)

**02:09.9 · s5_1** — *Each provider's error against its number of patients, for both fits. Bars for the typical error: 0.28 and 0.20 overall; 0.40 and 0.25 under 50 patients.*

> [02:09.9] What does the pull buy? Accuracy, on average. We know the truth in this crowd, so we can measure the typical error.  
> [02:16.9] It falls from 0.28 to 0.20. For providers under 50 patients, from 0.40 to 0.25.  

## S06_Outliers · What it costs: the outliers  (02:28)

**02:29.3 · s6_1** — *The six planted providers on a line marked at 0.8 either side of the centre. Their fixed-effect estimates average 0.67 from the centre; their random-effect ones, 0.46. Flags: four and three.*

> [02:29.3] Now the costs. First, the pull does not know who truly differs. Our six planted providers sit 0.8 from the centre.  
> [02:37.9] Fixed effects put them at 0.67, on average. Random effects, at 0.46.  
> [02:45.0] And fixed effects flag four of the six; random effects, three.  

## S07_CaseMix · What it costs: the case mix  (02:50)

**02:50.8 · s7_1** — *True provider effects against case mix: a downward cloud. Providers with sicker patients truly do better.*

> [02:50.8] The second cost is subtler. In this crowd, providers with sicker patients truly perform better. The random-effect model assumes there is no such link, and pulls everyone toward one centre.  

**03:03.4 · s7_2** — *Each provider's error against its case mix, two panels. Fixed effects: a level cloud, correlation 0.06. Random effects: a rising cloud, 0.35; the sickest fifth 0.10 too high, the healthiest 0.10 too low.*

> [03:03.4] So its errors follow the case mix. Their correlation with it is 0.35. For fixed effects, 0.06.  
> [03:12.4] The sickest fifth of providers look 0.10 worse than they are. The healthiest fifth, 0.10 better.  

**03:19.9 · s7_3** — *The random-effect panel again, for the same crowd with the link broken: a level cloud, correlation −0.01.*

> [03:19.9] Break the link, so that performance and case mix are unrelated, and that correlation vanishes.  

## S08_Choose · Which to use  (03:27)

**03:27.5 · s8_1** — *Two cards. Fixed effects: judging individual providers, when performance may be tied to case mix. Random effects: many tiny providers, or questions about providers as a population.*

> [03:27.5] So which? If you are judging individual providers, and performance may be tied to case mix, fixed effects.  
> [03:34.4] If you have many tiny providers, or your question is about providers as a population, random effects.  

**03:41.6 · s8_2** — *Both cards feed one box: the standardization of Episode 11, observed over expected. Under it, a caution that applies to both: a risk factor nobody recorded.*

> [03:41.6] Either way, the estimates feed the same standardization from Episode 11. The choice changes the numbers that go in, not the arithmetic that follows.  
> [03:51.3] And neither one protects you from a risk factor that nobody recorded.  

## S09_Recap · Recap  (03:57)

**03:57.3 · s9_1** — *Three recap cards, each with a small icon.*

> [03:57.3] Let's gather it up.  
> [03:58.9] Random effects pull each estimate toward the centre, by its reliability.  
> [04:03.8] The pull buys accuracy on average, and gives every provider an estimate.  
> [04:08.6] It costs you the outliers, and it bends with the case mix.  

**04:12.4 · s9_2** — *A long row of small intercept markers, one per provider, running off the edge of the frame. The next episode's title.*

> [04:12.4] Fixed effects have a cost of their own that we have not faced. One intercept per provider is a great many intercepts.  
> [04:20.1] Next time: too many intercepts.  

**04:22.7 · s9_3** — *Series end card with the next episode title.*

> [04:22.7] This has been Model in Motion. Thanks for following the story.  
