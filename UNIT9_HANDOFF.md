# Unit 9 build: handoff log (BC only)

Branch: `claude/admiring-feynman-m8ygr9`, continuing after Unit 8 (UNIT8_HANDOFF.md). Same rules: built per
.claude/skills/unit-building and lesson-writing; nothing rendered; each topic passes tools/transcripts.py,
py_compile, and `build.py X.Y --no-pdf`. Every topic is `bc_only=True`.

## Status

Unit test: content/unit_9.py done (all of 9.1-9.9; 12 + 4 MCQ, 3 FRQs: calculator plane motion, polar, no-calculator parametric curve).

| Topic | Transcript | Scene | Notes/problems | Commit |
|---|---|---|---|---|
| 9.1 | done | done (ladybug, param_curve in kit) | done (FRQS = []) | see git log |
| 9.2 | done | done | done (FRQS = []) | see git log |
| 9.3 | done | done | done (FRQS = []) | see git log |
| 9.4 | done | done | done (FRQS = []) | see git log |
| 9.5 | done | done | done (FRQS = []) | see git log |
| 9.6 | done | done (drone prop in kit) | done (calculator parametric-motion FRQ) | see git log |
| 9.7 | done | done (polar_curve, lighthouse in kit) | done (FRQS = []) | see git log |
| 9.8 | done | done (polar_region, polar_wedge in kit) | done (FRQS = []) | see git log |
| 9.9 | done | done | done (polar FRQ: area between curves, dr/dθ, slope, dr/dt) | see git log |

## Notes for the merging agent

- CED codes for Unit 9 (CHA-3.G etc.) were written from memory; check them against the CED before release.
- `UnitTest` has no BC flag; the web presumably takes BC-ness from syllabus.json (unit `bc: true`). Check that the U9/U10 tests are hidden from AB students.
- Render every scene and run video-review / notes-review.
