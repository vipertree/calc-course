from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from accounts.models import Classroom, Profile


class Command(BaseCommand):
    help = "Create a teacher account, optionally with a first class: create_teacher adder 'Adder Oaks' pw --class 'Period 3'"

    def add_arguments(self, p):
        p.add_argument("username")
        p.add_argument("display_name")
        p.add_argument("password")
        p.add_argument("--class", dest="classname")
        p.add_argument("--course", default="AB", choices=["AB", "BC"])

    def handle(self, username, display_name, password, classname=None, course="AB", **kw):
        if User.objects.filter(username=username).exists():
            raise CommandError(f"{username} already exists")
        u = User.objects.create_user(username, password=password)
        Profile.objects.create(user=u, role=Profile.TEACHER, display_name=display_name)
        self.stdout.write(f"teacher {username} created")
        if classname:
            c = Classroom.objects.create(name=classname, teacher=u, course=course)
            self.stdout.write(f"class {c.name}: join code {c.code}")
