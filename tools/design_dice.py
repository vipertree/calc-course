#!/usr/bin/env python3
"""Roll design directions for the course site, so the options aren't just my defaults.

    python tools/design_dice.py [how_many] [seed]

Adder (2026-10-08): the transit/subway look is turning into a Claude house style; find new directions and do
something clever to randomize them. Each roll draws a reference world from outside web design (its palette and
shapes come from that world, not from a web palette), a type pairing from fonts that are not AI favourites, and a
layout idea, then rejects anything that lands on a known AI cluster. The seed comes from os.urandom unless given,
and is printed, so a roll can be reproduced.
"""
import os
import random
import sys

# Where the look comes from: a physical thing with its own colours, materials and conventions.
WORLDS = {
    "Japanese school notebook": dict(colors=["pale blue rule lines", "manila cover", "red margin line", "pencil graphite"],
                                     motif="dotted 5 mm grid, a title box at the top of each page, tabbed sections"),
    "Montessori math materials": dict(colors=["beech wood", "bead red", "bead blue", "bead green"],
                                      motif="rounded wooden tiles, bead bars as progress, felt-textured panels"),
    "1960s slide rule and instrument dials": dict(colors=["ivory celluloid", "black engraving", "brass", "signal red hairline"],
                                                  motif="scales with tick marks, a sliding cursor as the progress marker"),
    "Topographic survey map": dict(colors=["contour brown", "survey green", "water blue", "paper buff"],
                                   motif="contour lines as section dividers, map legend for the formula box"),
    "Eurogame rulebook": dict(colors=["meeple orange", "board-game teal", "card-stock white", "rule-box mustard"],
                              motif="example boxes with player icons, numbered setup steps, component callouts"),
    "Museum exhibition labels": dict(colors=["gallery white", "wall paint sage", "object-label charcoal"],
                                     motif="object labels with accession numbers, wall text, generous negative space"),
    "1980s children's encyclopedia": dict(colors=["primary yellow", "cobalt", "tomato", "airbrush sky"],
                                          motif="cutaway diagrams, numbered callouts, 'Did you know?' bubbles"),
    "Risograph zine": dict(colors=["fluorescent pink", "medium blue", "misregistered overprint"],
                           motif="two-ink overprints, halftone shading on graphs, stapled-spine layout"),
    "Engineering drafting sheet": dict(colors=["vellum", "drafting-pencil grey", "red-line markup"],
                                       motif="title block in the corner, dimension lines, revision table as progress"),
    "Botanical field guide": dict(colors=["specimen ink", "leaf green", "pressed-flower violet", "herbarium paper"],
                                  motif="plates with figure numbers, specimen tags, key-to-species decision trees"),
    "Chalkboard and colored chalk": dict(colors=["slate green", "chalk white", "chalk yellow", "chalk pink"],
                                         motif="hand-drawn underlines, erasure smudges, the teacher's boxed rule"),
    "Library card catalog": dict(colors=["oak drawer", "card stock", "typewriter ink", "brass label holder"],
                                 motif="index cards with call numbers, drawer pulls as navigation"),
    "Airline safety card": dict(colors=["airline navy", "safety orange", "warm grey"],
                                motif="numbered pictogram panels, 'do this, not this' pairs"),
    "Weather station / barograph chart": dict(colors=["chart paper", "barograph purple ink", "instrument steel"],
                                              motif="drum-chart traces as graphs, readings in small boxed gauges"),
}

# Display / text pairings, deliberately away from the AI-default faces (Inter, Space Grotesk, DM Sans, Fraunces,
# Playfair, Instrument Serif, Cormorant, IBM Plex, JetBrains Mono, Newsreader).
TYPE = [
    ("Gloock", "Literata"), ("Young Serif", "Hanken Grotesk"), ("Bitter", "Atkinson Hyperlegible"),
    ("Zilla Slab", "Source Serif 4"), ("Familjen Grotesk", "Spectral"), ("Darker Grotesque", "Gelasio"),
    ("Alegreya SC", "Alegreya"), ("Chivo", "Charis SIL"), ("Bodoni Moda", "Albert Sans"),
    ("Archivo Narrow", "Libre Caslon Text"), ("Sono", "Sono"), ("Schibsted Grotesk", "Crimson Pro"),
    ("Red Hat Display", "Red Hat Text"), ("Kalam", "Atkinson Hyperlegible"), ("Overpass", "Overpass"),
]

LAYOUTS = [
    "notebook spread: video on the left page, notes on the right page, a spine down the middle",
    "single tall column with margin notes in the outer gutter, formula boxes pinned in the margin",
    "stacked cards that slide like a card-catalog drawer, one idea per card",
    "a board-game style track across the top showing the lesson's steps as spaces",
    "a fixed instrument panel (video + controls) with the notes scrolling underneath like chart paper",
    "a gallery wall: each section is an object with a label beside it",
]

# Known AI clusters: a roll is thrown out if its words land here.
CLICHES = ["purple", "gradient", "cream", "terracotta", "acid", "vermilion", "hairline", "newsprint", "broadsheet",
           "neon", "glass", "subway", "transit", "signage"]


def roll(rng):
    world = rng.choice(sorted(WORLDS))
    w = WORLDS[world]
    display, text = rng.choice(TYPE)
    layout = rng.choice(LAYOUTS)
    accent = rng.choice(w["colors"])
    return {"world": world, "colors": w["colors"], "accent": accent, "motif": w["motif"],
            "display": display, "text": text, "layout": layout}


def cliche(r):
    blob = " ".join(str(v) for v in r.values()).lower()
    return [c for c in CLICHES if c in blob]


def main(n=8, seed=None):
    n = int(n)
    seed = int(seed) if seed is not None else int.from_bytes(os.urandom(4), "big")
    rng = random.Random(seed)
    print(f"seed {seed}")
    seen, out = set(), []
    while len(out) < n:
        r = roll(rng)
        if cliche(r) or r["world"] in seen:
            continue
        seen.add(r["world"])
        out.append(r)
    for i, r in enumerate(out, 1):
        print(f"\n{i}. {r['world']}\n   colors: {', '.join(r['colors'])} (lead with {r['accent']})\n   motif: {r['motif']}"
              f"\n   type: {r['display']} / {r['text']}\n   layout: {r['layout']}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
