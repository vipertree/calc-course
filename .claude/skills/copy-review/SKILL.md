---
name: copy-review
description: Review and rewrite user-facing copy so it stops sounding machine-written. Strips em dashes, "it's not X, it's Y" constructions, rhetorical-question reveals, rule-of-three padding, and overused LLM vocabulary (delve, seamless, genuinely, honestly, vibrant, journey...). Use when asked to "copy review", de-AI, humanize, punch up, or tighten UI text, onboarding, store listings, READMEs, tooltips, error messages, or game dialogue in a game or app.
---

# Copy review

Goal: text a sharp human copywriter would sign off on. It shouldn't set off anyone's "a chatbot wrote this" alarm. You're not making the prose fancier; you're taking the autopilot out.

## Scope

1. **Default target: user-facing strings.** HTML/templates, UI strings in JS/TS/Swift/Kotlin/etc., i18n files (`.json`, `.strings`, `.po`), store listings, README, marketing pages, in-game dialogue, tooltips, toasts, errors, notifications, `<title>` tags.
2. **Code comments, docstrings, commit messages, and internal docs are out of scope** unless the user asks. Report the count and leave them alone.
3. If the user names files, a directory, or pastes text, review only that.
4. Never change string keys, identifiers, format placeholders (`{name}`, `%s`, `${n}`, `{{ var }}`), HTML structure, or anything a test asserts on without updating the test too.

## Workflow

1. **Triage with the scanner.** It over-flags on purpose, so don't treat it as the verdict.
   ```bash
   python3 .claude/skills/copy-review/scripts/scan.py <paths> --min-severity med
   python3 .claude/skills/copy-review/scripts/scan.py <paths> --summary   # counts only
   ```
   Severities: `high` is almost always a fix, `med` is a fix unless it's clearly the right word, `low` counts only in clusters (three intensifiers in one blurb is a tell; one isn't).
2. **Read the copy in context.** The scanner can't see the patterns that span sentences or paragraphs (see "Structural tells"). Read every user-facing string in scope, not just the flagged lines.
3. **Rewrite.** Apply the rules below. Keep meaning, tone, and length budget (UI strings often have hard width limits, so a rewrite should come out no longer than the original, and ideally shorter).
4. **Re-run the scanner** on the touched files to confirm the high/med hits are gone or deliberately kept.
5. **Report** in a compact table (file:line, before, after) plus a line listing anything you kept on purpose and why. Group repetitive fixes ("27 em dashes in titles → `·`") instead of listing each one.

## The rules

### 1. Em dashes: zero, and no disguised substitutes

Remove every `—` (and `&mdash;`, `—`). Do **not** swap in ` - `, ` – `, or ` -- `. Those are the same tell in a cheap disguise. Choose by what the dash was doing:

