# Unit 8 build: handoff log

Branch: `claude/admiring-feynman-m8ygr9`, continuing after Unit 7 (UNIT7_HANDOFF.md). Same rules: built per
.claude/skills/unit-building and lesson-writing; nothing rendered; each topic passes tools/transcripts.py,
py_compile, and `build.py X.Y --no-pdf`.

## Status

| Topic | Transcript | Scene | Notes/problems | Commit |
|---|---|---|---|---|
| 8.1 | done | done | done (table FRQ: trapezoid average, MVT, average value vs average rate) | see git log |
| 8.2 | done | done | done (particle-motion FRQ) | see git log |
| 8.3 | done | done | done (rate-in-context FRQ) | see git log |
| 8.4 | done | done | done (FRQS = []; area FRQs come in 8.6 and the unit test) | see git log |
| 8.5 | done | done | done (FRQS = []) | see git log |
| 8.6 | done | done | done (area FRQ: regions R and S, net vs total, dividing line) | see git log |
| 8.7 | done | done (oblique(), base_curve(), oblique_axes() added to kit) | done (FRQS = []) | see git log |
| 8.8 | done | done (sections/base_region/rect_section moved to kit; isosceles_hyp kind) | done (area + cross-section FRQ) | see git log |
| 8.9 | done | done (solid_about_vertical in kit) | done (FRQS = []) | see git log |

## Notes for the merging agent

- New helpers:
  - calclib/figs.py `region(name, fns, xr, yr, pieces, var="x"|"y")`: graph() with shaded regions (drawn under the
    curves via graph()'s new `under=` argument).
  - anim/kit.py `region(ax, top, bottom, a, b, var)`, `slice_rect(ax, top, bottom, at, d, var, label)`,
    `solid_of_revolution(ax, r_out, a, b, r_in, axis_y)`, `cross_section(kind, p0, p1)`. None rendered yet: check
    them on the first render of 8.4/8.7/8.9.
- Render every scene and run video-review / notes-review.
