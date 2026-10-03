---
name: unit-building
description: Build a new AP Calculus unit (or topic) end to end in this repo: content/topic_X_Y.py notes, practice, quiz, test prep and FRQs; transcripts/X_Y.md; anim/sX_Y.py scenes; content/unit_X.py test. Use when starting a unit or topic that doesn't exist yet. Load lesson-writing (pedagogy and wording) and ap-frq (FRQs) alongside it.
---

# Building a unit

Units 1-5 are the model; copy their shape exactly. The topic list and titles are in `web/course/syllabus.json`
(CED order; `bc: true` topics are BC-only). The site discovers topics from the JSON that `build.py --web`
exports, so a new topic needs no registration beyond its files.

## Order of work, per topic

1. **Read the CED** learning objectives for the topic (cite them in the module docstring and `ced=[...]`, like
   `content/topic_5_1.py`). Read the previous topic's files so notation and running examples carry over.
2. **Transcript first** (`transcripts/X_Y.md`, format in `transcripts/README.md`): an opening hook beat, the silent
   Title beat, 3-5 teaching beats, one lesson worked example solved inside the lesson (`[try it]`), a Close beat,
   then `# Worked examples` with 3-4 examples. Add `<!-- check: ... -->` sympy checks for every number (the checker
   only knows `x`; use plain numbers or `Symbol('y')`). Run `python3 tools/transcripts.py X.Y` until 0 flags.
3. **Scene** (`anim/sX_Y.py`, class `Lesson(TranscriptScene)`, `NUM = "X.Y"`): one `with self.beat(name)` per
   transcript beat, `b.line(i)` to sync each visual with narration line i, `self.title()` after the hook,
   `self.examples_card()` before the examples, `self.example(...)` for every worked example (steps are literal
   strings so `calclib/videx.py` can copy them into the notes; give `text=` when the problem is a mobject and
   `notes_graph=` when the problem needs its graph), `self.finish()` at the end. Every transcript beat must be
   animated. py_compile it. Rendering needs manim + kokoro (not in cloud sessions); leave renders to a machine
   that has them and note it in the handoff.
4. **Notes and problems** (`content/topic_X_Y.py`): `NOTES` (Video, Sections, Formula boxes with `\blank{}`,
   Text, graph figures via `calclib.figs.graph`, `VideoExample('<lesson example title>')`, BigIdea, Check),
   `PRACTICE` (8-14 Items/MCQs), `QUIZ` (5 `Variants` slots of 3), `MCQS` (4 test-prep MCQs), `FRQS` (1 AP-style
   FRQ; follow the ap-frq skill), and `TOPIC = Topic(...)`. Verify every keyed answer with sympy via `same(...)`,
   `close(...)` or asserts in the module, so a wrong key fails at import. `python3 -c "import content.topic_X_Y"`
   and `python3 build.py X.Y --no-pdf` must pass.
5. **Before committing, grep the new files for draft debris**: `grep -nE "if False|or True|\.\.\.|\* 0 \+|\.replace\(" anim/sX_Y.py content/topic_X_Y.py`.
   Half-edited stems ("... more precisely"), placeholder expressions and `.replace()` on step strings (videx needs plain
   literals) have all slipped into drafts before. Board prose lines start with `TEXT:` (never `\text{TEXT:...}`), and
   `Table(latex, spec, header=...)` takes a LaTeX tabular body, not Python lists.
6. **Commit and push per topic**, with a message saying what's in it and that it isn't rendered.

## The unit test

`content/unit_X.py`: `TEST = UnitTest(...)` in AP format (12 MCQ no calculator, 4 MCQ calculator, 3 FRQ), two forms
for every slot, choices placed with `pick(...)`, every key checked with sympy. Copy `content/unit_5.py`'s
structure. Build with `python3 build.py UX --no-pdf`.

## Conventions to keep

- Colors in scenes: FUNC (f), SECANT (average rate), TANGENT (instantaneous), AREA, ACCUM (accumulation
  functions), DERIV (f'). Unit 6 onward: shade area with AREA, accumulation functions in ACCUM.
- kit helpers: `plot_axes`, `table`, `sign_chart` / `staged_chart` + `reveal_sign` / `reveal_words` /
  `mark_point`, `formula_box`, `nudge_arrow`, `callout`, scenery props; Unit 8 added `region`, `slice_rect`,
  `solid_of_revolution` / `solid_about_vertical`, `oblique` + `base_curve` + `oblique_axes` + `base_region` +
  `sections` / `cross_section` / `rect_section` for 3D-looking solids. Figures: `calclib.figs.region` shades regions. Reuse before writing new drawing code;
  add new shared helpers to kit with a docstring.
- Numbers on boards in LaTeX with `\ ` spacing; `TEXT:` prefix for prose steps; `PART:` for multi-part reveals.
- Keep each topic's video around 5-9 minutes; worked examples are where the length goes.

## Handoff

Work can be cut off at a usage limit. Keep a `UNIT<N>_HANDOFF.md` at the repo root: what was asked, per-topic
status, commits, and what the merging agent must still do (render, notes-review, video-review). Update it with
every commit.
