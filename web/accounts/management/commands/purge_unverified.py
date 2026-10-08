from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = ("Delete self sign-ups (no class, not a teacher) whose email was never confirmed and that never did any "
            "work, after UNVERIFIED_ACCOUNT_DAYS. Class students are never touched: they sign up without email.")

    def add_arguments(self, p):
        p.add_argument("--dry-run", action="store_true")

    def handle(self, dry_run=False, **kw):
        cutoff = timezone.now() - timedelta(days=settings.UNVERIFIED_ACCOUNT_DAYS)
        qs = (User.objects.filter(date_joined__lt=cutoff, is_staff=False, is_superuser=False,
                                  profile__email_verified=False, profile__role="student", profile__full_access=False)
              .exclude(email="").filter(enrollments__isnull=True, responses__isnull=True, drafts__isnull=True,
                                        steps_done__isnull=True, quiz_attempts__isnull=True).distinct())
        names = list(qs.values_list("username", flat=True))
        if not dry_run:
            User.objects.filter(username__in=names).delete()
        self.stdout.write(f"{'would delete' if dry_run else 'deleted'} {len(names)} unconfirmed accounts")
