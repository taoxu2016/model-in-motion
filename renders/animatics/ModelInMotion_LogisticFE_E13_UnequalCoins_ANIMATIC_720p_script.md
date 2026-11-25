# Model in Motion · The Logistic Fixed-Effect Model · Episode 13: Unequal Coins

*is this count surprising for a reference clinic?*

Narration script with timestamps. 689 words, running time 05:01. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *Alder's 13 observed beside the 8.02 expected at the reference. A question: a real difference, or luck?*

> [00:00.0] Alder had 13 readmissions. The reference clinic, given the same patients, expects 8.  
> [00:06.1] Is that a real difference? Or could a clinic exactly like the reference have had 13, just by luck?  

**00:12.7 · s1_2** — *Dune's 12 patients as chips: six lower-risk, six higher-risk, 7 of them filled.*

> [00:12.7] To answer, we need to see what luck looks like.  
> [00:15.6] We'll start with Dune, because Dune has only 12 patients, and we can watch every one of them.  

**00:21.7 · s1_3** — *Dune's figures beside the chips: 7 observed, 4.8 expected, 58% readmitted, the highest raw rate in the cast.*

> [00:21.7] Dune had 7 readmissions against 4.8 expected: the highest raw rate in the cast. So make a guess. Is Dune unusual?  

## S02_Title  (00:32)

**00:32.5 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:32.5] Welcome back to Model in Motion.  
> [00:34.7] Today: unequal coins.  

## S03_Coins · Twelve coins  (00:38)

**00:38.9 · s3_1** — *Dune's twelve patients become twelve coins: risk chips whose slice is the reference chance. Six show 18%, six show 62%.*

> [00:38.9] Suppose Dune were exactly like the reference. Then each patient is a coin.  
> [00:43.7] For the six lower-risk patients, it comes up readmitted 18% of the time. For the six higher-risk patients, 62%.  

**00:52.6 · s3_2** — *Three rounds of flips, each a row of twelve marks under the coins, filled where the coin came up readmitted. The counts: 3, 5, 3.*

> [00:52.6] Flip all twelve and count. Three readmissions.  
> [00:55.8] Flip again: five. And again: three.  

**00:58.8 · s3_3** — *A histogram of the counts grows below: after 20 rounds, 200, then 2,000. A dashed line marks 4.8.*

> [00:58.8] Do it two thousand times, and the counts pile up around 4.8.  
> [01:03.3] That pile is what luck looks like, for a clinic like the reference with Dune's patients.  

## S04_Exact · No need to flip  (01:10)

**01:10.0 · s4_1** — *An empty histogram with one full bar at zero: before any coin is added, the count is certainly zero.*

> [01:10.0] We don't actually have to flip anything. The pile can be worked out exactly, one coin at a time.  

**01:16.2 · s4_2** — *The first coin splits the bar: 82% stays at zero, 18% moves to one. Then the other eleven coins, one at a time; the bars spread and settle.*

> [01:16.2] Each new coin splits every bar in two. One part stays where it is: no readmission. The other moves one step to the right.  

**01:26.6 · s4_3** — *The finished pile, enlarged, with four labels: 26% at 5, 19% at 6, 9% at 7, and 4% at 8 or more.*

> [01:26.6] After twelve coins, the chance of exactly 5 is 26%. Of 6, 19%. Of 7, 9%. And of 8 or more, 4%.  

## S05_Tail · How surprising is seven?  (01:39)

**01:40.4 · s5_1** — *The pile with a marker at 7. The bars at 7 and beyond are shaded: 13%.*

> [01:40.4] Dune's count was 7. For a clinic just like the reference, the chance of 7 or more is 13%.  

**01:47.4 · s5_2** — *The bar at 7 is cut in half. Half of it, plus the bars beyond: 0.046 + 0.036 = 0.082. Then × 2 = 0.165.*

> [01:47.4] Two refinements. Counts move in whole steps, so we take only half of the bar at 7 itself. That brings it to 8%.  
> [01:55.5] And a clinic can surprise us in either direction, so we double it: 16%.  

**02:00.8 · s5_3** — *A verdict: p = 0.165, about 1 in 6. Not flagged.*

> [02:00.8] That is the p-value. About one time in six, luck alone does this. Dune is not flagged.  

## S06_Alder · Alder's thirty coins  (02:08)

**02:08.5 · s6_1** — *Alder's thirty coins in a row, 24 at 18% and 6 at 62%, above their exact pile. A marker at 13; the tail from 13 is shaded: 2.5%. The p-value: 0.035.*

