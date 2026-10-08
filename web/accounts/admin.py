from django.contrib import admin, messages
from django.core.mail import send_mail

from .models import Classroom, Enrollment, Profile


def approve_teacher(profile):
    """Make a teacher-account request a teacher. Returns False when the email isn't confirmed yet."""
    if not profile.email_verified:
        return False
    profile.role = Profile.TEACHER
    profile.teacher_requested = None
    profile.save(update_fields=["role", "teacher_requested"])
    send_mail("Your teacher account is ready",
              f"Hi {profile.display_name},\n\nYour AP Calculus teacher account is approved. Sign in to create a class "
              "and get its join code.\n", None, [profile.user.email], fail_silently=True)
    return True


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "role", "email_verified", "teacher_requested", "school", "full_access")
    list_filter = ("role", "email_verified", "full_access")
    search_fields = ("display_name", "user__username", "user__email", "school")
    actions = ["approve_teacher_requests"]

    @admin.action(description="Approve teacher request")
    def approve_teacher_requests(self, request, queryset):
        done = skipped = 0
        for p in queryset.select_related("user").filter(teacher_requested__isnull=False):
            if approve_teacher(p):
                done += 1
            else:
                skipped += 1
        self.message_user(request, f"Approved {done}.", messages.SUCCESS)
        if skipped:
            self.message_user(request, f"Skipped {skipped}: email not confirmed yet.", messages.WARNING)


admin.site.register(Classroom)
admin.site.register(Enrollment)
