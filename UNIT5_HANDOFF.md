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
3. EVT failures: slow down and show graphically. For the open interval (approaching a value with no function value
   at the endpoint), zoom in and show it gets closer and closer but never reaches it, so no max. Same care for the
   one that shoots off to infinity.
4. Define critical points very clearly: f' = 0 or f' undefined.

**5.3**
1. Slow the "where is x^3 - 3x^2 + 4 increasing" example: pause on "so we're asking when is f' > 0?", take the
   derivative, show the solving, draw the number line, explain the pieces and why those test values, show each sign.
2. More graphs in general: hammer the graphical relationship between f and f'. Point out f' can be negative where f
   is positive.
3. Graph-reading questions: given a graph of f' (lines, semicircles), when is f increasing, when does f have a max.
   Look at f, answer about f' and f; look at f', answer about f. Check if a later section already does this; if not,
   5.3 is where it gets hammered. (Finding: 5.8 does f'-graph reading incl. concavity, with one piecewise-linear FRQ;
   nothing earlier. Decision: 5.3 gets the increasing/decreasing/turning-point readings; 5.8 keeps concavity.)

**5.4**
1. Every extrema problem working out +, -, + gets its own number-line sign chart, shown clearly, every one.

**5.5**
1. Emphasize inputs vs outputs: the max/min IS the function value (output); "when"/"where" is the x where it is
   achieved, e.g. "maximum of 20 when x = 3". Include questions that ask only for the absolute max (value) and others
   that ask where it is achieved.

**5.6**
1. Adder says "bowl" and "hill" (not cup/cap).
2. Vocabulary: in English, concave = opened/caved in, convex = bulging the other way. A graph is a thin line, so from
   one side it's concave and from the other it's convex; that's why we say concave UP and concave DOWN, to be clear
   which side the opening faces.

**5.7**
1. Slow down the algebra for derivatives, second derivatives, and solving for zero. Also: build this into the
   lesson-making skill (done: .claude/skills/lesson-writing/SKILL.md).

## Status

| Topic | Request | Status | Commit |
|---|---|---|---|
| 5.1 | 1-5 above | done (transcript, scene, notes); not rendered | see git log |
| 5.4 | 1 above | done (transcript, scene); not rendered | see git log |
| 5.3 | 1-3 above | done (transcript, scene, notes, practice); not rendered | see git log |
| 5.2 | 1-4 above | done (transcript, scene, notes); not rendered | see git log |

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
- 5.2 EVT split into three beats: "The Extreme Value Theorem" (box, underlines on [a, b] and "continuous"),
  "No endpoint, no maximum" (three nested zoom panels of y = x near the open circle at 1: windows [0,1.25],
  [0.9,1.025], [0.99,1.0025], dot at 0.9/0.99/0.999, box-and-connector insets), "Off to infinity" (1/x, a dot
  climbing the right branch, table x = 0.1/0.01/0.001). Check the inset boxes land on the open circle and the
  connector lines don't cross labels. "Critical points" now ends with a boxed definition at the bottom; the row of
  three mini-graphs moved to the top edge to make room.
- NEW kit helpers (anim/kit.py, appended): staged_chart / reveal_sign / reveal_words. A sign chart passed as an
  example's figure with figure_at, whose signs and words start at opacity 0 and are revealed by cues as each test
  value is written. Used in 5.3 (and planned for 5.4). If the layout audit flags the hidden signs, that is why.
- 5.3 scene: new beats "f and f prime together" (stacked f / f' with a TracedPath drawing f' as the tangent rides f,
  colored by sign) and "Height is not slope" (x = 2: f > 0, f' < 0; x = 4.2: f < 0, f' > 0). New lesson example
  "From the graph of f prime" (segments + semicircle, pieces recolor as read; notes_graph given). Examples 1-3 all
  have staged sign charts and one algebra step per line. New Example 4 "From the graph of f" (positive f, negative
  f'). Runtime ~5 -> ~8.6 min. Notes: new sections "Graphs of f and f'" and "Reading the graph of f'", plus 5 new
  graph practice items (figures t5_3_pq, t5_3_f) and t5_3_fp.
- 5.4: "From a sign chart" and Examples 1-3 all use staged sign charts (kit.mark_point labels max/min/neither over
  each critical point, new helper) and spell out every test-value computation.
