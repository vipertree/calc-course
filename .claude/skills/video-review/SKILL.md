---
name: video-review
description: Review rendered AP Calculus lesson videos (anim/) before calling them done. Use after any publish.sh render, and whenever Adder reports a visual problem in a video (overlaps, clutter, leftovers, pacing).
---

# Video review

Every lesson video is rendered by `anim/publish.sh <topic>` (480p drafts for now). A render is not finished
until it has been reviewed this way. Adder catches these problems by eye; catch them first.

## 1. Run the review tool

```bash
cd /workspace/repos/calc-course
~/opt/mamba/envs/calc/bin/python tools/video_review.py 1.1 1.2      # or: all
```

It writes `/tmp/video_review/sheet_<slug>.png` (24 frames) and `issue_<slug>_NN.png` (a still at every moment
the render's built-in layout audit flagged), and prints each issue: time, beat, overlap or off-frame, and
what collided. The audit lives in `anim/kit.py` (`TranscriptScene._audit`) and runs on every render.

## 2. Look, don't just count

Read every contact sheet and every issue still with the Read tool. Check:

- **Overlaps**: text on text, text on a picture or a graph label. Fix the layout in the scene; never accept
  an overlap because "it's only for a second".
- **Leftovers**: props from an earlier scene still on screen (this happened with Zeno's arrows). `self.clear()`
  fades every mobject; anything added with `self.add` outside a beat must be cleared.
- **Off-frame**: anything near the edges or under the caption band at the bottom.
- **Legibility at 480p**: labels under ~28 pt and thin sprites disappear. Enlarge insets.
- **Clutter**: one idea per screen. If a scene has more than about four separate things, split it.
- **Worked examples**: the problem must be complete on screen before the solving starts, with the
  "Pause and try it" cue and the think pause; multi-part problems reveal one part at a time (`PART:` steps
  with `[try it]` in the transcript); a real break between examples. The algebra goes one step per line and
  every sign analysis has its number line (see the lesson-writing skill).
- **On-screen text matches the narration** word for word for quotes and definitions.
- **Notation**: limit notation on every line of a limit computation; piecewise functions as `cases`.

## 3. Fix, re-render, re-review

Fix in `anim/s<slug>.py` (and `transcripts/<slug>.md` if the words change), then
`cd anim && ./publish.sh <topic>` and repeat from step 1. Long batches: render 2 to 3 at a time
(`--frame_rate 30 -ql` per topic is about 10 to 15 minutes each on this machine).

Report to Adder what was checked and what was fixed, with any remaining known issues named plainly.
