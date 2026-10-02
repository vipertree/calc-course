---
name: ap-frq
description: Write or review AP Calculus free-response questions (the FRQS list in content/topic_*.py and the FRQs in content/unit_*.py TEST). Use whenever you add, edit or audit an FRQ, so every part is a question type and phrasing the AP exam actually uses, scored the way the College Board scores it.
---

# Writing AP-style free-response questions

Adder wants the test-prep and unit-test FRQs to look like the real exam. The real exam asks a small set of
question types in a small set of phrasings. Anything outside that set does not belong in an FRQ, even if it is
good mathematics: put it in the notes, practice or quiz instead, or leave the topic without an FRQ.

The reference archive is Adder's own site, https://adderoaks.com/calcfrq (released AB/BC questions 2002-2025
with scoring guidelines, sorted into TABLE, RATE-ACCUMULATION, PARTICLE-MOTION, GRAPH-ANALYSIS,
DIFFERENTIAL-EQUATION, MISCELLANEOUS, BC-ONLY). When unsure whether AP asks something, find a precedent there.
The PDFs download with `curl -sL https://adderoaks.com/calcfrq/<FOLDER>/<YEAR>-AB-Q<n>.pdf` and pymupdf reads them.

## 1. The question types

A real FRQ is one setup (a context, a table, a graph, an equation) with 3 or 4 lettered parts that all use it.
Each part is a separate task worth 1 to 3 points; a full exam question is 9 points. A topic's test-prep FRQ may be
shorter (2-3 parts, 3-7 points) but every part must still be something the exam asks.

| Type (`frq_type`) | What the setup is | Typical parts | Course topics that can use it |
|---|---|---|---|
| Table | Values of a differentiable function (often a rate) at unevenly spaced times, with units | approximate $f'(c)$ by an average rate of change, with units; interpret $f'(c)$ with units; IVT ("Must there be a value $c$ ... such that $f(c) = k$?"); MVT ("... such that $f'(c) = k$?"); fewest number of times $f'$ must be 0; Riemann/trapezoidal sums and their over/under (Unit 6+); a model function for later parts | 1.1, 1.16, 2.1, 2.3, 4.1, 5.1; unit tests |
| Derivatives from a table | $f, f', g, g'$ at a few $x$ values | $h'(c)$ for products, quotients, composites; tangent line to $h$; $(f^{-1})'(a)$ and the tangent line to $f^{-1}$; concavity of $k$ from a given $k'$ | 2.8, 2.9, 3.1, 3.3, 3.5 |
| Rate in context | A formula model $R(t)$ with units, sometimes a second rate out | is the amount increasing or decreasing at $t = a$? Give a reason; value and interpretation of $R'(a)$; time when the instantaneous rate equals the average rate on an interval; end behavior as a limit; time of a maximum/minimum, justified; total amounts by integrals (Unit 6+) | 2.6, 2.7, 2.9, 3.4, 4.1, 4.3, 5.5, 5.11 |
| Particle motion | $x(t)$ or $v(t)$ on the $x$-axis, or a table/graph of $v$ | velocity/acceleration at a time; when or on what intervals the particle moves left/right ("Give a reason"); is the speed increasing or decreasing at $t = a$? ("Give a reason"); position and total distance (by turning points now, by integrals in Unit 8); two particles moving toward/away from each other | 4.2; unit tests 2-4 |
| Graph of f' | Graph of $f'$ made of line segments and semicircles, plus one value of $f$ | relative extrema with justification; intervals of increase; concave down/up with reason; points of inflection with reason; "both increasing and concave up"; tangent line at a known point; $f''(c)$ "find the value or explain why it does not exist"; values of $f$ by areas (Unit 6+); absolute extrema (candidates) | 5.3-5.9 |
| Function analysis | $f$ or $f'$ given by a formula, possibly with a constant $k$ | critical points; classify with First or Second Derivative Test, justify; absolute extrema on a closed interval, justify; inflection points; find $k$ so $f$ has a critical point / inflection point at a given place; tangent line | 3.6, 5.2-5.7, 5.9 |
| Implicit differentiation | A curve given by an equation | "Show that $\frac{dy}{dx} = \dots$"; tangent line at a point; points with horizontal or vertical tangents (or "explain why no such point exists"); approximate a nearby $y$ with the tangent line; $\frac{d^2y}{dx^2}$ at a point and "Does the curve have a relative maximum, relative minimum, or neither at P? Justify"; a particle moving along the curve ($\frac{dx}{dt}$ given, find $\frac{dy}{dt}$) | 3.2, 5.12; unit tests 3, 5 |
| Related rates | Geometric or physical setup with a formula ($V = \frac13\pi r^2h$ is given in the stem) | find a rate at an instant, with units; "Show that $\frac{dh}{dt} = \dots$"; a second rate from the first | 4.4, 4.5; often a last part of a table or model question |
| Linearization | $f(a)$ and $f'(a)$, or a differential equation $\frac{dy}{dx}$ | tangent line equation; use it to approximate $f(b)$; is the approximation an overestimate or underestimate? Give a reason (from the sign of $f''$, often found by the student) | 4.6; unit test 4 |
| L'Hospital's Rule | Values or a graph of $f$, $g$ and their derivatives | "Find the value of $\lim \dots$, or show that it does not exist. Justify your answer."; given that a limit exists and can be found with L'Hospital's Rule, find $f(a)$ and $f'(a)$ | 4.7; part (c) or (d) of a graph or table question |
| Limits and continuity | Piecewise $f$ with constants | "Is $f$ continuous at $x = a$? Use the definition of continuity to explain your answer."; values of the constants that make $f$ continuous, or differentiable, at $a$; one-sided limits from a graph ("find the value or state that it does not exist"); squeeze between two functions ("Is $k$ continuous at $x = a$? Justify") | 1.3, 1.8, 1.11, 1.13, 2.4; unit tests 1-2 |
| Limits at infinity | A model $C(t)$ | "Write a limit expression that describes the end behavior of ... Evaluate this limit expression."; which model or particle is eventually larger, with a reason | 1.15, 3.4 |

