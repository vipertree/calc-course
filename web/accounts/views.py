from django import forms
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.shortcuts import redirect, render

from .models import CODE_ALPHABET, Classroom, Enrollment, Profile


class JoinForm(forms.Form):
    code = forms.CharField(max_length=6, label="Class code")
    display_name = forms.CharField(max_length=80, label="Your name", help_text="What your teacher will see")
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)

    def clean_code(self):
        code = "".join(ch for ch in self.cleaned_data["code"].upper() if ch in CODE_ALPHABET)
        c = Classroom.objects.filter(code=code, open=True).first()
        if not c:
            raise forms.ValidationError("No open class has that code. Check it with your teacher.")
        self.classroom = c
        return code

    def clean_username(self):
        u = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=u).exists():
            raise forms.ValidationError("That username is taken.")
        return u

    def clean_password(self):
        validate_password(self.cleaned_data["password"])
        return self.cleaned_data["password"]


class JoinExistingForm(forms.Form):
    code = forms.CharField(max_length=6, label="Class code")

    def clean_code(self):
        code = "".join(ch for ch in self.cleaned_data["code"].upper() if ch in CODE_ALPHABET)
        c = Classroom.objects.filter(code=code, open=True).first()
        if not c:
            raise forms.ValidationError("No open class has that code.")
        self.classroom = c
        return code


def join(request):
    if request.user.is_authenticated:
        form = JoinExistingForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            Enrollment.objects.get_or_create(classroom=form.classroom, student=request.user)
            return redirect("home")
        return render(request, "accounts/join.html", {"form": form, "existing": True})
    form = JoinForm(request.POST or None, initial={"code": request.GET.get("code", "")})
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            u = User.objects.create_user(form.cleaned_data["username"], password=form.cleaned_data["password"])
            Profile.objects.create(user=u, role=Profile.STUDENT, display_name=form.cleaned_data["display_name"].strip())
            Enrollment.objects.create(classroom=form.classroom, student=u)
        login(request, u)
        return redirect("home")
    return render(request, "accounts/join.html", {"form": form})
