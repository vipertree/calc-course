# Video transcripts

One file per topic, `X_Y.md`. These are the scripts the manim scenes get built from,
written for review BEFORE anything is animated or voiced.

Math claims in the narration get hidden checks, evaluated with sympy by the checker:

    <!-- check: limit((x**2-1)/(x-1), x, 1) == 2 -->

Format (the checker parses it):

    # 1.1 Title
    ## Beat name
    **On screen:** what the viewer sees (for the animator; not spoken)
    > Narration, one paragraph per line. This is exactly what the voice reads.

Pacing: mark deliberate silences with `[pause]` (about 1 s) or `[long pause]` (about 2 s), inline or on a
line of their own. They are stripped from the spoken text and become silence in the render. Adder wants
the videos unhurried: explain the why, give the viewer a beat after each key idea.

Rules for narration (from the copy-review skill): no em dashes, no "not X, it's Y",
no rhetorical-question reveals, no signposting ("let's dive in"), plain words.
Math is written the way it is spoken ("s of t", "h approaches zero").

    python3 tools/transcripts.py          # check all, print runtimes
    python3 tools/transcripts.py 1.1      # one topic
