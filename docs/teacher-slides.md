# Teacher slide decks

One deck per topic, in two versions:

- **Solutions shown**: notes blanks filled in (bold and underlined, so they read in grayscale), and every worked
  example revealed one step per slide.
- **Blank**: notes blanks left open, and each problem followed by a slide with room to work it live.

Each version is an HTML deck the site presents in the browser and a PowerPoint file to download.

## Building

```bash
~/opt/mamba/envs/calc/bin/python tools/build_slides.py 1.2 1.3      # or: all
    --no-pptx      skip the PowerPoint export (it screenshots every slide, the slow part)
    --no-clips     skip the video clips
    --media-root /workspace/repos/calc-course   read videos and voicemaps from another checkout (a worktree has none)
```

Output goes to `build/slides/<num>/` (ignored by git, like `build/pdf/`):
`deck-solutions.html`, `deck-blank.html`, `<num>-slides-{solutions,blank}.pptx`, `clips/`, and `manifest.json`.
The manifest's `log` lists every clip that was skipped and why.

The slides come from the topic's content source (`content/topic_X_Y.py`) and the scene's `self.example(...)`
calls, the same blocks the notes PDF and the lesson page use, so a rebuild picks up any content change.

- Title slide, then each notes section: text, tables and figures on "Notes" slides; each formula box, definition
  and big idea on its own slide.
- Each worked example: a problem slide with its silent clip, then step slides (solutions) or a work slide (blank).
- Each quick check: the prompt, then the answer (solutions) or room to work (blank).
- A closing slide listing the formula boxes and big ideas, and the next topic.

The PowerPoint export screenshots each slide in headless chromium (system python3 + playwright, with
`LD_LIBRARY_PATH=$HOME/chromium-libs/root/usr/lib/x86_64-linux-gnu`), in the light look at 1.5 times 1080p. Plain
titles are editable text, the math is a picture, clips are embedded movies, and the speaker notes hold the slide's
text as LaTeX. In the blank version the notes leave out the solutions, in case a teacher shares the file.

## Clips

Every worked example gets a silent clip cut from `web/static/video/<slug>.mp4` (light) and `<slug>-dark.mp4` (dark).
The deck plays the one matching its current look. Where a notes section's title matches a transcript beat, that
beat's animation goes on the section's first slide too.

- The cut points come from `anim/media/pub_<slug>_<look>/voicemap_<slug>.json`, written by the render.
- The solutions version plays the whole example. The blank version stops when the solving starts, so the class
  sees the problem and "Pause and try it."
- A topic with no voicemap, or with a voicemap older than its video, gets no clips. Its decks still build, and the
  manifest log says why.
- Re-run the tool after renders finish. Clips already cut from the same video at the same times are kept, and clips
  no deck uses any more are deleted.

Before `anim/kit.py` change f7ef173, only renders in Adder's recorded voice (1.1 and 1.2 so far) wrote a voicemap.
Since that change every render writes one, and it adds `video_end` for each beat plus `think_at` and `solve_at`
for each worked example. Topics rendered before the change get clips once they are re-rendered.

## Who can open them

Teacher accounts only. A teacher reaches a deck from:

- **Handouts and slides** (`/teacher/handouts/`, linked from the teacher dashboard): a **Slides** link on each
  topic that has a deck.
- **The lesson page**: a "Teacher slides for this topic" button, shown only to teachers.

Both lead to `/teacher/slides/<num>/`, which has "Present in the browser" and "Download PowerPoint" for each version.

`course/views.py` (`slides_page`, `slides_file`) answers 403 to students and visitors for every URL under
`/teacher/slides/`: the page, both decks, the PowerPoint files, and every clip and poster. Only names matching
`course/slides.py:FILE_RE` are handed out, so `manifest.json` and anything else in the folder 404. When a teacher
opens a deck, the server adds "Prepared for <name>" to its title slide and opens it in the teacher's site look.

## Production (nginx)

The decks are **not** under `web/static/`, so `collectstatic` never copies them and no `/static/` location serves
them. Don't move them there: anything nginx serves directly skips the teacher check.

Django can stream the files itself (with HTTP Range, so clips seek), but in production let nginx send the bytes
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
since they get the teacher's name and look. Keep the `^~` here. If the vhost has a static-extension regex location (the adderoaks vhost does), a plain prefix
location loses to it for `.jpg` and `.mp4` URLs, and `internal` never applies. (The browser
never sees `/protected-slides/` URLs. The deck asks for `/teacher/slides/...`, which goes to Django.)

Also make sure `build/slides/` is readable by the user nginx runs as, and that a plain request to
`/protected-slides/1.2/clips/ex1-full.mp4` returns 404.

`SLIDES_DIR` can be set in the environment if the decks are built somewhere other than `<repo>/build/slides`.
