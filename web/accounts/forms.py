from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .antibot import HumanCheckMixin
from .models import CODE_ALPHABET, Classroom

USERNAME_HELP = "Letters, digits and . _ - only. You sign in with this."


def _clean_code(raw):
    code = "".join(ch for ch in (raw or "").upper() if ch in CODE_ALPHABET)
    return code, Classroom.objects.filter(code=code, open=True).first()


def email_in_use(email, exclude=None):
    qs = User.objects.filter(email__iexact=email, profile__email_verified=True)
    if exclude is not None:
        qs = qs.exclude(pk=exclude.pk)
    return qs.exists()


class NewAccountFields(forms.Form):
    """Username, display name and password, shared by every sign-up form."""
    display_name = forms.CharField(max_length=80, label="Your name")
    username = forms.RegexField(regex=r"^[\w.-]{3,30}$", max_length=30, help_text=USERNAME_HELP,
                                error_messages={"invalid": "Use 3 to 30 letters, digits, dots, dashes or underscores."},
                                widget=forms.TextInput(attrs={"autocomplete": "username", "autocapitalize": "none"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), min_length=8,
                               help_text="At least 8 characters. Not a common password.")

    def clean_display_name(self):
        name = " ".join(self.cleaned_data["display_name"].split())
        if not name:
            raise forms.ValidationError("Tell us what to call you.")
        return name

    def clean_username(self):
        u = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=u).exists():
            raise forms.ValidationError("That username is taken.")
        return u

    def clean(self):
        data = super().clean()
        if data.get("password"):
            try:
                validate_password(data["password"], User(username=data.get("username", ""),
                                                         first_name=data.get("display_name", "")))
            except forms.ValidationError as e:
                self.add_error("password", e)
        return data


class JoinForm(HumanCheckMixin, NewAccountFields):
    """A student makes an account with their teacher's class code. No email: the teacher can reset a
    forgotten password, and a student may add an address later in Account settings."""
    code = forms.CharField(max_length=6, label="Class code")
    field_order = ["code", "display_name", "username", "password"]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.fields["display_name"].help_text = "What your teacher will see. First name and last initial is plenty."

    def clean_code(self):
        code, self.classroom = _clean_code(self.cleaned_data["code"])
        if not self.classroom:
            raise forms.ValidationError("No open class has that code. Check it with your teacher.")
        return code


class JoinExistingForm(forms.Form):
    code = forms.CharField(max_length=6, label="Class code")

    def clean_code(self):
        code, self.classroom = _clean_code(self.cleaned_data["code"])
        if not self.classroom:
            raise forms.ValidationError("No open class has that code.")
        return code


class EmailField(forms.EmailField):
    def __init__(self, **kw):
        kw.setdefault("widget", forms.EmailInput(attrs={"autocomplete": "email"}))
        super().__init__(max_length=254, **kw)


class SignupForm(HumanCheckMixin, NewAccountFields):
    """Someone studying on their own (no class code)."""
    email = EmailField(help_text="We send a link to confirm it. Used for password resets, nothing else.")
    age_ok = forms.BooleanField(label="I am 13 or older",
                                error_messages={"required": "You need to be 13 or older to sign up on your own. "
                                                            "Ask your teacher for a class code instead."})
    field_order = ["display_name", "email", "username", "password", "age_ok"]

    def clean_email(self):
        e = self.cleaned_data["email"].strip()
        if email_in_use(e):
            raise forms.ValidationError("An account already uses that email. Sign in, or reset your password.")
        return e


class TeacherSignupForm(SignupForm):
    school = forms.CharField(max_length=120, required=False, label="School (optional)",
                             help_text="Helps us confirm you teach. Not shown to students.")
    field_order = ["display_name", "email", "school", "username", "password"]

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        del self.fields["age_ok"]
        self.fields["display_name"].help_text = "How students will see you, e.g. Ms. Rivera."


class NameForm(forms.Form):
    display_name = forms.CharField(max_length=80, label="Your name")

    def clean_display_name(self):
        name = " ".join(self.cleaned_data["display_name"].split())
        if not name:
            raise forms.ValidationError("Tell us what to call you.")
        return name


class EmailChangeForm(forms.Form):
    email = EmailField(label="New email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
                               label="Your password")

    def __init__(self, user, *a, **kw):
        self.user = user
        super().__init__(*a, **kw)

    def clean_password(self):
        if not self.user.check_password(self.cleaned_data["password"]):
            raise forms.ValidationError("That password isn't right.")
        return self.cleaned_data["password"]

    def clean_email(self):
        e = self.cleaned_data["email"].strip()
        if email_in_use(e, exclude=self.user):
            raise forms.ValidationError("Another account already uses that email.")
        return e


class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
                               label="Your password")
    sure = forms.BooleanField(label="I understand this can't be undone")

    def __init__(self, user, *a, **kw):
        self.user = user
        super().__init__(*a, **kw)

    def clean_password(self):
        if not self.user.check_password(self.cleaned_data["password"]):
            raise forms.ValidationError("That password isn't right.")
        return self.cleaned_data["password"]


class PasswordResetForm(HumanCheckMixin, auth_forms.PasswordResetForm):
    """Django's reset form, sending only to confirmed addresses (an unconfirmed one may not be the owner's)."""

    def get_users(self, email):
        return (u for u in super().get_users(email)
                if getattr(getattr(u, "profile", None), "email_verified", False) or u.is_superuser)