| Dash was doing | Replace with | Example |
|---|---|---|
| Joining two full clauses | Period, or semicolon if tightly linked | "Stage scored — paused" → "Stage scored. Paused." |
| Introducing an explanation/list | Colon | "Partner up — they can't refuse" → "Partner up: they can't refuse" |
| Parenthetical aside | Commas, or parentheses | "The frog — the blue one — won" → "The blue frog won" (or just cut the aside) |
| Dramatic pause before a punchline | Delete the drama; restructure | "One thing matters — speed" → "Speed is all that matters" |
| Separator in titles/labels | `·`, `|`, `:` or a line break | "Join ABCD — Frog Legs" → "Join ABCD · Frog Legs" |
| Empty-value placeholder in a table/stat | Fine to keep (it's typography, not prose), or use `–`/`n/a` | `<span>—</span>` |
| Ranges (numbers, dates) | En dash `–` or "to" | "3—5 players" → "3–5 players" |

Often the best fix is splitting the sentence in two. Short sentences sound human.

### 2. Kill the negative-parallelism family

The single loudest tell after em dashes. Say the positive claim directly.

- "It's not a game, it's an experience." → "Every round tells a story." (or cut entirely)
- "This isn't just a race." → "A race where betting matters more than speed."
- "Not only fast, but also fun." → "Fast and fun."
- "More than just a to-do list." → say what it *is*.
- "Not ten. Not fifty. Five hundred." → "Five hundred."
- "Less about X, more about Y." → "It's about Y."

Exception: a correction of a misconception the user holds ("Bets aren't refunded. They go to the pot.") is fine. Test: would a human say it this way in conversation?

### 3. Banned and suspect vocabulary

Replace with the plain word, or delete. Most of these are intensifiers or throat-clearing that carry no information.

**Always replace** (high): delve, tapestry, testament to, genuinely, honestly, seamless(ly), elevate, unleash, unlock (as metaphor), embark, realm, bustling, vibrant, meticulous(ly), ever-evolving, game-changer, journey (unless literal), boasts, nestled, whimsical, captivating, enchanting, breathtaking, immersive, unparalleled, harness, furthermore, moreover, in conclusion, in summary, "in today's fast-paced world", "a symphony/dance of".

**Replace unless it's precisely right** (med): crucial, pivotal, robust, leverage, foster, underscore, showcase, intricate, nuanced, landscape, ecosystem, holistic, comprehensive, empower, transformative, revolutionize, cutting-edge, effortless, curated, quietly, serves as / stands as (→ "is"), dive into / deep dive, at its core, resonate, streamline, enhance, utilize (→ use), facilitate (→ help), plethora, myriad, paramount, embrace, "whether you're X or Y", "look no further", "rest assured".

**Cap per piece** (low): really, truly, actually, simply, just, very, incredibly, absolutely, literally, deeply. One is fine. Clusters are a tell.

**Chatbot residue** (always remove from product copy): "Great question!", "Certainly!", "Absolutely!", "I hope this helps", "Feel free to…", "Let me know if…", "Happy [verb]ing!".

### 4. Structural tells

The scanner catches some of these; most need reading.

- **Rule of three.** Triplets of adjectives or benefits ("fast, fun, and friendly"). Keep the strongest one or two. Vary list lengths.
- **Rhetorical-question reveal.** "The catch? Nobody wins." → "Nobody wins."
- **Signposting.** "Here's the thing", "It's worth noting", "Let's break it down", "Think of it as", "Imagine a world where", "The truth is", "Make no mistake". Delete; start with the point.
- **Stakes inflation.** "Redefines how you play", "the ultimate party game", "like never before". Say something concrete and checkable instead.
- **False ranges.** "From casual players to seasoned strategists, and everything in between." → name the actual audience or cut.
- **Fragment stacks.** "Fast. Chaotic. Hilarious." Fine once on a splash screen, grating anywhere else.
- **Superficial -ing tails.** "…, highlighting the importance of teamwork." Cut the tail.
- **Hedge stacks.** "may potentially", "could possibly". Pick one or commit.
- **Summary echo.** Final paragraph restating everything. Cut it.
- **Uniform rhythm.** Every sentence the same length and shape. Vary it: one short, one long.
- **Bold-lead bullets everywhere.** `**Feature**: description` for every list. Fine in docs, robotic in marketing copy.
- **Decoration.** Arrows (→), sparkles (✨), rockets (🚀), ✅ bullets in prose. Keep only where they're real UI affordances (a "Next →" button is fine).
- **Title Case Every Heading** when the rest of the product uses sentence case. Match the product.
- **Vague attribution.** "Players love…", "Experts agree…". Cite or cut.

### 5. What good replacement copy looks like

- Concrete nouns and verbs over adjectives. "Bet on the frog you think will lose" beats "Engage in thrilling strategic wagering."
- Second person, present tense, active voice for UI.
- Say the specific thing. Numbers, names, actions.
- Match the product's existing voice. If the game is goofy, stay goofy; de-AI doesn't mean de-personality.
- Buttons are verbs. Errors say what happened and what to do.
- Contractions are good.
- If a sentence exists only to sound nice, delete it.

## Guardrails

- Don't "fix" code, data, or proper nouns (a character literally named "Journey" stays).
- Don't flatten deliberate voice: a pirate NPC can say "Behold!". Flag it, don't change it, if unsure.
- Don't introduce new tells while fixing old ones (the classic: replacing "—" with " - ", or "delve into" with "dive into").
- Keep i18n in sync: if you rewrite the source-language string, note that translations are now stale; don't machine-translate them unless asked.
- Run the project's tests after editing strings; tests often assert on copy.
