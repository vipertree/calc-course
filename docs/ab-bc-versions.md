# AB and BC versions

Adder, 2026-10-14 (docs/review-notes/2026-10-14-adder-units6-10.md, "6.14, and AB/BC versions"): 6.14 gets two
distinct lessons, one for AB and one for BC, and Units 6, 7 and 8 get two versions of the unit test. These are the
decisions behind how that was built.

## Lesson numbers: 6.14 AB and 6.14 BC

- **6.14** stays the AB lesson. Its files keep their names (`content/topic_6_14.py`, `transcripts/6_14.md`,
  `anim/s6_14.py`) and it uses only AB techniques: basic rules, rewriting, substitution, long division, completing
  the square.
- **6.15** is the BC lesson, internally. A number in the existing `d.d` pattern fits every URL, file name, packet,
  slide deck and saved result with no special cases (`content/topic_6_15.py`, `transcripts/6_15.md`,
  `anim/s6_15.py`). It adds integration by parts and partial fractions to the toolkit, and its worked examples are
  pairs built from the same pieces (x ln x by parts, ln x / x by substitution; 2/(x^2 - 1) by partial fractions,
  2x/(x^2 - 1) by substitution).
- **No student ever sees "6.15".** `web/course/syllabus.json` gives the two topics a display `label` ("6.14 AB",
  "6.14 BC") and points each at its `twin`. `calclib.label()`, `content.label()`, the video title card and outro
  (`anim/kit.py`), the PDFs and the slides all read it. 6.14 is marked `ab: true`; 6.15 is `bc: true` like the other
  BC-only topics.
- **Where a tag sits beside the number** (the course map and the top-bar menu), the number shows as plain "6.14"
  with an AB or a BC tag; everywhere else (lesson header, previous/next, videos, handouts, dashboards) the full label
  says which version it is. The menu now tags every BC-only lesson of a mixed unit, as the map already did.
- **Previous/Next** (`content.neighbours`): the two versions are one stop. A BC lesson (6.13) leads to 6.14 BC and
  any other lesson to 6.14 AB; leaving either version skips its twin. A student in a class follows the class's
  course (AB or BC) instead of the lesson's own tag.
- The videos never say "BC" (Adder, 6.11 review); the AB video's outro goes straight to 7.1.

## Unit tests: U6 / U6BC, U7 / U7BC, U8 / U8BC

- **U6, U7, U8 stay the AB tests.** They already left out the BC-only topics (their docstrings said so), so every
  existing result, release and draft for them is an AB result and needs no migration. Their PDFs now say "Unit 6 AB
  Test" (`UnitTest(ab=True)`).
- **U6BC, U7BC, U8BC are the BC tests**: the whole unit (`content/unit_6bc.py` and so on, `UnitTest(version="BC")`).
  Each is built from its AB test so the two stay parallel: same AP format (12 + 4 multiple choice, 3 free response),
  same two forms A and B, a few slots swapped for the BC topics:
  - Unit 6: integration by parts, partial fractions, an improper integral and a BC antiderivative replace four
    no-calculator slots; FRQ 3 becomes an unbounded-region question (parts or partial fractions, then an improper
    integral).
  - Unit 7: Euler's method and two logistic slots replace three no-calculator slots; the calculator tangent-line slot
    becomes two Euler steps; FRQ 1(b) becomes an Euler's method part; FRQ 3 becomes a logistic model.
  - Unit 8: two arc-length slots (one no-calculator setup, one exact) and a calculator arc length replace three slots;
    FRQ 3(c) becomes "the perimeter of R".
- **Item ids start `u6bc`** (`UnitTest.ids`), so FRQ self-scores, which are keyed by part id alone, never mix between
  versions. `build.py U6BC` loads `content/unit_6bc.py`; the JSON is `web/course/content/U6BC.json` and the PDFs are
  `build/pdf/U6BC/U6BC-unittest-form{A,B}[-key]-classic.pdf`.
- URLs accept `U\d{1,2}(BC)?` (`web/config/urls.py`), and `accounts.models.unit_of("U6BC")` is 6, so access rules,
  free units and grading work unchanged.

## Picking a version

- The course map and the menu list both tests under the unit, each tagged AB or BC ("Leaves out the BC-only topics" /
  "The whole unit, BC topics included"), each with its own best score.
- The unit test page names its version and links the other one; a student in a class sees which version their class
  takes (`Classroom.course`).
- "Next" at the end of a unit (Adder 2026-10-14) leads to the unit test for that lesson's course: 6.14 AB to U6, 6.14
  BC to U6BC, 7.9 and 8.13 (BC topics) to U7BC and U8BC; a class's course overrides that.
- Teachers' handouts list both tests per unit, student copies and keys, as "Unit test, AB version" and "Unit test, BC
  version"; the teacher dashboard and student dashboard name results "Unit 6 AB test" / "Unit 6 BC test".
- Units 9 and 10 are BC-only units with one test each, and Units 0-5 have no BC-only topics: one test, no tag.

## Tests

`web/course/tests_abbc.py`: labels and twins, Next/Previous with and without a class course, the AB versions contain
no BC-only words while the BC versions do, AB and BC item ids never overlap, both versions on the course map, menu,
handouts and dashboards, the version switch, grading and saved results for U7BC, and old U6 results showing as AB.
