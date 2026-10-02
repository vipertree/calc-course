---
name: notes-review
description: Review the AP Calculus guided notes as students see them on the site (and in the PDFs). Use after editing content/topic_*.py, after build.py --web, and whenever Adder reports a rendering or formatting problem in the notes.
---

# Notes review

The notes are authored in `content/topic_*.py` (a LaTeX subset), built by `build.py` into PDFs and
`web/course/content/*.json`, and rendered on the site with KaTeX. Rendering problems Adder has caught:
raw TeX showing as text, blanks nested inside math, displays broken around blanks, long formulas squeezed
inline, tables full of tedious blanks.

## 1. Build, then run the checker

```bash
cd /workspace/repos/calc-course
export PATH=$HOME/opt/texlive/bin/x86_64-linux:$PATH
~/opt/mamba/envs/calc/bin/python build.py 1.2 1.4 --web --no-pdf          # PDFs too when the LaTeX changed
export LD_LIBRARY_PATH=$HOME/chromium-libs/root/usr/lib/x86_64-linux-gnu
python3 tools/notes_review.py 1.2 1.4 --shots /tmp/notes_review            # or: all; dev server must be on :8018
```

The static checks flag raw TeX, long or tall inline math, blanks inside tables, and missing video examples.
The browser pass (logged in as `demo-student`) flags KaTeX errors and anything wider than the column, and saves
full-page screenshots.

## 2. Look at the screenshots

Crop and read the screenshots (they are tall; crop 2000 px at a time). Check:

- **Displays**: important formulas on their own centered line; no stray punctuation on its own line
  (put the period inside the display: `\[ ... = 3. \]`); short expressions mid-sentence stay inline.
- **Blanks**: `\blank{...}` in text, `\mblank{...}` inside math. A display with blanks renders as a centered
  line of display-style pieces (`calclib/web.py`, `_display_blank_lines`): fine, but keep such displays short.
- **Tables are filled in** when they hold data or computations; blanks are for big ideas.
- **Every worked example from the video appears in the notes** (`calclib/videx.py` adds them from the scene;
  a table or graph problem needs `text=`/`notes_graph=` on the scene's `self.example` call).
- Multi-part problems list their parts (a), (b), ... in the problem itself.
- Limit notation on every line; piecewise functions as `cases`.

## 3. PDFs

When LaTeX changed, build without `--no-pdf` and render a page or two with PyMuPDF
(`fitz.open(...)[i].get_pixmap(dpi=70).save(...)`) to look at it. The build fails loudly on LaTeX errors and on
raw TeX that would leak to the web (`LEFTOVER`).

Report what was checked and what was fixed, naming anything left.