Later units (for when the course grows): accumulation and rate in/out with integrals, Riemann and trapezoidal sums,
accumulation functions $g(x) = \int_a^x f(t)\,dt$, average value, area and volume (washers, cross sections, "write
but do not evaluate"), separable differential equations, slope fields, Euler's method (BC), parametric/polar/vector
motion (BC), Taylor polynomials, error bounds and interval of convergence (BC).

**Topics with no FRQ.** Leave `FRQS = []` when AP does not ask the topic as free response: estimating limits from a
table (1.4), limit definitions and limit laws (1.2, 1.5), limit algebra drills (1.6, 1.7), composite limits (1.9),
naming discontinuity types (1.10), continuity on an interval (1.12), vertical asymptotes (1.14), the limit
definition of the derivative (2.2), and building an optimization model from a word problem (5.10). Those are MCQ
material. Builds and the site handle an empty list.

## 2. Phrasings the exam uses

Copy these. They are what students will see in May.

- "Find ..." / "Find the value of ..." / "Find all values of $x$ ..." / "Find the $x$-coordinate of each ..."
- "Approximate $R'(1)$ using the average rate of change of $R$ over the interval $0 \le t \le 2$. Show the work that leads to your answer. Indicate units of measure."
- "Use the data in the table to estimate $H'(6)$. Using correct units, interpret the meaning of $H'(6)$ in the context of the problem."
- "Using correct units, interpret the meaning of your answer in the context of this problem."
- "Must there be a value $c$, for $0 < c < 10$, such that $R(c) = 155$? Justify your answer."
- "Explain why there must be a value $c$, for $1 < c < 3$, such that $h'(c) = -5$."
- "For $0 \le t \le 9$, what is the fewest number of times at which $L'(t)$ must equal 0? Give a reason for your answer."
- "Is the amount of water in the tank increasing or decreasing at time $t = 2$? Give a reason for your answer."
- "Is the speed of the particle increasing, decreasing, or neither at time $t = 2$? Give a reason for your answer."
- "During what open intervals of time $t$ is the particle moving to the left? Give a reason for your answer."
- "On what open intervals, if any, is the graph of $f$ concave down? Give a reason for your answer."
- "Find the $x$-coordinate of each point of inflection of the graph of $f$. Justify your answer." (or "Explain your reasoning.")
- "Does $f$ have a relative minimum, a relative maximum, or neither at $x = 6$? Give a reason for your answer."
- "Find the absolute minimum value of $f$ on the closed interval $[-2, 8]$. Justify your answer."
- "For each of $f''(-5)$ and $f''(3)$, find the value or explain why it does not exist."
- "Write an equation for the line tangent to the graph of $f$ at $x = 2$." Then "Use the tangent line to approximate $f(2.1)$." Then "Is this approximation an overestimate or an underestimate? Give a reason for your answer."
- "Show that $\dfrac{dy}{dx} = \dfrac{3y - 2x}{8y - 3x}$." (the result is given so later parts can use it)
- "Find the coordinates of a point on the curve at which the line tangent to the curve is vertical, or explain why no such point exists."
- "Find the value of $\displaystyle\lim_{x\to2}\frac{6f(x) - 3x}{x^2 - 5x + 6}$, or show that it does not exist. Justify your answer."
- "Is $f$ continuous at $x = 3$? Use the definition of continuity to explain your answer."
- "Write a limit expression that describes the end behavior of the rate of change ... Evaluate this limit expression."
- "Find the time $t$ when the instantaneous rate of change of $C$ equals the average rate of change of $C$ over the time interval $0 \le t \le 4$."
- "Write, but do not evaluate, an integral expression that gives ..." (Unit 6+)

Units go in the stem ("$R(t)$ is measured in words per minute and $t$ is measured in minutes"), and a part that
wants units says "Indicate units of measure." or "Using correct units, ...".

## 3. What not to write

These have all appeared in drafts and none of them is on the exam:

- Meta questions about methods: "Explain why the table alone cannot prove the value of the limit", "Explain why
  $[8, 8]$ cannot be used", "Can the quotient law be used? Explain", "Name the rules you use", "Explain why
  $f'(g(2))g'(2)$ is not the same as $f'(2)g'(2)$".
- Vocabulary quizzes: "classify each discontinuity", "name the indeterminate form", "explain why the function is
  continuous on $[0, 5]$".
- Proofs of facts or theorems: "Explain why $H'(\theta) \ge 30$ for every $\theta$", "prove that ...".
- Derivatives from the limit definition ("Use the limit definition of the derivative to find $f'(x)$").
- Hints inside the prompt ("(Hint: where is $D'(t) = 0$ ...)", "(Topic 5.5 shows why ...)").
- Questions that tell the student the answer's shape ("the graph bends up, above its tangent lines" before asking
  over/under). AP gives $f''$ or the facts about it and lets the student reason.
