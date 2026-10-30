from django.contrib.auth.models import User
from django.test import Client, TestCase

from accounts.models import Classroom, Profile

from . import setup as S
from .models import Dated, Setup


def teacher(name="t1"):
    u = User.objects.create_user(name, password="pw12345678")
    Profile.objects.create(user=u, role=Profile.TEACHER, display_name=name.title())
    return u


class SettingsTests(TestCase):
    def setUp(self):
        self.t = teacher()
        self.c = Classroom.objects.create(name="P3", teacher=self.t)

    def fresh(self):
        return Classroom.objects.get(pk=self.c.pk)          # drops the per-object setup cache

    def test_defaults_match_how_the_site_already_works(self):
        q = S.settings_for(self.c, "quiz", "2.5")
        self.assertEqual((q["where"], q["results"], q["attempts"]), ("site", "release", "one"))
        self.assertEqual(S.settings_for(self.c, "practice")["record"], "done")

    def test_class_then_unit_then_item_win_in_that_order(self):
        Setup.objects.create(classroom=self.c, kinds={"quiz": {"results": "now", "where": "paper"}},
                             units={"0": {"quiz": {"where": "off"}}})
        c = self.fresh()
        self.assertEqual(S.settings_for(c, "quiz", "2.5")["where"], "paper")
        self.assertEqual(S.settings_for(c, "quiz", "0.3")["where"], "off")
        d = Dated.objects.create(classroom=c, kind="quiz", ref="2.6", settings={"results": "due"})
        self.assertEqual(S.settings_for(c, "quiz", "2.6", d)["results"], "due")

    def test_practice_is_never_scored_for_correctness(self):
        self.assertEqual(S.clean("practice", {"record": "score"})["record"], "done")
        Setup.objects.create(classroom=self.c, kinds={"practice": {"record": "score"}})
        self.assertEqual(S.settings_for(self.fresh(), "practice")["record"], "done")

    def test_clean_drops_unknown_fields_and_values(self):
        self.assertEqual(S.clean("quiz", {"where": "moon", "results": "now", "x": "y"}), {"results": "now"})


class SetupPageTests(TestCase):
    def setUp(self):
        self.t = teacher()
        self.c = Classroom.objects.create(name="P3", teacher=self.t)
        self.web = Client()
        self.web.force_login(self.t)
        self.url = f"/teacher/class/{self.c.pk}/setup/"

    def test_page_shows_every_kind(self):
        page = self.web.get(self.url).content.decode()
        for name in S.NAMES.values():
            self.assertIn(name, page)

    def test_saving_the_table(self):
        self.web.post(self.url, {"notes.where": "paper", "notes.record": "mark", "quiz.results": "now",
                                 "show.grade": "on", "watch.inactive": "on", "watch.inactive_days": "7"})
        s = Setup.objects.get(classroom=self.c)
        self.assertEqual((s.kinds["notes"]["where"], s.kinds["notes"]["record"], s.kinds["quiz"]["results"]), ("paper", "mark", "now"))
        self.assertEqual((s.show["grade"], s.show["due_dates"], s.watch["inactive_days"]), (True, False, 7))

    def test_a_template_fills_every_row(self):
        self.web.post(self.url, {"apply_template": "paper"})
        s = Setup.objects.get(classroom=self.c)
        self.assertEqual((s.kinds["notes"]["where"], s.kinds["unittest"]["where"], s.template), ("paper", "paper", "paper"))
        self.assertEqual(set(s.kinds), set(S.KINDS))

    def test_another_teachers_class_is_not_found(self):
        other = Client()
        other.force_login(teacher("t2"))
        self.assertEqual(other.get(self.url).status_code, 404)
        self.assertEqual(other.post(self.url, {"quiz.results": "now"}).status_code, 404)

    def test_students_are_turned_away(self):
        s = User.objects.create_user("kid", password="pw12345678")
        Profile.objects.create(user=s, display_name="Kid")
        web = Client()
        web.force_login(s)
        self.assertEqual(web.get(self.url).status_code, 403)


import datetime as dt  # noqa: E402

from . import calendar as cal  # noqa: E402
from .models import NoSchool, StudentException  # noqa: E402


