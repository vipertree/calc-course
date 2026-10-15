"""The AP FRQ Archive (/frq/). Runs against a small made-up archive in a temp folder, so the suite never needs the
real files (build/frq/ is not in git)."""
import json
import shutil
import tempfile
from pathlib import Path

from django.test import TestCase, override_settings


def _q(year, exam, n, cat, text, shared=False):
    qid = f"{year}-{exam.lower()}-{n}"
    return {"id": qid, "year": year, "exam": exam, "number": n, "categories": [cat] if cat else [],
            "exams": ["AB", "BC"] if shared else [exam], "sources": [], "text": text,
            "question_pages": [{"file": "q1.webp", "w": 1224, "h": 1584}],
            "guideline_pages": [{"file": "s1.webp", "w": 1224, "h": 1584}, {"file": "s2.webp", "w": 1224, "h": 1584}],
            "pdf": f"{qid}.pdf", "pdf_size": 2048}


QUESTIONS = [
    _q(2025, "AB", 3, "TABLE", "3. A student starts reading a book at time t = 0 minutes. Selected values of R(t)."),
    _q(2024, "AB", 2, "PARTICLE-MOTION", "2. A particle moves along the x-axis with velocity v(t). Find the total distance.",
       shared=True),
    _q(2019, "BC", 2, "BC-ONLY", "2. Let R be the region enclosed by the polar curve r = 3 sin(2θ)."),
    _q(2010, "AB", 1, "RATE-ACCUMULATION", "1. Water flows into a tank at a rate modeled by the function W(t)."),
    _q(2003, "AB", 6, "", "6. Let f be the function defined on the closed interval."),
]


