from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from inertia import location
from inertia import render as inertia_render

from .forms import UserLoginForm


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    success_message = _("You are logged in")

    def form_valid(self, form):
        self.request.user = form.get_user()
        login(self.request, form.get_user())
        messages.success(self.request, self.success_message)
        return location("/")

    def form_invalid(self, form):
        return inertia_render(
            self.request, 
            "Login", 
            props={
                "error": form.errors.as_text(),
                "form": form
            }
        )

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return location("/")
        return inertia_render(request, "Login", props={})


class CustomLogoutView(LogoutView):
    success_message = _("You are logged out")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        return inertia_render(request, "Index", {})
