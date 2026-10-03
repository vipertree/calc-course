# Unit 6 build: handoff log

Branch: `claude/admiring-feynman-m8ygr9` (cloud session, after the unit 5 edits in UNIT5_HANDOFF.md).
Adder asked (2026-10-03): fold all unit 1-5 notes into a skill (done: .claude/skills/lesson-writing and
.claude/skills/unit-building), then build the rest of the course one unit at a time until credits run out.

Nothing here is rendered (no manim/kokoro in the cloud container). Each topic is py_compile-clean, passes
`tools/transcripts.py`, imports, and `build.py X.Y --no-pdf` runs. The merging agent should render
(`anim/publish.sh X.Y`), run `build.py --web`, and do the notes-review / video-review passes.

Topic list: web/course/syllabus.json (6.11-6.13 are BC-only).

## Status

| Topic | Transcript | Scene | Notes/problems | Commit |
|---|---|---|---|---|
| 6.10 | done | done (long-division layout drawn by hand) | done (FRQS = []) | see git log |
| 6.9 | done | done (example_ref keeps the u/du recipe in the corner) | done (FRQS = []) | see git log |
| 6.8 | done | done | done (FRQS = []) | see git log |
| 6.7 | done | done | done | see git log |
| 6.6 | done | done | done (FRQS = []) | see git log |
| 6.5 | done | done | done | see git log |
| 6.4 | done | done | done | see git log |
| 6.3 | done | done | done (FRQS = [], MCQ-only topic on AP) | see git log |
| 6.2 | done | done (riemann_boxes helper in kit) | done | see git log |
| 6.1 | done | done (water_tank helper in kit) | done | see git log |

## Notes for the merging agent

- Always run `python3 build.py X.Y --no-pdf` (not just import): sympy key checks are collected and reported at the end of the build.
- sympy leaves exp_polar in semicircle integrals; topic_6_5.py snaps values with nsimplify(N(e), [pi]) (`exact`). Reuse that pattern.
- GRADER CHANGE (web/course/grading.py, with a test in course/tests.py Grading): an expr key containing the symbol C
  (an antiderivative F + C) accepts any constant offset but requires the student to write + C; compares derivatives.
  Also fixed parsing of "5ln|x|" (it used to become a product of letters). Grading/AnswerKeys tests pass; the other
  course tests error the same way with and without the change (no exported site content in the cloud container).