class FRQArchive(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tmp = Path(tempfile.mkdtemp())
        (cls.tmp / "manifest.json").write_text(json.dumps({"questions": QUESTIONS, "problems": []}))
        for q in QUESTIONS:
            d = cls.tmp / "files" / q["id"]
            d.mkdir(parents=True)
            for name in ("q1.webp", "s1.webp", "s2.webp"):
                (d / name).write_bytes(b"RIFF0000WEBPVP8 ")
            (d / q["pdf"]).write_bytes(b"%PDF-1.4 test")
        cls.settings = override_settings(FRQ_DIR=cls.tmp)
        cls.settings.enable()

    @classmethod
    def tearDownClass(cls):
        cls.settings.disable()
        shutil.rmtree(cls.tmp)
        super().tearDownClass()

    def html(self, url):
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200, url)
        html = r.content.decode()
        self.assertNotIn("—", html, url)          # no em dashes, Adder's rule
        self.assertNotIn("&mdash;", html, url)
        for dialog in ("alert(", "confirm(", "prompt("):
            self.assertNotIn(dialog, html, url)
        return html

    def test_pages_load_without_an_account(self):
        for url in ("/frq/", "/frq/table/", "/frq/bc-only/", "/frq/miscellaneous/", "/frq/q/2025-ab-3/", "/frq/q/2019-bc-2/"):
            html = self.html(url)
            self.assertIn("College Board", html, url)        # the attribution is on every page
            self.assertIn("does not endorse it", html, url)

    def test_index_lists_everything_by_type(self):
        html = self.html("/frq/")
        self.assertIn("5 questions, newest first.", html)
        for qid in ("2025-ab-3", "2024-ab-2", "2019-bc-2", "2010-ab-1", "2003-ab-6"):
            self.assertIn(f'href="/frq/q/{qid}/"', html)
        self.assertIn("Not sorted yet", html)
        for slug in ("table", "rate-accumulation", "particle-motion", "graph-analysis", "differential-equations",
                     "miscellaneous", "bc-only"):
            self.assertIn(f'href="/frq/{slug}/"', html)

    def test_category_page_shows_only_its_questions(self):
        html = self.html("/frq/table/")
        self.assertIn('href="/frq/q/2025-ab-3/"', html)
        self.assertNotIn('href="/frq/q/2024-ab-2/"', html)
        self.assertIn("1 question, newest first.", html)

    def test_unknown_category_404s(self):
        self.assertEqual(self.client.get("/frq/nope/").status_code, 404)

    def test_exam_filter_counts_shared_questions_on_both_exams(self):
        html = self.html("/frq/?exam=BC")
        self.assertIn('href="/frq/q/2019-bc-2/"', html)
        self.assertIn('href="/frq/q/2024-ab-2/"', html)          # AB/BC shared question
        self.assertNotIn('href="/frq/q/2025-ab-3/"', html)
        html = self.html("/frq/?exam=AB")
        self.assertNotIn('href="/frq/q/2019-bc-2/"', html)
        self.assertIn('href="/frq/q/2025-ab-3/"', html)
        self.assertIn("Also on the BC exam", html)

    def test_year_range_filter(self):
        html = self.html("/frq/?from=2010&to=2020")
        self.assertIn('href="/frq/q/2019-bc-2/"', html)
        self.assertIn('href="/frq/q/2010-ab-1/"', html)
        self.assertNotIn('href="/frq/q/2025-ab-3/"', html)
        self.assertNotIn('href="/frq/q/2003-ab-6/"', html)
        swapped = self.html("/frq/?from=2020&to=2010")             # a backwards range still means the same years
        self.assertIn('href="/frq/q/2019-bc-2/"', swapped)
        self.assertNotIn('href="/frq/q/2025-ab-3/"', swapped)

    def test_text_search(self):
        html = self.html("/frq/?q=tank")
        self.assertIn('href="/frq/q/2010-ab-1/"', html)
        self.assertNotIn('href="/frq/q/2025-ab-3/"', html)
        self.assertIn("1 question matches, newest first.", html)
        html = self.html("/frq/?q=particle+distance")             # every word has to be there
        self.assertIn('href="/frq/q/2024-ab-2/"', html)
        self.assertIn("No questions match.", self.html("/frq/?q=zebra"))

    def test_filters_combine_with_category_and_bad_values_are_ignored(self):
        html = self.html("/frq/particle-motion/?exam=BC&from=2020")
        self.assertIn('href="/frq/q/2024-ab-2/"', html)
        html = self.html("/frq/?exam=XYZ&from=abc&to=")
        self.assertIn("5 questions", html)

    def test_question_page(self):
        html = self.html("/frq/q/2025-ab-3/")
        self.assertIn("AB Question 3", html)
        self.assertIn('src="/frq/file/2025-ab-3/q1.webp"', html)
        self.assertIn("Show the scoring guidelines", html)
        self.assertIn('src="/frq/file/2025-ab-3/s2.webp"', html)
        self.assertIn('href="/frq/file/2025-ab-3/2025-ab-3.pdf"', html)
        self.assertIn("Part B: no calculator", html)
        self.assertIn('href="/frq/table/"', html)

    def test_unknown_question_404s(self):
        self.assertEqual(self.client.get("/frq/q/1999-ab-1/").status_code, 404)

    def test_files_are_served_with_their_types(self):
        r = self.client.get("/frq/file/2025-ab-3/q1.webp")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "image/webp")
        self.assertIn("max-age", r["Cache-Control"])
        r = self.client.get("/frq/file/2025-ab-3/2025-ab-3.pdf")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "application/pdf")

    def test_missing_or_foreign_files_404(self):
        for url in ("/frq/file/2025-ab-3/q9.webp",          # no such page
                    "/frq/file/2025-ab-3/2024-ab-2.pdf",    # another question's PDF under this one's URL
                    "/frq/file/2025-ab-3/manifest.json",    # not a page or a PDF
                    "/frq/file/1999-ab-1/q1.webp",          # no such question
                    "/frq/file/2025-ab-3/..%2fmanifest.json"):
            self.assertEqual(self.client.get(url).status_code, 404, url)

    def test_nav_link_present(self):
        for url in ("/frq/", "/exams/", "/course/"):
            html = self.html(url)
            self.assertIn('href="/frq/"', html, url)
            self.assertIn("AP FRQ Archive", html, url)
        nav = self.html("/frq/")
        self.assertIn('href="/frq/" class="on" aria-current="page">AP FRQ Archive', nav)

    @override_settings(FRQ_DIR=Path("/nonexistent/frq"))
    def test_no_archive_built_yet(self):
        html = self.html("/frq/")
        self.assertIn("The archive is empty on this server for now.", html)
        self.assertEqual(self.client.get("/frq/q/2025-ab-3/").status_code, 404)


class FRQLessonLinks(TestCase):
    def test_categories_for_topic(self):
        from course import frq
        with override_settings(FRQ_DIR=Path("/nonexistent/frq")):
            self.assertEqual(frq.categories_for_topic("4.2"), [])      # nothing built, no links
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "manifest.json").write_text(json.dumps({"questions": QUESTIONS, "problems": []}))
            with override_settings(FRQ_DIR=tmp):
                self.assertEqual([c["slug"] for c in frq.categories_for_topic("4.2")], ["particle-motion"])
                self.assertEqual([c["slug"] for c in frq.categories_for_topic("10.11")], ["bc-only"])
                self.assertEqual(frq.categories_for_topic("3.1"), [])
                q = frq.get("2019-bc-2")
                self.assertEqual(frq.lessons_for(q, {"9.7", "9.8", "9.9", "10.11"}), ["9.7", "9.8", "9.9"])
                self.assertEqual(frq.lessons_for(frq.get("2024-ab-2"), {"4.2", "8.2"}), ["4.2", "8.2"])
        finally:
            shutil.rmtree(tmp)