> [02:08.5] Now Alder. Thirty coins: 24 at 18%, and 6 at 62%. The pile centres on 8.  
> [02:16.6] Alder's 13 sits far out in the tail. The chance of 13 or more is two and a half percent, and the p-value is 3.5%.  

**02:26.2 · s6_2** — *A line at 5% and a flag beside Alder's p-value.*

> [02:26.2] That is below the usual 5% line. Alder is flagged: more readmissions than luck comfortably explains.  

**02:33.8 · s6_3** — *Dune and Alder side by side. Dune: 12 patients, 58% readmitted, p = 16%, not flagged. Alder: 30 patients, 43% readmitted, p = 3.5%, flagged.*

> [02:33.8] So the clinic with the highest raw rate is not flagged, and Alder is. Twelve patients leave a lot of room for luck. Thirty leave less.  

**02:42.4 · s6_4** — *All five p-values in a row: 0.035, 0.45, 0.99, 0.16 and 0.11, with one flag.*

> [02:42.4] For the others: Birch, 45%. Cedar, 99%. And Elm, 11%, which is simply its whole bar at zero.  

## S07_Unequal · Why unequal matters  (02:53)

**02:53.2 · s7_1** — *Alder's pile as filled bars, and over it, as an outline, the pile for thirty identical coins of 27%: wider. Two p-values: 3.5% and 5.2%.*

> [02:53.2] Why insist that the coins are unequal? Swap Alder's thirty for thirty identical coins with the same average.  
> [03:00.9] The pile gets wider. The p-value rises from 3.5% to 5.2%, and Alder slips under the bar.  

**03:10.0 · s7_2** — *Two variances: 4.94 for the mixed coins, 5.88 for identical ones.*

> [03:10.0] Mixed coins vary less than identical ones. Use the right pile, and the test is sharper.  

## S08_Inside · Turn the test inside out  (03:17)

**03:17.6 · s8_1** — *Alder's pile with its marker at 13 and, under it, a ruler for gamma with a slider at the reference, −1.52.*

> [03:17.6] So far we built the pile at the reference. But we can build it at any gamma, and ask where Alder's 13 stops being surprising.  

**03:26.0 · s8_2** — *The slider moves up. The pile slides right under the fixed marker, and a live p-value changes. Two positions are marked where it reads 5%: −1.46 and +0.13. The reference sits just outside.*

> [03:26.0] Slide the gamma up, and the pile slides right. Between minus 1.46 and plus 0.13, thirteen is unremarkable.  
> [03:35.6] That is Alder's exact 95% interval. The reference, at minus 1.52, lies just outside it: the same verdict as the flag.  

**03:46.3 · s8_3** — *Three intervals on a ratio axis with its line at 1: Alder 1.04 to 2.26, Dune 0.82 to 2.04, Elm 0 to 1.33.*

> [03:46.3] Carried through the rising curve from Episode 11, Alder's ratio lies between 1.04 and 2.26. Dune's, between 0.82 and 2.04, which includes 1.  

## S09_Trust · What the p-value promises  (04:02)

**04:02.6 · s9_1** — *Fifty simulated crowds in which every provider truly equals the reference: 10,000 tests, 4.8% flagged, against a nominal 5%.*

> [04:02.6] Does the test keep its promise? We built fifty crowds in which every provider truly equals the reference, and tested all ten thousand.  
> [04:11.4] It flagged 4.8%, against the 5% it promises.  

**04:16.2 · s9_2** — *Two caution cards: the dial and the reference are treated as known; a p-value is not the chance that the clinic is ordinary.*

> [04:16.2] Two cautions. The test treats the dial and the reference as known.  
> [04:20.6] And a p-value is not the chance that the clinic is ordinary. It is the chance of a count like this, if it were.  

## S10_Recap · Recap  (04:29)

**04:29.2 · s10_1** — *Three recap cards, each with a small icon.*

> [04:29.2] Let's gather it up.  
> [04:30.7] If a clinic were like the reference, each patient would be a coin with a chance of their own.  
> [04:35.8] The count's whole distribution can be worked out exactly, and the tail beyond what was observed gives the p-value.  
> [04:42.9] Turned inside out, the same test gives an interval.  

**04:46.3 · s10_2** — *The exact pile beside three quick sketches; the next episode's title.*

> [04:46.3] Exact is satisfying, but it takes work. Are there quicker ways to nearly the same answer?  
> [04:52.0] Next time: three shortcuts.  

**04:54.4 · s10_3** — *Series end card with the next episode title.*

> [04:54.4] This has been Model in Motion. Thanks for following the story.  