class CalendarTests(TestCase):
    def setUp(self):
        self.t = teacher()
        self.c = Classroom.objects.create(name="P3", teacher=self.t, course="AB")
        Setup.objects.create(classroom=self.c, kinds=S.template_kinds("full_schedule"))
        self.c = Classroom.objects.get(pk=self.c.pk)

    def local(self, moment):
        return moment.astimezone(cal.zone(self.c))

    def test_unit_topics_follow_the_course(self):
        ab, bc = cal.unit_topics(6, "AB"), cal.unit_topics(6, "BC")
        self.assertNotIn("6.15", ab)            # 6.14 BC is stored as 6.15
        self.assertIn("6.15", bc)
        self.assertLess(len(cal.unit_topics(10, "AB")), 1)   # Unit 10 is BC only

    def test_planning_skips_weekends_and_no_school(self):
        NoSchool.objects.create(classroom=self.c, day=dt.date(2026, 10, 21))     # a Wednesday
        rows = cal.plan_unit(self.c, 2, dt.date(2026, 10, 17))                   # a Saturday: starts Monday
        notes = sorted((d for d in rows if d.kind == "notes"), key=lambda d: d.opens)
        days = [self.local(d.opens).date() for d in notes]
        self.assertEqual(days[0], dt.date(2026, 10, 19))
        self.assertNotIn(dt.date(2026, 10, 21), days)
        self.assertTrue(all(d.weekday() < 5 for d in days))
        quiz = next(d for d in rows if d.kind == "quiz" and d.ref == notes[0].ref)
        self.assertEqual(self.local(quiz.due).date(), dt.date(2026, 10, 20))      # due the next class day
        self.assertEqual((self.local(quiz.due).hour, self.local(quiz.due).minute), (23, 59))
        self.assertTrue(any(d.kind == "unittest" for d in rows))

    def test_planning_only_dates_what_setup_schedules(self):
        Setup.objects.filter(classroom=self.c).update(kinds={})          # the defaults: nothing on a schedule
        c = Classroom.objects.get(pk=self.c.pk)
        self.assertEqual(cal.plan_unit(c, 2, dt.date(2026, 10, 19)), [])

    def test_a_snow_day_moves_later_work_one_class_day(self):
        cal.plan_unit(self.c, 2, dt.date(2026, 10, 19))
        fri = Dated.objects.get(classroom=self.c, kind="notes", ref="2.5")      # Fri Oct 23
        cal.shift(self.c, dt.date(2026, 10, 23), 1)
        fri.refresh_from_db()
        self.assertEqual(self.local(fri.opens).date(), dt.date(2026, 10, 26))   # over the weekend to Monday
        first = Dated.objects.get(classroom=self.c, kind="notes", ref="2.1")
        self.assertEqual(self.local(first.opens).date(), dt.date(2026, 10, 19))  # earlier work stays


class CalendarPageTests(TestCase):
    def setUp(self):
        self.t = teacher()
        self.c = Classroom.objects.create(name="P3", teacher=self.t)
        self.web = Client()
        self.web.force_login(self.t)
        self.url = f"/teacher/class/{self.c.pk}/calendar/"
        self.kid = User.objects.create_user("kid", password="pw12345678")
        Profile.objects.create(user=self.kid, display_name="Kid")
        self.c.enrollments.create(student=self.kid)

    def test_add_a_date_and_an_exception(self):
        self.web.post(self.url, {"action": "add", "kind": "quiz", "ref": "2.5"})
        d = Dated.objects.get(classroom=self.c, kind="quiz", ref="2.5")
        self.web.post(self.url, {"action": "item", "dated": d.pk, "opens": "2026-11-02T08:00", "due": "2026-11-03T23:59", "results": "now"})
        d.refresh_from_db()
        self.assertEqual(self.local_hm(d.due), (23, 59))
        self.assertEqual(d.settings, {"results": "now"})
        self.web.post(self.url, {"action": "exc_add", "dated": d.pk, "student": self.kid.pk, "due": "2026-11-06T23:59", "time_factor": "1.5"})
        e = StudentException.objects.get(dated=d)
        self.assertEqual((e.student, e.time_factor), (self.kid, 1.5))
        self.assertIn("Quiz 2.5", self.web.get(self.url + "?start=2026-11-02").content.decode())

    def local_hm(self, m):
        m = m.astimezone(cal.zone(self.c))
        return m.hour, m.minute

    def test_unknown_refs_and_other_classes_are_refused(self):
        self.web.post(self.url, {"action": "add", "kind": "quiz", "ref": "99.9"})
        self.assertFalse(Dated.objects.exists())
        other = Classroom.objects.create(name="P5", teacher=teacher("t2"))
        d = Dated.objects.create(classroom=other, kind="quiz", ref="2.5")
        self.web.post(self.url, {"action": "item_delete", "dated": d.pk})
        self.assertTrue(Dated.objects.filter(pk=d.pk).exists())

    def test_the_return_address_stays_on_the_page(self):
        r = self.web.post(self.url, {"action": "noschool", "day": "2026-11-26", "back": "//evil.example/"})
        self.assertEqual(r["Location"], self.url)
