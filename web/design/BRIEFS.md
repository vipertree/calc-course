# Design briefs

Four alternate looks for the course site, written as the design direction the
"Escaping the Claude-y Look" research says the human should supply. Each one names
a real reference, a type pairing, exact colors, layout and component rules, and a
ban list. They are built as switchable designs next to the original look, which
stays available as **Classic** (Dark = Slate, Light = Paper).

## Why the current look reads as Claude

Checked against the tell table in the research:

- Paper theme: warm cream background (#f7f2e8) with a terracotta accent (#b4412f)
  and a serif body with a sans UI. That is the exact current Claude signature.
- Slate theme: tinted near-black (#0e1216) with one vermilion accent (#ff6b5a).
  That is the second named cluster.
- Everything sits in cards with one radius and the same soft shadow; the course
  map is a uniform grid of identical rounded cards.
- Template chrome: tracked all-caps labels ("SOLUTION", "MEMBERS", "BC ONLY"),
  pill badges, a ▶ glyph prefix on the video title.

So every brief below replaces all three legs (palette, type, structure), not just one.

## Rules that apply to all four

- Every color is a CSS token; each design defines light and dark token sets that
  hook into the existing Dark/Light toggle and the device default.
- The math color vocabulary stays semantic (func, secant, tangent, area, accum,
  deriv) but each design re-inks it in its own palette. Figures keep using
  `currentColor` and `var(--bg)`.
- KaTeX and MathLive stay untouched in size and font. The video panel stays sticky.
- No tracked all-caps eyebrows, no pill badges, no soft drop shadows, no fade-and-slide
  motion, no arrows glued onto buttons, no emoji, no gradient text.

---

## 1. Transit

**Reference.** Massimo Vignelli and Bob Noorda's *New York City Transit Authority
Graphics Standards Manual* (1970), read through Josef Müller-Brockmann's *Grid
Systems in Graphic Design*. The subway sign is the model: white grotesk on a black
band, colored route bullets, nothing decorative.

**Idea.** A course is a route. Every unit gets a line color, every topic is a
station, the topic number is a round route bullet. The course map is drawn as a
strip map, not a card grid. A "Map layout" toggle on the course map (cookie `maplayout`) picks
how the strip map reads. Rows (the default) runs the line across each row, turns
down at the row's end and comes back under it to the next row, like a line of
text. Columns stacks the stations down each column, so the vertical lines match
the reading order. At phone width both are one vertical line.

**Type.** Public Sans (Google Fonts; the US Web Design System face, a civic
grotesk), one family on purpose, as in Swiss work. Archivo was tried first and
dropped: its P-space kerning ran "AP Calculus" together. Headings Public Sans 800 at tight leading (1.05) and slight negative tracking; body
Public Sans 400 at 17px/1.6; UI labels Public Sans 600. No second face.

**Palette.**

| Token | Light | Dark (signage) |
| --- | --- | --- |
| bg | #FFFFFF | #000000 |
| panel | #F1F1F1 | #161616 |
| ink | #000000 | #FFFFFF |
| ink-2 | #2B2B2B | #D6D6D6 |
| dim | #5E5E5E | #A3A3A3 |
| rule | #000000 | #FFFFFF |
| link / accent | #0039A6 | #FCCC0A |
| good / bad | #00933C / #D52B1E | #6CBE45 / #FF5A4F |

Unit lines (MTA route colors): U1 #EE352E, U2 #00933C, U3 #B933AD, U4 #0039A6,
U5 #FF6319, U6 #FCCC0A, U7 #6CBE45, U8 #996633, U9 #808183, U10 #00A1DE.
Math palette: func #0039A6, secant #FF6319, tangent #EE352E, area #00933C,
accum #B933AD, deriv #00933C.

**Layout.** The site header is a solid black sign band (white type) in both modes,
with a 6px line-color rule under it on lesson pages. Flush-left everywhere, big
asymmetric headings. Lesson head: a large route bullet on the left, title set big
and heavy beside it. Step headings hang their bullet in the left gutter. Course
map: each unit is a vertical route line with stations; ready topics are open
circles on the line, unwritten topics are ticks.

**Components.**
- Buttons: rectangles, 0 radius, 2px black border. Primary is solid black with
  white text (yellow on black in dark). No hover lift, only an inverse fill.
- Cards: no box. A 4px rule on top, as the manual separates sign panels.
- Inputs: 2px bottom rule only, light gray fill.
- Tabs: bold words; the active one gets a thick 6px bar above it in the unit color.

**Avoid.** Hairline rules (the broadsheet cluster), rounded cards, shadows, any
mono type, more than one typeface, centered text.

---

## 2. Drafting

**Reference.** A green engineering computation pad (the National Brand 42-381 style
sheet with the grid printed on the back so it ghosts through), and for dark mode
a cyanotype blueprint. The drawing title block in the lower right of every
engineering sheet supplies the header.

**Idea.** Worked math on the paper engineers use for worked math. Final answers are
boxed and double-underlined, as engineering students are taught.

**Type.** B612 (Google Fonts; designed by Airbus for cockpit displays) for headings
and the title block, Barlow 400/600 for body, Barlow Semi Condensed 500 for small
labels. Labels are sentence case except the title block field names, which follow
drafting convention.

**Palette.**

| Token | Light (pad) | Dark (blueprint) |
| --- | --- | --- |
| bg | #E6EEDB | #0E3A66 |
| grid line | #CBDCB3 | rgba(255,255,255,.07) |
| panel | #F2F6EA | #11457A |
| panel-2 | #DAE5C8 | #16518C |
| ink | #1F2A22 | #F3F7FB |
| ink-2 | #37443A | #CFE0F1 |
| dim | #56634F | #9EBBD8 |
| rule | #7E9867 | #8DB0D6 |
| accent (blue pencil) | #1D4F91 | #FFE27A (yellow grease pencil) |
| redline | #B42318 | #FF8C82 |
| good | #2D6A1F | #9BE28A |

Math palette light: func #1D4F91, secant #A15C00, tangent #B42318, area #2D6A1F,
accum #6B3FA0. Dark: func #8FD3FF, secant #FFE27A, tangent #FF8C82, area #9BE28A,
accum #D7B8FF.

**Layout.** A 20px CSS grid covers the page. The lesson header is a drafting title
block: a ruled box of cells (topic number, unit, title) with 2px ink borders.
The notes column carries a vertical double rule on its left, like a pad margin.
Step numbers are square boxes.

**Components.**
- Buttons: square corners, 2px ink border, flat fill of the pad color; primary is
  blue pencil fill with white type. Pressed state shifts 1px down.
- Cards: a 1.5px ink outline, no radius, no shadow, pad-colored fill so the grid
  stops behind them.
- Inputs: white answer boxes with a 1.5px ink border.
- Answers and solution labels: "Answer" line double-underlined.
- Tabs: file-folder index tabs with square shoulders; the active tab joins the page.

**Avoid.** Handwriting fonts, fake paper textures from images, rounded corners,
monospace labels, neon on dark (blueprint is a mid blue, not near-black).

---

## 3. Textbook

**Reference.** A LaTeX-set mathematics book: Spivak's *Calculus*, Knuth's own
TeX-produced books, AMS journal articles. The page looks like it came out of
`pdflatex` with `amsthm` and `hyperref`.

**Idea.** The text and the math are set in the same face, so KaTeX output stops
looking pasted in. Structure comes from theorem environments, not boxes.

**Type.** Computer Modern, via the KaTeX_Main and KaTeX_SansSerif faces that the
site already loads from jsdelivr with KaTeX (Google Fonts has no Computer Modern;
no new font host is added). Body KaTeX_Main 19px/1.55, headings KaTeX_Main bold,
UI chrome (tabs, buttons, header) in KaTeX_SansSerif.

**Palette.** Named xcolor `dvipsnames` colors, since that is what a LaTeX author reaches for.

| Token | Light | Dark (PDF reader night mode) |
| --- | --- | --- |
| bg | #FFFFFF | #1D2025 |
| panel | #FFFFFF | #1D2025 |
| panel-2 | #F2F2F2 | #282C33 |
| ink | #000000 | #E9E6E0 |
| ink-2 | #222222 | #CAC6BF |
| dim | #595959 | #9A968F |
| rule | #000000 | #E9E6E0 |
| link (RoyalBlue) | #0071BC | #6DB8F2 |
| good (OliveGreen) | #3C8031 | #8FCB7F |
| bad (BrickRed) | #B6321C | #F08C78 |

Math palette: func RoyalBlue #0071BC, secant BurntOrange #C86B00, tangent BrickRed
#B6321C, area OliveGreen #3C8031, accum Plum #92268F (dark versions lightened).

**Layout.** A single centered text block with a book measure (about 36em) for the
practice and quiz pages; the notes keep the sticky video column. Steps read as
numbered sections ("§1 Start here"). The course map is a table of contents with
dot leaders running to the progress figure, like page numbers.

**Components.**
- Definitions and big ideas: run-in bold label, italic body, no box (amsthm style).
- Formula boxes: a thin `\fbox` frame, square.
- Worked solutions end with a tombstone ∎.
- Buttons: a thin black frame around sans text, square; primary is inverse.
- Cards: none. Examples, checks and exercises are separated by space and a run-in
  bold head, as in a book.
- Inputs: a thin underline only.
- Tabs: plain sans words separated by space, active one bold with a rule under it.

**Avoid.** Serif-display-over-sans-body (everything is one family), cream paper,
colored panels, drop caps, decorative ornaments beyond ∎ and §.

---

## 4. Chalkboard

**Reference.** A working classroom board: Feynman's last Caltech blackboard for
dark mode, a whiteboard with dry-erase markers for light mode. The four marker
colors (black, blue, red, green) are what real teachers carry.

**Idea.** The page is the board the teacher is writing on: headings and step numbers
in a teacher's hand, body text in a type built for reading, and every color is a
real chalk or marker color.

**Type.** Kalam 700 (Google Fonts) for headings, tabs and labels; Lexend 400/500
(designed to improve reading fluency) for body, UI and every numeral. Numbers
stay in Lexend because Kalam's 1 reads as a slash inside a circle.

**Palette.**

| Token | Light (whiteboard) | Dark (chalkboard) |
| --- | --- | --- |
| bg | #F3F5F4 | #24372E |
| panel | #FFFFFF | #2B4036 |
| panel-2 | #E6EAE8 | #33493E |
| ink | #1D2320 | #F0EFE6 |
| ink-2 | #3A423E | #D3DACF |
| dim | #5D6762 | #A7B8AC |
| rule | #B7C0BC | #5E7A6B |
| accent (marker blue / yellow chalk) | #1F57C3 | #F4E285 |
| red | #C8302C | #F4A6A6 |
| green | #17804A | #B5E3A1 |
| tray | #AEB6B9 (aluminum) | #7A5A3A (wood) |

Math palette light: func #1F57C3, secant #B26A00, tangent #C8302C, area #17804A,
accum #7A3FB0. Dark (colored chalk): func #9ED3F2, secant #F4E285, tangent #F4A6A6,
area #B5E3A1, accum #D9C2F0.

**Layout.** The header sits on the board frame: a thick tray-colored ledge below it.
Wide left-aligned board with the video pinned as if taped to the board's edge.
Step numbers are hand-drawn circles. The course map is a class schedule written up
on the board: unit headings in the hand face, topics as a plain two-column list.

**Components.**
- Buttons: marker outlines with slightly irregular radii (hand-drawn loop); primary
  is filled marker blue (yellow chalk on the dark board).
- Cards: a hand-drawn outline in rule color, no shadow, no fill on the board.
- Inputs: white (light) or darker board (dark) with a marker underline.
- Tabs: handwritten words, the active one underlined with a thick chalk stroke.

**Avoid.** Novelty chalk textures that hurt reading, handwriting in body text, emoji
doodles, cream, gradients.

---

## Critique pass (plan checked against the ban list before building)

- Transit dark is black with bright accents: that is close to the "near-black plus
  one neon" cluster. Fix: pure #000 (not a tinted near-black), and several route
  colors carrying meaning instead of one accent.
- Drafting's title-block field names are all caps. Allowed only there, because
  that is drafting convention; everywhere else labels are sentence case.
- Textbook uses zero radius and rules, which can drift into broadsheet cosplay.
  Fix: no hairline column rules or dense columns; one wide text block, space
  instead of lines.
- Chalkboard risks being a novelty skin. Fix: the hand face is only on headings
  and numbers; body stays Lexend, and no image textures.
- All four: the old tracked-caps "SOLUTION" and "MEMBERS" labels and pill badges
  are restyled to sentence case in every new design.
