# Unit 7 build: handoff log

Branch: `claude/admiring-feynman-m8ygr9`, continuing after Unit 6 (UNIT6_HANDOFF.md). Same rules: built per
.claude/skills/unit-building and lesson-writing; nothing rendered; each topic passes tools/transcripts.py,
py_compile, and `build.py X.Y --no-pdf`.

## Status

| Topic | Transcript | Scene | Notes/problems | Commit |
|---|---|---|---|---|
| 7.9 (BC) | done | done | done (bc_only, FRQS = []; logistic) | see git log |
| 7.8 | done | done | done (FRQS = []) | see git log |
| 7.7 | done | done | done (full AP DE FRQ: tangent line, over/under, particular solution) | see git log |
| 7.6 | done | done | done (FRQS = []; the full DE FRQ is in 7.7) | see git log |
| 7.5 (BC) | done | done | done (bc_only, FRQS = []) | see git log |
| 7.4 | done | done | done (slope-field FRQ) | see git log |
| 7.3 | done | done (slope_field in kit) | done (calclib.figs.slope_field for notes figures; FRQS = []) | see git log |
| 7.2 | done | done | done (FRQS = []) | see git log |
| 7.1 | done | done (coffee_mug prop in kit) | done (FRQS = []) | see git log |

## Notes for the merging agent

- New helpers: anim/kit.py slope_field(ax, f, xs, ys) and calclib/figs.py slope_field(name, f, xs, ys, xr, yr, curves=...) (tikz segments, aspect-corrected).
