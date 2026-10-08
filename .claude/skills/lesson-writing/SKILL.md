---
name: lesson-writing
description: Write or revise an AP Calculus lesson (transcripts/X_Y.md, anim/sX_Y.py, content/topic_X_Y.py) the way Adder teaches it. Use before adding or editing any lesson beat, worked example, or notes section, so worked solutions are slow, every sign analysis has a number line, theorems come with plain words and pictures, and the wording follows Adder's notes from units 1-5. For building a whole new unit, also load unit-building.
---

# Lesson writing

Adder's standing rules for how lessons explain things, collected from Adder's review notes on units 1-5 (October 2026;
the commit messages titled "Adder's notes" have the details).
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

## Wording rules (units 1-4)

- "Yields" for what substitution produces ("substituting yields 0/0"). Never write "= 0/0": say the limits of the
  numerator and denominator are both 0 (or both infinite), so L'Hospital's Rule applies.
- No implication arrows on boards or in solutions: write ", so". No level arrows on curved paths; an arrow always
  points along its flight path.
- "Does not exist" (DNE) for nonexistent limits; such blanks read "limit = ___".
- Discontinuities: removable (a hole) vs nonremovable (a jump or a vertical asymptote). Never "infinite
  discontinuity".
- Never "blows up". Say the value (or slope) goes off to infinity, and pause to ask what would cause that.
- Methods are a toolkit, not a decision tree (limits: substitution, rewrite and cancel, special identities, split
  into sides, L'Hospital later).
- "The outermost function or operation" for the chain rule's outside; u and v are functions of x.
- Money rates as $ per unit (d$/dt). Velocity vs speed: speed drops the direction.
- Linearization is just the tangent line evaluated near the point: no new formula to memorize.
- When a new form of something appears (a line), connect it to what students know (slope-intercept, standard,
  point-slope from Algebra 1) and say that it recurs all course.
- Interpreting a derivative in context is a big part of the AP exam: units, when, what, which way, how fast.

## Structure rules (units 1-4)

- Recaps and Close beats state the rule to remember, not the pictures used to explain it.
- Definitions stated plainly first (inverse: f(a) = b means g(b) = a), then cues or tests that use them, and each
  example names the cue it uses.
- Keep the rule being practiced on screen during worked examples: `example(..., ref=...)` or `example_ref`.
- Chain rule examples: underbrace the inside u, write u = ... and u' = ..., then f'(u) u'.
- Implicit differentiation examples start with d/dx(left side) = d/dx(right side); "every time we take the derivative
  of y (or something in y) with respect to x, multiply by dy/dx".
- Slow down the first odd step (the first d/dx(y^2); deriving Q = f/g by multiplying both sides by g, one step at a
  time; the x*x counterexample to a wrong product rule).
- A first-of-its-kind problem is follow-along (`follow=True`: no "Pause and try it"); later ones get [try it].
- A warning's picture arrives with the warning (`figure_at=`).
- Proofs that aren't on the exam: say so and reassure ("memorize the rules"). Reviews of prerequisite facts (trig
  values, identities) give the facts outright with no blanks, and name identities (the Pythagorean identity).
  Formula boxes for a reference rule (quotient rule) have no blanks in the rule itself.
- Summary charts with memory tips where students memorize a family (inverse trig derivatives: order, signs on the
  co-functions, what's under the root).
- Patterns worth naming: polynomials' derivatives run out to 0; sine's derivatives cycle every four.
- 2D formulas are known; 3D formulas (box, cylinder volume and surface area) are stated in the problem, as on the AP
  exam. No FRQ titles anywhere (just "Question n").
- Context examples: units examples (miles per hour, liters per minute, dollars per shirt).

## Pictures (units 1-4)

- Every dx, dw, dl in a picture gets its own little labeled double arrow (`nudge_arrow`).
- Zooms are continuous, with tick labels that fade by on-screen spacing so labels never overlap and the curve never
  morphs. Graphs being compared share one scale (slope 1 is 45 degrees).
- Real-life objects should be pretty: painted sprites (anim/assets, generated on Scenario, credited in CREDITS.md)
  where possible, else the vector props in kit (river_band, fence_path, sheep, the cardboard palette). Nothing cut
  off at the frame edge.
- Pacing is unhurried: explain the why, give a beat after each key idea; think time is 5 s.
- Sign charts: bold tick, dot and dashed divider at each zero so it's clear which piece each sign belongs to.

## After writing

Run `python3 tools/transcripts.py X.Y`, py_compile the scene, import the content module, and check
`calclib.videx.video_examples("X.Y")` parses. Then render and run the video-review and notes-review skills.