- A formula for $f'$ next to a "graph of $f'$" question. Graph questions give the graph only, built from lines and
  semicircles so values can be read exactly.
- "Enter the larger one" / "Enter the positive $y$-coordinate". When a part has several answers, use
  `selfcheck(...)` with all of them in the display rather than steering the prompt toward the web box. When a part
  can be asked so it has one answer (one critical point, one time), do that and keep a checked `num(...)`.
- Word-problem modeling for its own sake ("Write the area as a function of $x$ and give its domain"). AP gives the
  model, or asks "Show that ..." when a derived formula is needed later.

## 4. Scoring conventions (the rubric list)

Follow the College Board's points, which Adder grades with:

- A part's points are listed one line per point: `[(1, "answer with supporting work"), (1, "units")]`.
- Estimates from a table: 1 point for a difference quotient that uses table values and the answer. Units are
  their own point when asked (often a single units point shared across parts).
- Interpretation: 1 point needs all of: what quantity changes, at what time, at what rate, with units.
- IVT / MVT justification: 1 point for the hypothesis ("$R$ is differentiable, so $R$ is continuous"), 1 point for
  the numbers and the conclusion ("$R(0) = 90 < 155 < 162 = R(10)$, so by the IVT ..."). "$R$ is continuous"
  alone, without the reason, does not earn the hypothesis point.
