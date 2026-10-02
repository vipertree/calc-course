# Escaping the Claude-y Look

Sep 30, 2026 · @Adder

## Bottom line

The Claude look is what the model emits when nobody has made a design decision. Telling it to "not look AI-generated" doesn't work; making the decisions for it does.

Three moves carry most of the benefit:

1. Give it a concrete anchor (a real reference, a palette, a font pair) before any code is written.
2. Name the defaults you ban, specifically. A list of tells beats adjectives.
3. Force a plan-then-critique pass so the first draft gets argued with.

One trap: banning the old defaults just promotes the next ones. The purple gradient is now passé as a tell; cream plus terracotta is the current Claude signature, and I'd bet (roughly 80%) that's what you're seeing.

## The tells

The Claude look is a cluster, not one trait. Anthropic's own [frontend-design skill](https://www.aitmpl.com/component/skill/creative-design/frontend-design) names the main clusters AI design gravitates to, and [third-party audits](https://github.com/funboy322/avoid-ai-design) extend the list.

| Category | Tell | Note |
| --- | --- | --- |
| Color | Warm cream background (near #F4F1EA) with terracotta or clay accent (near #D97757) | The skill says this accent is Claude's own interface color, so on your brief it reads as a tell |
| Color | Near-black background with one acid-green or vermilion accent | Second named cluster |
| Color | Purple-to-blue gradients; cyan or purple accents on dark | The older, better-known slop palette ([vibecodekit](https://vibecodekit.dev/ai-slop-design)) |
| Color | Gradient washes as decoration; tinted near-black (#0B0B0B, #111) standing in for black | Listed in the skill |
| Type | High-contrast serif display over a clean sans body | Pairs with the cream look |
| Type | Inter, Roboto, Open Sans, or the system stack chosen by default | A font nobody chose is the tell, not the font ([925 Studios](https://www.925studios.co/blog/ai-slop-design-tells)) |
| Type | "Safe" replacement picks such as Space Grotesk | One version of avoid-ai-design's catalog also lists Geist, Instrument Serif, Fraunces; another [guide](https://www.aidesigner.ai/blog/claude-code-frontend-design) holds up Fraunces as good output, so what matters is whether you chose it |
| Layout | Centered hero, then a row of three feature cards; or a big number, small label, and gradient accent as the hero | The skill calls the stat-plus-gradient hero the default treatment |
| Layout | Broadsheet cosplay: hairline rules, zero radius, dense columns | Third named cluster |
| Layout | Everything in a card, cards inside cards, one border radius and the same soft gray shadow on all of them | Skill; [Impeccable](https://dev.to/_46ea277e677b888e0cd13/stop-your-ai-coding-tool-from-generating-generic-ui-impeccable-design-skill-4g1l) |
| Chrome | Tracked all-caps eyebrow above every heading; mono face for small labels; "WORD — fragment" labels; A · B · C meta strings; arrows appended to links and buttons | The skill's "template chrome" |
| Chrome | One word in a headline italicized, bolded, or colored | Named in the skill |
| Chrome | 01 / 02 / 03 numbering on content that isn't a sequence | Skill; also [anti-ai-slop](https://github.com/Vinayak-Shukla-03/anti-ai-slop) |
| Chrome | Fake window dots, emoji as icons, big rounded icons above headings | anti-ai-slop; Impeccable |
| Chrome | Glassmorphism, gradient headline text, untouched shadcn defaults | [avoid-ai-design](https://github.com/funboy322/avoid-ai-design) |
| Motion | The same fade-and-slide-up on every section, a hover transition on every card | Skill |
| Copy | Benefit-speak ("transform your workflow"), generic CTAs | Copy reads as templated as the layout |

## What others say

The consensus is wide and shallow. Nearly everyone agrees on the cause and the remedy; almost nobody has measured anything.

- **Cause:** the model samples from the statistical center of its training data, so unspecified design means median design ([aidesigner](https://www.aidesigner.ai/blog/claude-code-frontend-design), [925 Studios](https://www.925studios.co/blog/ai-slop-design-tells)). Anthropic's own [cookbook](https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics) says Claude defaults to safe choices unless pushed, and recommends explicitly calling out the defaults.
- **Anthropic's fix has aged:** the official frontend-design skill was rewritten to cast Claude as a design lead whose client already rejected templated work, with a plan-then-critique loop ([claudeskills.org](https://www.claudeskills.org/docs/skills-cases/frontend-design)). One developer argues the default skill [now produces the slop it was meant to prevent](https://dev.to/lovestaco/teaching-your-ai-web-design-some-actual-taste-4p13), and prefers a community skill (Impeccable) that names concrete anti-patterns.
- **The second-order trap:** asking for "less AI" yields the next default. The [avoid-ai-design](https://github.com/funboy322/avoid-ai-design) author says exactly that: cream plus terracotta, all-caps mono labels, one colored headline word, numbered features.
- **Vague adjectives fail:** [MindStudio](https://www.mindstudio.ai/blog/build-design-system-claude-design-no-ai-aesthetics) recommends real reference screenshots and a maintained component library over style words. [A prompting guide](https://ui-ux-pro-max-skill.com/blog/avoiding-ai-slop/) adds that asking the model to choose gets the median, while asking it to apply a specific item from a curated set does not.
- **Critique needs named rejects:** a commenter on that Dev.to post warns that agents will polish a page back toward the average unless the review pass lists specific things to reject.

Caveat: most of this is blog posts and repos selling a skill. As far as I can tell, the only evidence of effect is self-scored (anti-ai-slop rebuilt its own 10-artifact test set). Treat the advice as plausible, not proven.

## What works, ranked

Ranked by my expected payoff per minute of effort. The ordering is my judgment, not measured.

1. **Make the core decisions yourself.** Pick a real reference (a product, a print piece, an era), 4–6 named hex colors, and a display/body font pair by name. Claude then executes instead of choosing. This beats every prompt trick below. Anthropic's own skill says the brief's words win over its default-avoidance rules, so specifics you state get followed.
2. **Replace all three legs of the stool.** If you keep the cream background, serif display, or terracotta accent, the page still reads as Claude. Change the palette and the type, not just one. Also confirm fonts are actually loaded; a face declared in CSS but never loaded silently falls back to the default.
3. **Ban named tells, not vibes.** List exact colors, fonts, and components. Include the second-order defaults (cream and terracotta, mono eyebrows, one colored headline word, 01/02/03 numbering), not just purple gradients.
4. **Fix structure, not skin.** Three-card rows and cards-in-cards are layout habits, so recoloring won't cure them. For an app, design around the real content: actual data density, tables, asymmetric or unusual grids, and a nav that fits the task.
5. **Require plan, then critique, then build.** Have Claude state palette, type, layout, and one signature element, then check that plan against your ban list before writing code. The critique only works if it names concrete rejects.
6. **Generate three divergent directions, pick one.** Cheap, and it breaks the pull toward the median. One developer's loop: five styles side by side, three layout variations of the winner, then tune fonts, accent, and motion in a live tweak panel added to the dev server, so you judge by eye instead of by prompt.
7. **Lock tokens.** Put colors, type scale, radii, and spacing in CSS variables or a DESIGN.md that CLAUDE.md points to, so later screens don't drift back to defaults.
8. **Write the copy, or give a voice sample.** Generic benefit-speak makes a distinctive design read as templated anyway.
9. **Render it and look.** Screenshot the result and review it against the ban list. Finish with a deletion pass: remove one decorative element per screen.

An honest note on the skills: several community ones (Impeccable, Hallmark, avoid-ai-design, anti-ai-slop) automate items 3 and 5. They might save you effort, but you can get most of the value from a hand-written block, and a skill's own default palette is itself a new convergence point if everyone installs it. The same Dev.to author warns that narrowly prescriptive skills hand you the same output every time.

## Drop-in CLAUDE.md block

Fill the bracketed slots yourself; the slots are the point. Everything else is the ban list and the process gate.

```markdown
## Frontend design

Direction: [one sentence: a real reference plus a mood, e.g. "a 1970s airline timetable, but for a scheduling tool"]

Palette (use only these): bg [#...], surface [#...], text [#...], accent [#...], alert [#...]
Type: display [font], body [font], mono [font]. Load each one explicitly and verify it renders.
Layout: [e.g. dense, left-aligned, asymmetric; built around the real data, not a marketing page]

Never, unless I name it above:
- Cream or off-white background with terracotta/clay accent; serif display over sans body by default
- Near-black background with one neon accent
- Purple or indigo gradients, gradient text, glassmorphism
- Inter, Roboto, Open Sans, system font stack, Space Grotesk, Geist, Instrument Serif, Fraunces
- Three-up feature card rows, cards inside cards, uniform rounded corners with a 1px gray border on everything
- All-caps tracked eyebrow labels, one accented word in a heading, decorative 01/02/03 numbering, fake window dots, emoji as icons, the same fade-and-slide-up on every section, arrows appended to button text
- Benefit-speak copy ("transform your workflow")

Process: before writing CSS, state the palette, type pairing, layout, and one signature element. Critique that plan against the Never list and fix it. Build. Then screenshot the result and list any Never item that slipped in.
```

If Claude keeps drifting, put the direction and ban list in a DESIGN.md and reference it from CLAUDE.md so it is re-read every session.

## Sources

Pages marked † were opened in full; the rest I read as search excerpts only. Searched 2026-09-30.

- † [Frontend Design skill text (mirror)](https://www.aitmpl.com/component/skill/creative-design/frontend-design): the named clusters, hex values, template chrome, plan-then-critique process
- † [Teaching Your AI Web Design Some Actual Taste](https://dev.to/lovestaco/teaching-your-ai-web-design-some-actual-taste-4p13): critique of the default skill, Impeccable, build-in-loops workflow; the named-rejects point is from a reader comment
- † [avoid-ai-design](https://github.com/funboy322/avoid-ai-design): tell catalog by category. The copy I opened predates the README text my search excerpts showed, which adds the cream-plus-terracotta second-order defaults
- [Anthropic cookbook: prompting for frontend aesthetics](https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics)
- [Frontend Design skill breakdown, claudeskills.org](https://www.claudeskills.org/docs/skills-cases/frontend-design)
- [anti-ai-slop](https://github.com/Vinayak-Shukla-03/anti-ai-slop)
- [Impeccable write-up, Dev.to](https://dev.to/_46ea277e677b888e0cd13/stop-your-ai-coding-tool-from-generating-generic-ui-impeccable-design-skill-4g1l)
- [AI Slop Fonts and Gradients, 925 Studios](https://www.925studios.co/blog/ai-slop-design-tells)
- [AI Slop Design fix guide, vibecodekit](https://vibecodekit.dev/ai-slop-design)
- [Avoiding AI slop: 7 prompt techniques](https://ui-ux-pro-max-skill.com/blog/avoiding-ai-slop/)
- [Design system in Claude Design, MindStudio](https://www.mindstudio.ai/blog/build-design-system-claude-design-no-ai-aesthetics)
- [How to Design Beautiful UIs With Claude Code, aidesigner](https://www.aidesigner.ai/blog/claude-code-frontend-design)
