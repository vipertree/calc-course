# Teacher slide decks

One deck per topic, in two versions (Adder 2026-10-14 and 10-15):

- **Solutions shown**: every worked example revealed one step per slide.
- **Blank**: each problem on its own slide with nothing worked. The teacher works it on the board or over the slide;
  there is no "work it out here" box.

Both versions show every formula, definition and notes line in full: no fill-in blanks (the students fill in their own
notes), and no "Prepared for" line. Pictures are stills rendered by manim, not video.

Each version is an HTML deck the site presents in the browser and a PowerPoint file to download.

## Building

```bash
anim/stills.sh 2.1                                                   # the lesson's stills, both looks (a few minutes)
~/opt/mamba/envs/calc/bin/python tools/build_slides.py 2.1 2.2      # or: all
    --no-pptx      skip the PowerPoint export (it screenshots every slide, the slow part)
    --media-root /workspace/repos/calc-course   read stills from another checkout (a worktree has none)
```

Output goes to `build/slides/<num>/` (ignored by git, like `build/pdf/`):
`deck-solutions.html`, `deck-blank.html`, `<num>-slides-{solutions,blank}.pptx`, `stills/`, and `manifest.json`.
The manifest's `log` says when a topic had no stills.

The slides come from the topic's content source (`content/topic_X_Y.py`) and the scene's `self.example(...)`
calls, the same blocks the notes PDF and the lesson page use, so a rebuild picks up any content change.

- Title slide, then each notes section: text, tables and figures on "Notes" slides; each formula box, definition
  and big idea on its own slide.
- Each worked example: a problem slide, then step slides (solutions version only).
- Each quick check: the prompt, then the answer (solutions version only).
- A closing slide listing the formula boxes and big ideas, and the next topic.

The PowerPoint export screenshots each slide in headless chromium (system python3 + playwright, with
`LD_LIBRARY_PATH=$HOME/chromium-libs/root/usr/lib/x86_64-linux-gnu`), in the light look at 1.5 times 1080p. Plain
titles are editable text, the math and stills are a picture, and the speaker notes hold the slide's text as LaTeX. In
the blank version the notes leave out the solutions, in case a teacher shares the file.

## Stills

`anim/stills.sh <num>` runs the lesson's manim scene with `-s` (nothing animated, so it costs a few minutes, not a
render) and `CALC_STILLS` set. `anim/kit.py` then saves, at 1080p on a transparent background (no paper, border or
logo), into `build/stills/<slug>/{light,dark}/`:

- `<beat>-end.png` for every transcript beat: its fullest frame (a frame is kept before each animation that takes
  things off screen, and the one with the most drawn on it wins).
- For each worked example, `<beat>-problem.png` as posed (before the solving starts) and, when it has a figure,
  `<beat>-figure-problem.png` and `<beat>-figure.png`: the figure cropped out, as posed and as solved.
- `stills.json` lists them.

The builder shares a section's beat stills out over its text slides, in video order. A slide that gets several is
repeated ("1 of 3", "2 of 3", ...), its text held still while the picture steps through the animation (Adder
2026-10-15); a section with no text slide shows them on picture slides. A slide that already has the notes' graph
gets none. An example's figure goes beside the problem (posed) and the last solution step (solved); a notes figure is
the fallback when the video has none. The deck swaps
light and dark stills with its look. Re-run `stills.sh` after a scene changes.

## Who can open them

Teacher accounts only. A teacher reaches a deck from:

- **Handouts and slides** (`/teacher/handouts/`, linked from the teacher dashboard): a **Slides** link on each
  topic that has a deck.
- **The lesson page**: a "Teacher slides for this topic" button, shown only to teachers.

Both lead to `/teacher/slides/<num>/`, which has "Present in the browser" and "Download PowerPoint" for each version.

`course/views.py` (`slides_page`, `slides_file`) answers 403 to students and visitors for every URL under
`/teacher/slides/`: the page, both decks, the PowerPoint files, and every still. Only names matching
`course/slides.py:FILE_RE` are handed out, so `manifest.json` and anything else in the folder 404. When a teacher
opens a deck, the server opens it in the teacher's site look.

## Production (nginx)

The decks are **not** under `web/static/`, so `collectstatic` never copies them and no `/static/` location serves
them. Don't move them there: anything nginx serves directly skips the teacher check.

Django can stream the files itself, but in production let nginx send the bytes
after Django has checked the account. Set `SLIDES_ACCEL=/protected-slides/` in the app's environment, and add an
internal location to the vhost:

```nginx
# only reachable through X-Accel-Redirect from Django, never from a browser
location ^~ /protected-slides/ {
    internal;
    alias /home/deploy/calc-course/build/slides/;    # settings.SLIDES_DIR
    add_header Cache-Control "private, max-age=3600";
}
```

With that set, `slides_file` checks the account and answers with `X-Accel-Redirect: /protected-slides/<num>/<file>`
and an empty body. nginx then serves the file with Range support. The HTML decks are always rendered by Django,
since they get the teacher's look. Keep the `^~` here. If the vhost has a static-extension regex location (the adderoaks vhost does), a plain prefix
location loses to it for `.png` URLs, and `internal` never applies. (The browser
never sees `/protected-slides/` URLs. The deck asks for `/teacher/slides/...`, which goes to Django.)

Also make sure `build/slides/` is readable by the user nginx runs as, and that a plain request to
`/protected-slides/1.2/stills/<file>.png` returns 404.

`SLIDES_DIR` can be set in the environment if the decks are built somewhere other than `<repo>/build/slides`.
