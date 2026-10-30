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