- Justifications for extrema and concavity name the sign behavior of the right function: "$f'$ changes from
  positive to negative at $x = 3$", "$f'$ is decreasing on $(1, 4)$", never just "the graph goes down".
- Candidates test: 1 point for considering the critical points and endpoints, 1 point for the answer with
  justification.
- Second Derivative Test, speed, and over/under questions: 1 point usually covers "answer with reason".
- Tangent line: 1 point for the slope or derivative value, 1 point for the equation. A linearization then earns its
  own point for the approximation.
- Related rates: 1 point for differentiating correctly with respect to $t$ (chain rule shown), 1 point for the
  answer, plus units if asked.
- Decimal answers are accurate to three places after the decimal point.

## 5. Encoding an FRQ in this repo

```python
FRQ("Short internal name", intro_tex, [
    Part("a", prompt_tex, answer, solution_tex, [(1, "point 1"), (1, "point 2")], work="2.5cm"),
    ...
], frq_type="Table", calc=False, figure=FIG_X)
```

- `title` is required by the code but students may stop seeing it (printed tests drop it). Keep it short and
  plain; never let it give away the method.
- `intro` holds the setup: function or context, units, tables (`\par\smallskip\centerline{\begin{tabular}...}`).
- `answer`: `num(v, tol=..., display=...)` for one number (put units in `display` as `\ \text{...}` and the web shows
  them beside the box), `expr("...", var="t")` for one expression, `selfcheck(display)` for several answers,
  yes/no with reasons, and interpretations, `dne()` for a limit that does not exist (shown as "Does not exist").
- `solution` is the model solution, written as a student should write it, with the justification sentence.
- `rubric` follows section 4. The FRQ's points are the sum.
- `frq_type` is exactly one of the names in the first column of the table in section 1 (`"Table"`, `"Graph of f'"`, ...).
- `calc=True` only when a calculator part is real (a transcendental equation, a decimal model).
- Figures come from `calclib.figs.graph(...)`: segments as `("expr", a, b)`, semicircles as `sqrt(r^2-(x-c)^2)`.
- Unit tests use `Variants(FA, FB)` per slot. Build both versions from one generator function so they cannot
  drift apart, and give the versions different numbers but the same structure and difficulty.

## 6. Verify every value with sympy

Every keyed number is computed or checked in the file, under the FRQ: `same("frq b", computed, expected)` for
exact values, `close("frq c", computed, expected, 5e-4)` for decimals. Compute from the given data (the table, the
formula), not from the answer you meant to get. Check the facts the question relies on as well: the critical
point is in the interval, the IVT target really is between the values, a "must there be" with answer yes really
has the theorem's hypotheses, a sign used in a justification really has that sign.

## 7. House style

- No em dashes anywhere (validate rejects them in tests). Use commas, colons or separate sentences.
- People in contexts have racially diverse names, and now and then a nonbinary character, referred to as "they"
  in passing. Never announce pronouns.
- A limit that does not exist is "Does not exist" (`dne()`), not "DNE" in prose.
- Units in words: "feet per minute", "degrees Celsius per minute", "gallons per hour per hour".
- Run Adder's copy-review skill on new stems and solutions.

## 8. Checklist

1. Is each part a type and phrasing from sections 1-2, with an archive precedent you could name?
2. Does the topic merit an FRQ at all? If AP only asks it as MCQ, `FRQS = []`.
3. Is the content within what the topic and earlier topics teach (no Unit 6 integrals in Unit 4)?
4. Do the parts share one setup, and does each stand alone if an earlier part is wrong (AP carries values forward with "from part (a)")?
5. Rubric: points per part 1-3, totals sensible, justification points named the AP way.
6. Every value computed with sympy below the FRQ; `python build.py <n> --web --docs testprep` passes validation.
7. No em dashes, no hints, no meta questions, no "Enter the ...".
8. Look at the rendered test-prep PDF page (pymupdf to PNG) and the web page for the topic.
