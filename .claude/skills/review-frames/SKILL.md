---
name: review-frames
description: How to make and read review sheets and contact sheets of rendered scenes in this repository - layout, captions, colour code, numbers. Use whenever checking a render, preview or final.
---

# Reviewing frames

**Make them.** `python3 tools/review.py EP OUT.png QUALITY SCENE[:t1,t2] ...` takes one frame near the end of every
narration clip of the scenes named, plus any extra times; tiles are labelled with scene, clip id and time. For a
finished MP4: `python3 tools/contact_sheet.py VIDEO OUT.png t1 t2 ... --cols 3 --w 640`.

**Read every tile** against this checklist:

1. **Text.** Nothing overlaps or touches; labels clear ruler ends, ticks and arrows; nothing is cut at the frame edge;
   small text is still legible at 480p.
2. **Captions.** Nothing that matters sits below y = −3.0, the bottom seventh of the frame. In a burned-in final, the
   caption box covers no content.
3. **Numbers.** Each matches the numbers JSON and what the narration says in that clip.
4. **Colour code.** Clinics keep their hues (Alder orange, Birch sky blue, Cedar grey-blue, Dune pink, Elm green); β and
   what it drives are yellow; observed is solid and expected dashed; green marks the better number, coral a warning.
5. **State.** What the narration says in the clip is on screen; nothing lingers from an earlier beat; filled and hollow
   chips are right.
6. **Focus.** One thing to look at per clip; the chapter tag is present except on title and end cards.

**Report** one row per problem: scene, clip, what is wrong, the smallest fix. Most fixes are spacing or timing.
Re-render only the scenes you changed.

**Limits.** Stills cannot show motion quality or sync with the voice. Say what still needs a watch-through with sound.
