#!/usr/bin/env python3
"""Flag common AI-writing tells in text and source files.

Usage: scan.py [PATH ...] [--min-severity {low,med,high}] [--ext .md,.html,...]

Stdlib only. Prints file:line:col  [severity/category] match  |  context
Exit code 1 if anything at or above --min-severity was found.
This is a triage tool: it over-flags. A human (or Claude) decides what to change.
"""
import argparse
import os
import re
import sys

SEV = {"low": 0, "med": 1, "high": 2}

DEFAULT_EXT = {
    ".md", ".mdx", ".txt", ".html", ".htm", ".jinja", ".j2", ".njk", ".hbs",
    ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".py", ".json", ".yaml",
    ".yml", ".toml", ".strings", ".po", ".xml", ".swift", ".kt", ".java",
    ".cs", ".gd", ".lua", ".rb", ".go", ".rs", ".dart", ".csv", ".ini",
}
SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", ".next", "out", "vendor",
    "__pycache__", ".venv", "venv", "env", "migrations", ".cache", "coverage",
    "target", "Pods", ".gradle", "Library",
}
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "Cargo.lock"}

# (severity, category, regex). Word lists are case-insensitive, whole-word.
PUNCT = [
    ("high", "em-dash", r"—"),
    ("high", "em-dash", r"&mdash;|&#8212;|\\u2014"),
    ("med", "dash-substitute", r"(?<=\w) -- (?=\w)|(?<=\w)--(?=[a-zA-Z]{2})"),
    ("med", "dash-substitute", r"(?<=[a-z,]) – (?=[a-zA-Z])"),  # spaced en dash used as em dash
    ("low", "dash-substitute", r"(?<=[a-z]) - (?=[a-z])"),           # spaced hyphen used as dash
    ("low", "unicode-decor", r"[→⇒➡✨\U0001F680\U0001F4A1✅]"),
    ("low", "ellipsis-char", r"…"),
]

WORDS_HIGH = [
    "delve", "delves", "delving", "tapestry", "testament to", "genuinely",
    "honestly", "seamless", "seamlessly", "elevate", "elevates", "unleash",
    "unlock the", "embark", "realm", "bustling", "vibrant", "meticulous",
    "meticulously", "in today's fast-paced", "ever-evolving", "game-changer",
    "game changer", "navigate the", "navigating the", "journey", "boasts",
    "nestled", "a symphony of", "a dance of", "whimsical", "captivating",
    "enchanting", "breathtaking", "immersive", "unparalleled", "harness the",
    "furthermore", "moreover", "in conclusion", "in summary",
]
WORDS_MED = [
    "crucial", "pivotal", "robust", "leverage", "leveraging", "foster",
    "fostering", "underscore", "underscores", "showcase", "showcasing",
    "intricate", "nuanced", "landscape", "ecosystem", "holistic",
    "comprehensive", "empower", "empowers", "empowering", "transformative",
    "revolutionize", "cutting-edge", "state-of-the-art", "effortless",
    "effortlessly", "curated", "elevated", "quietly", "additionally",
    "serves as", "stands as", "boast", "thrilling", "epic", "ultimate",
    "dive into", "dive in", "deep dive", "at its core", "the heart of",
    "resonate", "resonates", "streamline", "streamlined", "enhance",
    "enhances", "utilize", "utilizes", "facilitate", "plethora", "myriad",
    "paramount", "embrace", "whether you're", "look no further",
    "rest assured", "i hope this helps", "great question", "certainly!",
    "absolutely!", "of course!",
]
# Filler intensifiers: fine in moderation, damning in clusters. Low severity.
WORDS_LOW = [
    "truly", "really", "deeply", "incredibly", "absolutely", "simply",
    "actually", "literally", "just", "very", "super", "totally",
]

