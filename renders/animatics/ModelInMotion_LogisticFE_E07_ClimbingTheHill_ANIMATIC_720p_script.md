# Model in Motion · The Logistic Fixed-Effect Model · Episode 7: Climbing the Hill

*how a computer finds the top*

Narration script with timestamps. 660 words, running time 04:23. Voice: kokoro-onnx v1.0, `af_heart`, speed 0.92.

## S01_ColdOpen  (00:00)

**00:00.0 · s1_1** — *Episode 6's hill, its top marked. A climber's dot waits at the foot with a question mark.*

> [00:00.0] Last time we found the top of the hill: the one setting where every meter that can level is level.  
> [00:05.8] But we found it by being told where it was.  

**00:08.6 · s1_2** — *The balance equation for one clinic, with the S-curve inside it. A label: no formula solves this.*

> [00:08.6] A computer has no such luck. It cannot solve for the top with algebra, because every expected count passes through the S-curve.  
> [00:17.0] All it can do, from wherever it stands, is feel the ground: which way is up, and how the slope is changing.  

**00:23.8 · s1_3** — *Two small marks at the climber's feet: a slope arrow and a curvature arc.*

> [00:23.8] So how do you climb a hill you can only feel one spot at a time?  

## S02_Title  (00:29)

**00:29.5 · s2_1** — *Series logo and wordmark; arc and episode title.*

> [00:29.5] Welcome back to Model in Motion.  
> [00:31.7] Today: climbing the hill.  

## S03_OneStep · One slider, one step  (00:35)

**00:35.8 · s3_1** — *Dune's slider alone, standing at −1.52. The dial is held at 2.02.*

> [00:35.8] Start small, with one slider. Hold the dial at its fitted place, 2.02, and stand Dune's slider in the wrong spot: on Cedar's level, minus 1.52.  

**00:47.9 · s3_2** — *Dune's own hill, drawn faintly: its height for every slider position. A dot marks where we stand.*

> [00:47.9] Here is Dune's own hill: its height for every position of its slider.  
> [00:52.3] From where we stand, we can't see it. We know just two things: the slope under our feet, and how fast that slope is changing.  

**01:00.3 · s3_3** — *A parabola through the dot, matching the hill there. Its top is marked: 0.96 to the right, at −0.56. The dot jumps to it.*

> [01:00.3] That is enough to draw a parabola that matches the hill right here.  
> [01:04.3] So jump to the top of the parabola: 0.96 to the right, to minus 0.56.  

**01:11.6 · s3_4** — *A second, much smaller parabola: 0.017 to the left. The dot settles at −0.58, the top of Dune's hill.*

> [01:11.6] Do it again from the new spot. The second jump is tiny: 0.017 back to the left.  
> [01:18.6] And we are there: minus 0.58. Two steps.  

## S04_Tilt · Tilt over wobble  (01:24)

**01:24.4 · s4_1** — *Dune's meter, large: observed 7, expected 4.8, a gap of 2.2.*

> [01:24.4] Where did 0.96 come from? Read it off the meter.  
> [01:28.2] The tilt, we know: observed 7, expected 4.8, a gap of 2.2.  

**01:34.1 · s4_2** — *A hump: how much each patient adds to the wobble, against their probability. Marks at 18% and 62%, Dune's two groups; the sum, 2.29.*

> [01:34.1] The second number is how readily the expected count moves when the slider does. Call it the wobble.  
> [01:40.0] A patient near 50% adds the most to it. A patient near 0 or near 100% hardly adds at all.  
> [01:47.8] For Dune's twelve patients, it comes to 2.29.  

**01:51.9 · s4_3** — *The step as a fraction: tilt over wobble, 2.2 over 2.29, equals 0.96.*

> [01:51.9] So the step is tilt over wobble: 2.2 divided by 2.29.  
> [01:57.1] A gap of 2.2 to close, at 2.29 per unit of slider: move 0.96.  

**02:04.3 · s4_4** — *Caption: which way, and how far.*

> [02:04.3] That division is what makes this more than walking uphill. It does not just say which way. It says how far.  

## S05_Turns · Taking turns  (02:12)

**02:13.8 · s5_1** — *The whole machine at the plain guess. All five sliders step at once.*

> [02:13.8] Now the whole machine, from the plain guess. Every clinic can take its step at the same moment, because each step uses only that clinic's own patients.  

**02:23.3 · s5_2** — *The dial steps; the clinic meters tilt again. Sliders, dial, sliders: a round counter ticks.*

> [02:23.3] Then the dial takes one step, with the sliders frozen.  
> [02:26.8] But that unsettles every clinic, so the sliders step again. Then the dial. Then the sliders.  

**02:32.8 · s5_3** — *The round counter reaches 8 with the dial at 1.91; then runs on to 54, where the meters are level.*

> [02:32.8] Watch the dial. After eight rounds it has only reached 1.91, on its way to 2.02.  
> [02:40.2] Each round covers a fraction of what is left. Getting there takes 54 rounds.  

**02:45.7 · s5_4** — *Elm's slider is picked out: −2.06, −3.19, −4.23, −5.24, −6.25.*

> [02:45.7] And Elm steps down by about one unit every round, without end.  

## S06_Stairs · Why it zig-zags  (02:51)

**02:51.6 · s6_1** — *The hill from above: the dial left to right, Birch's slider up and down, contour lines around the top. The path appears as a staircase.*

> [02:51.6] Here is why it is slow. This is the hill seen from above: the dial runs left to right, Birch's slider up and down.  
> [02:59.3] The path is a staircase: up or down for the sliders, sideways for the dial.  

**03:04.5 · s6_2** — *The ridge is drawn as a dashed diagonal through the top.*

> [03:04.5] And the ridge it is trying to follow runs diagonally. Turn the dial up, and every expected count rises, so every slider has to come down.  
> [03:14.0] A staircase is a slow way along a diagonal.  

**03:17.5 · s6_3** — *Three rows beside the map: zero at a lower-risk patient, 54 rounds; zero five units away, 3,125 rounds.*

> [03:17.5] How slow depends on something that should not matter: where we put zero.  
> [03:21.7] Last episode, moving zero changed every gamma and no gap. It changes the climb too.  
> [03:27.8] Record the risk factor five units higher, and the same alternation needs 3,125 rounds.  

**03:35.6 · s6_4** — *The third row: zero in the middle of the patients, 21 rounds, with the package's name.*

> [03:35.6] Put zero in the middle of the patients instead, and the ridge straightens: 21 rounds. That is what pprof_py does before it starts.  

## S07_Recap · Recap  (03:46)

**03:46.5 · s7_1** — *Three recap cards, each with a small icon.*

> [03:46.5] Let's gather it up.  
> [03:48.0] A step is tilt over wobble. It says which way, and how far.  
> [03:52.1] The sliders can all step at once. The dial steps in turn.  
> [03:56.1] And taking turns climbs a diagonal ridge by staircase.  

**04:00.3 · s7_2** — *A line under the cards: every route climbs toward the same top.*

> [04:00.3] Every route here climbs toward the same top. They differ in how long they take.  

**04:05.3 · s7_3** — *The map again, with one straight arrow along the ridge to the top; the next episode's title.*

> [04:05.3] So here is the obvious question. Could the sliders and the dial step together, straight along the ridge?  
> [04:11.8] They can, and then it takes five steps. Next time: the arrow matrix.  

**04:16.8 · s7_4** — *Series end card with the next episode title.*

> [04:16.8] This has been Model in Motion. Thanks for following the story.  
