from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class UsernameOrEmailBackend(ModelBackend):
    """Sign in with a username, or with the email address of an account whose email is confirmed."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username and "@" in username:
            u = (User.objects.filter(email__iexact=username.strip(), profile__email_verified=True)
                 .order_by("pk").first())
            if u is None:
                User().set_password(password)       # same work as a real check, so timing says nothing
                return None
            username = u.get_username()
        return super().authenticate(request, username=username, password=password, **kwargs)
