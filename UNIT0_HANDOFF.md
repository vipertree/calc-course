# Unit 0 (Trig Review) handoff

**Asked (Adder, 2026-10-03):** "Please work on the Trig Review modules now. They should have the quizzes, packets, and a test
just like the others." Nothing for a trig review existed, so this branch adds it as **Unit 0: Trig Review**, before Unit 1,
built exactly like Units 1-10 (transcript, scene, notes/practice/quiz/test prep per topic, plus `content/unit_0.py`).

Branch: `claude/admiring-feynman-m8ygr9`. Videos not rendered (no manim/kokoro here). **PDFs and web JSON were built**: TeX installs
in this container with `apt-get install -y --no-install-recommends texlive-latex-base texlive-pictures texlive-xetex texlive-latex-extra
texlive-fonts-extra dvisvgm` (run `apt-get update` first; about 10 minutes).

## Registration
- `web/course/syllabus.json`: the module with lessons 0.1-0.8 inserted first (`"n": 0`, `bc: false`). URLs already accept `0.x` and `U0`.
- `anim/kit.py`: `UNIT_NAMES[0] = "Trig Review"` for the title card.

## Topics
Renumbered 2026-10-08 (Adder's critique): a new first lesson, so the old 0.1-0.7 are now 0.2-0.8. Students see T1-T8.

| # | Title | Notes |
|---|---|---|
| 0.1 (T1) | Right-Triangle Trigonometry | **new**: SOH CAH TOA in degrees, reciprocal ratios, finding sides and angles, elevation/depression |
| 0.2 (T2) | Angles and Radian Measure | radians as arc length on a circle of radius 1; arc length and sector area derived from the fraction theta/2pi |
| 0.3 (T3) | The Unit Circle | slowed down: triangle trig on the coordinate plane, the (0.6, 0.8) triangle, then beyond triangles |
| 0.4 (T4) | The Six Trigonometric Functions | triangle material moved to T1; now any point (x, y) and r, reciprocals of any angle |
| 0.5 (T5) | Graphs of Sine, Cosine, and Tangent | new beat: the input x vs the unit circle's x and y |
| 0.6 (T6) | Trigonometric Identities | renumbered only |
| 0.7 (T7) | Solving Trigonometric Equations | renumbered only |
| 0.8 (T8) | Inverse Trigonometric Functions | renumbered only |
| U0 | Trig Review test | 12+4 MCQ, 3 FRQ, two forms; slot 5 is now a T1 right-triangle ratio |

**Videos**: every lesson's video number moved, so all eight need publishing again (0.1-0.5 also changed content).
Published `web/static/video/0_*.mp4` from before the renumbering belong to the old numbers until replaced.

## New shared helpers
- `anim/kit.py`: `pi_axes` (axes with pi tick labels), `TrigCircle` (unit circle with `ray`, `angle_arc`, `drop` reference
  triangle, `coord` labels, `arc`), `right_triangle`, `ferris_wheel` prop, `clipped_plot` (tan/sec/csc branches cut at a
  y limit).
- `anim/kit.py` `example()`: problem statements longer than about 80 characters of prose now wrap onto several lines
  (`wrap_tex`) instead of shrinking to fit one line. This changes the look of long problems in every unit; check on render.
- `calclib/figs.py`: `graph(..., xpi=0.5)` labels x ticks in multiples of pi; `unit_circle(...)` and `triangle(...)` figures.
  Compiled and checked by eye in the Unit 0 notes.

## Judgment calls
- `ced=["Prerequisite: ..."]`: trig review isn't in the CED.
- Adder's rule "reviews of prerequisite facts give the facts outright with no blanks" was written for reviews inside calculus
  lessons. In this unit the facts are the lesson, so formula boxes keep a few blanks for things the student derives
  (2pi in a full turn, s = r theta); reference tables (unit-circle values, identities) are printed in full.

## Fixes outside Unit 0 (found once TeX was installed)
- `calclib/latex.py`: a text `\blank{...}` inside math failed to compile (`calc.sty` measures it in text mode). 52 topic files
  across units 1-10 had one, so their notes/packet PDFs could not build. The print path now converts it to `\mblank`, as
  the web export already did. Verified on 7.8.
- `calclib/latex.py`: MCQs in a PRACTICE list now print (the web already handled them).
- `calclib/web.py`: Table rows may carry print spacing `\\[5pt]`; the web drops it.

## Still to do (merging agent)
- Render every scene, then video-review and notes-review. Compile the PDFs (TikZ figures above).
- Decide whether Unit 0 should be optional/collapsed on the course map (it currently shows first, like any unit; the map still
  opens Unit 1 for newcomers).

## Whole-course verification (2026-10-03, with TeX installed)
- `build.py --docs packet,quiz` compiles for every topic 0.1-10.15, and every unit test U0-U10 compiles.
- `build.py --web` exports all 129 pages (topics + unit tests). Two fixes were needed: `\hline` in web tables (5.9) and
  the TikZ `center` label key (8.6, 8.8, 8.12, U8).
- `manage.py test course`: 49 of 51 pass. The two failures are `Video.*`, which need a rendered `1_1.mp4`/`.vtt`.
  `AnswerKeys` now runs over every page (it was vacuous before, with nothing exported) and caught a complex-valued key in
  7.9, fixed.
