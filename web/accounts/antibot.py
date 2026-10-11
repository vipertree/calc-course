"""Bot checks for public forms, without a third-party CAPTCHA.

Two hidden fields: `website`, a honeypot that people never see and simple bots fill in, and `started`, a
signed timestamp from when the form was shown. A submit that fills the honeypot, comes back faster than a
person can type, or carries a missing, forged or day-old stamp is refused with a plain retry message.
"""
import time

from django import forms
from django.conf import settings
from django.core import signing

SALT = "calc.antibot"
RETRY = "Something went wrong with that form. Please wait a moment and try again."


def stamp(seconds_ago=0):
    return signing.dumps(int(time.time() - seconds_ago), salt=SALT)


class HoneypotInput(forms.TextInput):
    def __init__(self):
        super().__init__(attrs={"autocomplete": "off", "tabindex": "-1", "class": "hp-field"})


class HumanCheckMixin:
    """Mix into a forms.Form; render {{ form.website }} and {{ form.started }} inside a .hp wrapper."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["website"] = forms.CharField(required=False, label="Leave this empty", widget=HoneypotInput())
        self.fields["started"] = forms.CharField(required=False, widget=forms.HiddenInput())
        if not self.is_bound:
            self.initial["started"] = stamp()

    def clean(self):
        data = super().clean()
        if data.get("website"):
            raise forms.ValidationError(RETRY, code="bot")
        try:
            t = signing.loads(data.get("started") or "", salt=SALT)
        except signing.BadSignature:
            raise forms.ValidationError(RETRY, code="bot")
        age = time.time() - int(t)
        if age < settings.HUMAN_MIN_SECONDS or age > settings.HUMAN_MAX_SECONDS:
            raise forms.ValidationError(RETRY, code="bot")
        return data
