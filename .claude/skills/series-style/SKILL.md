---
name: series-style
description: The Model in Motion identity - palette, type, motifs, layout, episode shape, narration voice - and the vocabulary in mim/. Use when writing or changing scene code or narration.
---

# Series style

Take every colour, font and motif from `mim/`; never hard-code them in an episode.

**Palette** (`mim/common.py`): background `INK` #0E1621, panels `INK_2` #16212F; text `PAPER` #F3EEE4, `MUTED` #8C9AAB,
`FAINT` #33445A. Clinics: `ALDER` #E69F00 orange and `BIRCH` #56B4E9 sky blue (the pair that swap places), `CEDAR`
#AEB9C6, `DUNE` #CC79A7, `ELM` #3CC59A. `ACCENT` #F0E442 yellow: attention, β and everything β drives. `GOOD` #3CC59A,
`ALERT` #E8705A. The palette is colour-blind safe (Okabe–Ito hues).

**Type.** Inter Display for titles and big numbers, Inter for labels, Lora Italic for asides and axis names, LaTeX
(`MathTex`) for mathematics. The wordmark is "Model *in* Motion", with "in" in Lora Italic and yellow.

**Motifs, and where they come from.** Chip: one patient, filled if the event happened, a pale ring if higher-risk
(Episode 1, `common.py`); trays, big trays and balance beams (Episode 1); rulers, the risk chip (a shaded slice is the
patient's probability) and the step arrow (Episode 2, `kit.py`); the dashed expected bar on a scale of patients and the
O − E balance (Episode 3); the log-odds line panel, the probability curve, the β dial and the γ sliders (`lines.py`);
text styles, marks, the control strip, title and end cards (`boards.py`); the fitting machine (`meters.py`); piles of
counts (`piles.py`); the funnel (`funnel.py`).

**Layout.** The frame is about 14.2 × 8 units. The chapter tag sits top-left. Keep content above y = −3.0 for captions.

**Episode shape.** Cold open (a question, or a wrong method shown first) → title card → four to six tagged chapters →
recap of three cards with icons → teaser of the next episode → end card. A formula appears only after its picture.

**Narration.** Warm and conversational ("let's"); one idea per clip; question, then picture, then name. Kokoro voice
`af_heart` at speed 0.92 with 0.32 s between sentences, about 150–160 words per minute.