CONSTRUCTIONS = [
    ("high", "not-x-but-y", r"\b(?:it's|it is|this is|that's|that is|they're|they are|we're|you're)\s+not\s+(?:just\s+|only\s+|about\s+)?[^.;!?\n]{1,60}?[,;:—–-]+\s*(?:it's|it is|but|they're|they are|this is|that's)\b"),
    ("high", "not-x-but-y", r"\b(?:isn't|aren't|wasn't|weren't|doesn't|don't)\s+(?:just|only|merely|simply)\b"),
    ("high", "not-x-but-y", r"\bnot\s+(?:just|only|merely)\s+[^.;!?\n]{1,50}?,?\s+but\s+(?:also\s+)?"),
    ("high", "not-x-but-y", r"\bmore than just\b|\bless about\b[^.\n]{1,50}\bmore about\b"),
    ("high", "not-x-not-y", r"\bNot\s+\w+[^.\n]{0,25}\.\s+Not\s+\w+[^.\n]{0,25}\.\s+"),
    ("med", "rhetorical-reveal", r"(?:^|[.!]\s+)(?:The|And the|But the)\s+(?:\w+\s){0,3}\w+\?\s+[A-Z]"),
    ("med", "signpost", r"\b(?:here's the (?:thing|kicker|catch|deal|twist)|here's (?:where|why|what)|it's worth noting|it is worth noting|let's break (?:this|it) down|let's unpack|let's dive|let's explore|think of it (?:as|like)|imagine a world|the truth is|the reality is|make no mistake|to be clear|the best part\??|the result\?|spoiler:?)\b"),
    ("med", "false-range", r"\bfrom\s+[\w\s'-]{2,30}\s+to\s+[\w\s'-]{2,30},?\s+(?:and\s+)?(?:everything|anything)\s+in\s+between\b"),
    ("med", "hedge-stack", r"\b(?:may|might|could)\s+(?:potentially|possibly|perhaps)\b"),
    ("med", "whether-youre", r"\bwhether you're\b[^.\n]{1,60}\bor\b"),
    ("low", "despite-challenges", r"\bdespite (?:these|its|the|some) (?:challenges|hurdles|setbacks)\b"),
    ("low", "ready-to", r"\b(?:ready to|get ready to|are you ready)\b"),
]


def wordlist_pattern(words):
    alts = sorted((re.escape(w) for w in words), key=len, reverse=True)
    return r"(?<![\w-])(?:" + "|".join(alts) + r")(?![\w-])"


def build_rules():
    rules = [(s, c, re.compile(p)) for s, c, p in PUNCT]
    rules.append(("high", "ai-word", re.compile(wordlist_pattern(WORDS_HIGH), re.I)))
    rules.append(("med", "ai-word", re.compile(wordlist_pattern(WORDS_MED), re.I)))
    rules.append(("low", "filler-word", re.compile(wordlist_pattern(WORDS_LOW), re.I)))
    case_sensitive = {"not-x-not-y", "rhetorical-reveal"}
    rules += [(s, c, re.compile(p, 0 if c in case_sensitive else re.I)) for s, c, p in CONSTRUCTIONS]
    return rules


def iter_files(paths, exts):
    for root in paths:
        if os.path.isfile(root):
            yield root
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
            for f in filenames:
                if f in SKIP_FILES or f.endswith(".min.js") or f.endswith(".map"):
                    continue
                if os.path.splitext(f)[1].lower() in exts:
                    yield os.path.join(dirpath, f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", default=["."])
    ap.add_argument("--min-severity", choices=SEV, default="low")
    ap.add_argument("--ext", help="comma-separated extensions to scan (overrides default)")
    ap.add_argument("--summary", action="store_true", help="print counts per category only")
    a = ap.parse_args()

    exts = {e if e.startswith(".") else "." + e for e in a.ext.split(",")} if a.ext else DEFAULT_EXT
    floor = SEV[a.min_severity]
    rules = [r for r in build_rules() if SEV[r[0]] >= floor]
    counts, hits = {}, 0

    for path in iter_files(a.paths, exts):
        try:
            with open(path, encoding="utf-8") as fh:
                lines = fh.readlines()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(lines, 1):
            if len(line) > 2000:  # minified or data blob
                continue
            for sev, cat, rx in rules:
                for m in rx.finditer(line):
                    hits += 1
                    counts[cat] = counts.get(cat, 0) + 1
                    if not a.summary:
                        ctx = line.strip()
                        if len(ctx) > 140:
                            s = max(0, m.start() - 60)
                            ctx = "…" + line[s:s + 140].strip() + "…"
                        print(f"{path}:{n}:{m.start() + 1}  [{sev}/{cat}] {m.group(0)!r}  |  {ctx}")

    if a.summary or hits:
        print(f"\n{hits} hits: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])), file=sys.stderr)
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
