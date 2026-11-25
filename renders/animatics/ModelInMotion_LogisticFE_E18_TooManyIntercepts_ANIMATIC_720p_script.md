# Model in Motion · The Logistic Fixed-Effect Model · Episode 18: Too Many Intercepts

*when one intercept per provider bends the shared rule*

Narration script with timestamps. 567 words, running time 03:55. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *One provider with two patients, drawn as two chips under one intercept marker. Then a field of such pairs: two thousand providers, four thousand patients.*

> [00:00.0] Here is the smallest provider there could be: two patients.  
> [00:03.7] And here are two thousand of them. Each pair has its own intercept, as always, and all of them share one risk rule.  

**00:11.4 · s1_2** — *The dial for the shared rule, with the truth marked on it: 0.5. A question: what will the fit return?*

> [00:11.4] We built this world, so we know the rule: a coefficient of 0.5.  
> [00:16.5] Four thousand patients is a lot of evidence. What should the fit return?  

**00:21.3 · s1_3** — *The dial's needle swings past the truth to 0.92. Then a pile of four hundred fits from four hundred such worlds, centred on 1.01, with the truth at 0.5 far to its left.*

> [00:21.3] It returns 0.92. Nearly twice the truth.  
> [00:25.3] Draw the world again, four hundred times. The average is 1.01. This is not bad luck, and it is not a bug.  

## S02_Title  (00:35)

**00:35.2 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:35.2] Welcome back to Model in Motion.  
> [00:37.4] Today: too many intercepts.  

## S03_Why · Where the bias comes from  (00:41)

**00:41.6 · s3_1** — *The field of pairs, sorted in two: 1,224 pairs whose two outcomes match, dimmed, and 776 pairs with one readmission, lit.*

> [00:41.6] Look inside the pairs. In 1,224 of these 2,000, both patients had the same outcome.  
> [00:49.4] Episode 10 told us what happens then: the intercept runs to the wall, and the pair says nothing about the rule.  

**00:56.7 · s3_2** — *One mixed pair up close: its two patients on the risk-factor line, one readmitted and one not, and the fitted intercept placing their two chances either side of 50%, adding to one.*

> [00:56.7] In the other pairs, one patient was readmitted and one was not. Here the intercept is free to go wherever fits this pair best, and it settles exactly midway between the two patients.  

**01:08.7 · s3_3** — *Three such pairs, each with its two fitted chances adding to exactly one. Under them: joint fit 0.9229, conditional fit 0.4614, a ratio of exactly two.*

> [01:08.7] That fit is too good. The intercept has been tuned to two patients and nobody else, and it flatters them.  
> [01:15.2] The shared rule inherits a little of that from every pair. For pairs the sum is exact: twice the truth.  

## S04_Sweep · How large must a provider be?  (01:23)

**01:24.5 · s4_1** — *The same four thousand patients regrouped: providers of 2, 5, 10, 25 and 100. A chart of the fitted rule over the true one against provider size: 2.01, 1.26, 1.12, 1.05, 1.01.*

> [01:24.5] Keep the same four thousand patients and regroup them, into providers of 5, of 10, of 25, of 100.  
> [01:32.3] The rule comes out 26% too steep, then 12%, then 5%, then 1%.  

**01:39.3 · s4_2** — *A curve through the points: one plus about 1.2 over the provider's size. A note: more providers of the same size add intercepts, not information for each one.*

> [01:39.3] The error shrinks as each provider grows. It does not shrink as providers are added.  
> [01:44.8] More providers of the same size bring more intercepts, and no more information for each one.  

## S05_NoWarning · No warning  (01:52)

**01:53.4 · s5_1** — *For three provider sizes, forty 95% intervals each, drawn against the truth at 0.5. For pairs every interval misses; for fives most miss; for hundreds nearly all hold it. Standard errors: 0.08, 0.05, 0.04.*

> [01:53.4] And nothing in the output warns you. The standard error stays small, between 0.04 and 0.08.  
> [02:02.1] So the 95% intervals are narrow, and in the wrong place. With providers of 5, they hold the truth about a quarter of the time. With pairs, never.  

## S06_Remedy · A remedy that deletes the intercepts  (02:14)

**02:14.2 · s6_1** — *One provider of five patients, two readmitted. The question changes from how many to which two; the intercept marker fades out. A small tag links this to the Cox series: who, not when.*

> [02:14.2] There is a fit that escapes this. Within each provider, take the number of readmissions as given, and ask only which patients they were.  
> [02:22.9] Asked that way, the provider's intercept cancels. It is the same move the Cox model makes when it asks who, not when.  

**02:31.0 · s6_2** — *The chart of S04 again with a second line, flat at 1.00: the conditional fit at every size. Beside it, an empty column where the intercepts would be.*

> [02:31.0] This conditional fit gets the rule right at every size: within 1% of the truth, even for pairs.  
> [02:37.8] But it has deleted the very numbers we came for. It returns no intercepts, so it cannot profile a provider.  

## S07_Practice · In practice  (02:46)

**02:47.6 · s7_1** — *The provider-size axis with three marks: the software's cutoff at 10; 25 patients, 5% too steep; 100 patients, 1%. A band from 20 to 500 for the series' crowd: 1% too steep.*

> [02:47.6] So we keep the joint fit, and keep an eye on provider size. At 25 patients the rule is about 5% too steep; at 100, about 1%.  
> [02:58.3] The software sets aside providers with 10 patients or fewer before it fits. And in our crowd, with 20 to 500 patients a provider, the rule comes out about 1% too steep.  

**03:11.0 · s7_2** — *A note: a property of the method, not of a program. pprof_py's fit of one world of tens gives the same coefficient to five decimals: 0.58803.*

> [03:11.0] One last thing. This is a property of the method, not of any program. Every joint fit, in any package, has it.  

## S08_Recap · Recap  (03:19)

**03:19.9 · s8_1** — *Three recap cards, each with a small icon.*

> [03:19.9] Let's gather it up.  
> [03:21.4] Each intercept is fitted to its own few patients, and overfits them a little.  
> [03:26.3] The shared rule inherits that, and comes out too steep, by a little more than one over the provider's size.  
> [03:32.9] Conditioning removes the bias, and the intercepts with it.  

**03:36.7 · s8_2** — *Episode 15's funnel with a quarter of its dots outside. The last episode's title.*

> [03:36.7] One question has been waiting since Episode 15. When a quarter of the providers fall outside the funnel, are they all outliers?  
> [03:44.9] Next time, the last episode: wider than chance.  

**03:48.5 · s8_3** — *Series end card with the next episode title.*

> [03:48.5] This has been Model in Motion. Thanks for following the story.  
