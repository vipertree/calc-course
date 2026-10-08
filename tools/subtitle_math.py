#!/usr/bin/env python3
"""Render spoken function expressions in WebVTT captions as mathematical notation."""

import re
import sys
from pathlib import Path


EXPRESSIONS = [
    ("s of t equals sixty t minus twelve t squared", "s(t) = 60t - 12t²"),
    ("g of x equals x squared minus one over x minus one", "g(x) = (x² - 1)/(x - 1)"),
    ("f of x equals x squared minus three x", "f(x) = x² - 3x"),
    ("g of x equals x cubed", "g(x) = x³"),
    ("y equals x plus one", "y = x + 1"),
    ("limit as x approaches one of g of x equals two", "limₓ→₁ g(x) = 2"),
]

ARGUMENTS = {
    "x": "x", "t": "t", "zero": "0", "one": "1", "two": "2",
    "three": "3", "four": "4", "negative two": "−2",
}


def _phrase_pattern(phrase):
    # WebVTT may split an expression across adjacent caption cues, and punctuation can
    # land at a cue boundary. Treat spaces and commas alike between spoken tokens.
    words = phrase.split()
    return re.compile(r"[\s,]+".join(map(re.escape, words)), re.IGNORECASE)


def convert(text):
    blocks = text.strip().split("\n\n")
    header, cue_blocks = blocks[0], blocks[1:]
    cues = []
    for block in cue_blocks:
        lines = block.splitlines()
        timing_index = next((i for i, line in enumerate(lines) if " --> " in line), None)
        if timing_index is None:
            continue
        cues.append((lines[:timing_index + 1], " ".join(lines[timing_index + 1:])))

    joined = " ".join(text for _, text in cues)
    owners = []
    for cue_index, (_, cue_text) in enumerate(cues):
        if cue_index:
            owners.append(cue_index - 1)
        owners.extend([cue_index] * len(cue_text))

    # Replace longer, complete function expressions before the general f(x) forms.
    for spoken, notation in EXPRESSIONS:
        pattern = _phrase_pattern(spoken)
        for match in reversed(list(pattern.finditer(joined))):
            owner = owners[match.start()]
            joined = joined[:match.start()] + notation + joined[match.end():]
            owners[match.start():match.end()] = [owner] * len(notation)

    def function_notation(match):
        name, argument = match.group(1), match.group(2).lower()
        return f"{name}({ARGUMENTS.get(argument, argument)})"

    function_pattern = re.compile(
        r"\b([fghsTP])\s+of\s+(negative\s+two|zero|one|two|three|four|x|t)\b",
        re.IGNORECASE,
    )
    for match in reversed(list(function_pattern.finditer(joined))):
        replacement = function_notation(match)
        owner = owners[match.start()]
        joined = joined[:match.start()] + replacement + joined[match.end():]
        owners[match.start():match.end()] = [owner] * len(replacement)

    article_before_limit = re.compile(r"\bwrite the (limₓ→₁)", re.IGNORECASE)
    for match in reversed(list(article_before_limit.finditer(joined))):
        replacement = "write " + match.group(1)
        owner = owners[match.start()]
        joined = joined[:match.start()] + replacement + joined[match.end():]
        owners[match.start():match.end()] = [owner] * len(replacement)

    cue_texts = [""] * len(cues)
    for char, owner in zip(joined, owners):
        cue_texts[owner] += char

    # A notation replacement can leave only punctuation at the start of the next
    # timed cue. Keep that punctuation with the expression it closes.
    for index in range(1, len(cue_texts)):
        match = re.match(r"^([,.;:!?]+)\s*", cue_texts[index])
        if match and cue_texts[index - 1].strip():
            cue_texts[index - 1] = cue_texts[index - 1].rstrip() + match.group(1)
            cue_texts[index] = cue_texts[index][match.end():]

    rendered = [header]
    for (cue_header, _), cue_text in zip(cues, cue_texts):
        rendered.append("\n".join(cue_header + [cue_text.strip()]))
    return "\n\n".join(rendered) + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: subtitle_math.py <captions.vtt>")
    path = Path(sys.argv[1])
    path.write_text(convert(path.read_text()))
