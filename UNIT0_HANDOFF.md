# Unit 0 (Trig Review) handoff

**Asked (Adder, 2026-10-03):** "Please work on the Trig Review modules now. They should have the quizzes, packets, and a test
just like the others." Nothing for a trig review existed, so this branch adds it as **Unit 0: Trig Review**, before Unit 1,
built exactly like Units 1-10 (transcript, scene, notes/practice/quiz/test prep per topic, plus `content/unit_0.py`).

Branch: `claude/admiring-feynman-m8ygr9`. Nothing rendered (no manim/kokoro/TeX in the cloud session).

## Registration
- `web/course/syllabus.json`: Unit 0 with topics 0.1-0.7 inserted first (`"n": 0`, `bc: false`). URLs already accept `0.x` and `U0`.
- `anim/kit.py`: `UNIT_NAMES[0] = "Trig Review"` for the title card.

## Topics
| # | Title | Transcript | Scene | Content | Notes |
|---|---|---|---|---|---|
| 0.1 | Angles and Radian Measure | done | done | done | |
| 0.2 | The Unit Circle | done | done | done | |
| 0.3 | The Six Trigonometric Functions | done | done | done | |
| 0.4 | Graphs of Sine, Cosine, and Tangent | done | done | done | |
| 0.5 | Trigonometric Identities | done | done | done | |
| 0.6 | Solving Trigonometric Equations | done | done | done | |
| 0.7 | Inverse Trigonometric Functions | | | | |
| U0 | Unit 0 test | | | | |

## New shared helpers
- `anim/kit.py`: `pi_axes` (axes with pi tick labels), `TrigCircle` (unit circle with `ray`, `angle_arc`, `drop` reference
  triangle, `coord` labels, `arc`), `right_triangle`, `ferris_wheel` prop, `clipped_plot` (tan/sec/csc branches cut at a
  y limit).
- `anim/kit.py` `example()`: problem statements longer than about 80 characters of prose now wrap onto several lines
  (`wrap_tex`) instead of shrinking to fit one line. This changes the look of long problems in every unit; check on render.
- `calclib/figs.py`: `graph(..., xpi=0.5)` labels x ticks in multiples of pi; `unit_circle(...)` and `triangle(...)` figures.
  **These TikZ figures have not been compiled** (no TeX here): run `python3 build.py 0.1 0.2 ...` on a machine with TeX first.

## Judgment calls
- `ced=["Prerequisite: ..."]`: trig review isn't in the CED.
- Adder's rule "reviews of prerequisite facts give the facts outright with no blanks" was written for reviews inside calculus
  lessons. In this unit the facts are the lesson, so formula boxes keep a few blanks for things the student derives
  (2pi in a full turn, s = r theta); reference tables (unit-circle values, identities) are printed in full.

## Still to do (merging agent)
- Render every scene, then video-review and notes-review. Compile the PDFs (TikZ figures above).
- Decide whether Unit 0 should be optional/collapsed on the course map (it currently shows first, like any unit; the map still
  opens Unit 1 for newcomers).
