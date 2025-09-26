from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"placeholder": _("Password")}
        ),
        help_text=_("Password must contain at least 3 characters"),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Password confirmation")}
        ),
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name", "username", "password1", "password2"]
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "username": _("Username"),
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": _("First name")}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": _("Last name")}
            ),
            "username": forms.TextInput(
                attrs={"placeholder": _("Username")}
            ),
        }
        help_texts = {
            "username": _(
                "Required field. No more than 150 symbols. "
                "Only letters, digits and symbols @/./+/-/_."
            )
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 3:
            raise ValidationError(
                _(
                    "The entered password is too short."
                    " It must contain at least 3 characters."
                )
            )
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError(_("Passwords didn't match."))
        return password2
