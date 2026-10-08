# Unit 10 build: handoff log (BC only)

Branch: `claude/admiring-feynman-m8ygr9`, continuing after Unit 9 (UNIT9_HANDOFF.md). Same rules: built per
.claude/skills/unit-building and lesson-writing; nothing rendered; each topic passes tools/transcripts.py,
py_compile, and `build.py X.Y --no-pdf`. Every topic is `bc_only=True`.

## Status

Unit test: content/unit_10.py done (all of 10.1-10.15; 12 + 4 MCQ, 3 FRQs: Taylor polynomial with Lagrange bound, Maclaurin series, convergence and interval).

| Topic | Transcript | Scene | Notes/problems | Commit |
|---|---|---|---|---|
| 10.1 | done | done | done (FRQS = []) | see git log |
| 10.2 | done | done | done (FRQS = []) | see git log |
| 10.3 | done | done | done (FRQS = []) | see git log |
| 10.4 | done | done | done (FRQS = []) | see git log |
| 10.5 | done | done | done (FRQS = []) | see git log |
| 10.6 | done | done | done (FRQS = []) | see git log |
| 10.7 | done | done | done (FRQS = []) | see git log |
| 10.8 | done | done | done (FRQS = []) | see git log |
| 10.9 | done | done | done (FRQS = []) | see git log |
| 10.10 | done | done | done (FRQS = []) | see git log |
| 10.11 | done | done | done (FRQS = []) | see git log |
| 10.12 | done | done | done (Taylor polynomial FRQ with Lagrange bound) | see git log |
| 10.13 | done | done | done (FRQS = []) | see git log |
| 10.14 | done | done | done (Maclaurin series FRQ: sin x / x, interval, integral, AST bound) | see git log |
| 10.15 | done | done | done (FRQS = []) | see git log |

## Notes for the merging agent

- CED codes for Unit 10 (LIM-7.x, LIM-8.x) were written from memory; check them against the CED before release.
- `UnitTest` has no BC flag; the web presumably takes BC-ness from syllabus.json (unit `bc: true`). Check that the U9/U10 tests are hidden from AB students.
- Render every scene and run video-review / notes-review.

## Whole-branch verification (end of Unit 10)

- `build.py X.Y --no-pdf` passes for every topic 5.1-10.15 and for U5-U10.
- `tools/transcripts.py`: 111 transcripts, 0 flags. Every scene in anim/ compiles.
- No MCQ in any topic or unit test has duplicate choices.
- `manage.py test course.tests.Grading course.tests.AnswerKeys` passes; the other web suites error identically with and
  without this branch's changes (they need exported content, which this container doesn't have).
