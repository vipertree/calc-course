from django.core.management.base import BaseCommand, CommandError

from accounts.admin import approve_teacher
from accounts.models import Profile


class Command(BaseCommand):
    help = "Approve a teacher-account request: approve_teacher <username>. With no username, list open requests."

    def add_arguments(self, p):
        p.add_argument("username", nargs="?")

    def handle(self, username=None, **kw):
        if not username:
            for p in Profile.objects.filter(teacher_requested__isnull=False).select_related("user"):
                ok = "confirmed" if p.email_verified else "email NOT confirmed"
                self.stdout.write(f"{p.user.username}\t{p.display_name}\t{p.user.email} ({ok})\t{p.school}")
            return
        p = Profile.objects.filter(user__username=username).select_related("user").first()
        if p is None or p.teacher_requested is None:
            raise CommandError(f"{username} has no open teacher request")
        if not approve_teacher(p):
            raise CommandError(f"{username} hasn't confirmed their email yet")
        self.stdout.write(f"{username} is now a teacher")
