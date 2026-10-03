---
name: lesson-writing
description: Write or revise an AP Calculus lesson (transcripts/X_Y.md, anim/sX_Y.py, content/topic_X_Y.py) the way Adder teaches it. Use before adding or editing any lesson beat, worked example, or notes section, so worked solutions are slow, every sign analysis has a number line, and theorems come with plain words and pictures.
---

# Lesson writing

Adder's standing rules for how lessons explain things. They come from Adder's review notes (unit 5, October 2026).
Narration style rules (no em dashes, no signposting, etc.) live in `transcripts/README.md` and the copy-review
skill; this skill is about *what* gets explained and how slowly.

## Worked solutions: one step per line

Never jump from an equation to its solutions. Each algebra move is its own board line and its own narration line:

1. Restate the question in derivative language first, and pause on it: "Increasing means f prime is positive. So
   the real question is: when is f prime of x greater than zero?"
2. Take the derivative (first, and second if needed) as its own line. Simplify as its own line.
3. Factor one move at a time: pull out the common factor, then factor what's left (e.g. a difference of squares).
4. Set each factor equal to zero, then solve each. Say both.
5. Solve trig equations visibly: 1 + 2cos x = 0, then cos x = -1/2, then the angles in the interval.
6. Square roots: keep the plus-or-minus, then check each root against the interval or domain out loud.
7. Plug test values in with the arithmetic shown: "f prime of negative one: three plus six, nine. Positive."

On the board this means many short lines (`at=[1, 2, 2, 3, ...]` may repeat an index); the Board scrolls.

## Every sign analysis gets a number line

Any increasing/decreasing, first-derivative-test, concavity or second-derivative sign problem shows a sign chart,
every time, not just the first example. Use the kit helpers so it fills in as the work is done:

```python
ch = staged_chart([0, 2], ["+", "-", "+"], words=["inc", "dec", "inc"], width=7)
self.example(..., figure=ch, figure_at=<line where the critical points are found>,
             cues={k: reveal_sign(ch, 0), ..., j: reveal_words(ch), m: mark_point(ch, 0, "max")})
```

Narrate why the pieces exist ("the critical points cut the line into three pieces; f prime can only change sign at
a critical point, so one test value per piece is enough") and why the test values are chosen (easy numbers).

## Theorems

- State the formula AND a plain-words version on screen ("the instantaneous rate of change at some c equals the
  average rate of change over the interval").
- Slow down on hypotheses. Say which conditions matter in practice and which rarely come up (closed vs. open
  endpoints in MVT), but still state all of them in a justification.
- When a theorem guarantees "at least one", show a case with more than one and say only one is guaranteed.
- Show failures graphically and slowly: zoom in on an open endpoint the function never reaches (nested zoom panels),
  climb an asymptote with a table of values.
- Where two methods exist (first vs. second derivative test), present the choice: when each is the better tool.

## Graphs, always

- Pair algebra with pictures. Stack f over f' on shared x-axes; color by sign.
- Hammer the f / f' relationship both ways: given f, answer about f'; given a graph of f', answer about f.
  Include AP-style f' graphs built from line segments and semicircles.
- Height is not slope: point out f > 0 where f' < 0, and the reverse.
- On a graph of f', "f' is decreasing" does not mean "f is decreasing". Say so.

## Words and meaning

- Vocabulary gets a short aside when the word is odd: Latin plurals (maximum/maxima, minimum/minima,
  extremum/extrema; English also says maximums, minimums, extreme values).
- Concavity: say "bowl" (concave up) and "hill" (concave down). Explain why "concave up/down": a curve is a thin
  line, concave from one side and convex from the other, so we name which way the opening faces.
- Inputs vs. outputs: the maximum IS the output value; "where" or "when" is the x that produces it ("a maximum of 20
  when x = 3"). Problems should ask for each separately.

## AP habits worth a dedicated example

- MVT from a table: the student must pick the pair of values whose average rate equals the target.
- Justifications name the theorem/test and the sign change of f' (or f''), not the graph of f.

## After writing

Run `python3 tools/transcripts.py X.Y`, py_compile the scene, import the content module, and check
`calclib.videx.video_examples("X.Y")` parses. Then render and run the video-review and notes-review skills.
