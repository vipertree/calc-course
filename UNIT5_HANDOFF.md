# Unit 5 edits: handoff log

Branch: `claude/admiring-feynman-m8ygr9` (cloud session). Based on `main` at 37d23fe
(3.4 inverse trig merge). Work here may stop mid-task at a token limit; this file is the
source of truth for what was asked, what is done, and what is left.

Scope: Adder's notes for unit 5 (content/topic_5_*.py, content/unit_5.py, transcripts/5_*.md,
anim/s5_*.py). Renders/deploys are NOT done on this branch; the merging agent should run
`build.py --web` and `anim/publish.sh` for touched topics and do the notes-review /
video-review passes.

## Requests (verbatim-ish, as Adder gave them)

**Standing (all unit 5 worked examples):** slow down the algebra in worked solutions. Show every step
(e.g. 3c^2 - 1 = 3, then 3c^2 = 4, then c^2 = 4/3, then c = ±2/√3, then check the interval), not a jump to the answer.

**5.1**
1. Opening secant-slide: this curve actually has TWO points where the tangent is parallel to the secant. Show/mention
   that it happens twice here, but only one is guaranteed.
2. When the theorem is introduced, add a plain-words version next to the formula: the instantaneous rate of change at
   some c equals the average rate of change over the interval.
3. Slow down on closed vs. open interval. Tell students the distinction rarely matters: usually a polynomial or
   something continuous well past the interval. When justifying, state both continuity and differentiability, but
   the endpoint conditions rarely come up.
4. Show the algebra in "find c" (see standing note).
5. Add a worked example from a TABLE (classic AP). Point out you have to pick the right pair of values whose average
   rate of change equals the target.

**5.2**
1. Add the usual "little Latin lesson": extremum/extrema, minimum/minima, maximum/maxima. In English we often say
   minimums, maximums, or extreme values, but you'll see the Latinate forms; extrema = any plural of mins and maxes.
2. (standing note) factoring steps in "Find the critical points" and Example 1 broken out.

## Status

| Topic | Request | Status | Commit |
|---|---|---|---|
| 5.1 | 1-5 above | done (transcript, scene, notes); not rendered | see git log |
| 5.2 | 1-2 above | done (transcript, scene, notes); not rendered | see git log |

## Notes for the merging agent

- Nothing here has been rendered (no manim/numpy in this container). Code is py_compile-clean and
  `tools/transcripts.py` passes; content modules import and `calclib.videx.video_examples` parses the new steps.
- 5.1 scene: new beat "Closed and open" (polynomial y = x^3 - x over a shaded [a, b]); "Slide the secant" now slides
  back to the second tangent point c_2 (~3.71); "The theorem" has an in-words line under the box (the box group was
  shifted up 0.6 to make room; Close reuses it). Example 1 has 8 board lines (board scrolls). New Example 4 (table,
  cue highlights the t = 2 and t = 5 columns). Watch for: layout audit on the right-hand column of "Closed and open",
  and the words line width in "The theorem".
- 5.1 runtime went ~5.3 -> ~7.1 min.

- 5.2 scene: new beat "A little Latin" (table of singular/plural, between "Absolute and relative" and the EVT).
  "Find the critical points" and Example 1 now write one factoring step per line.
