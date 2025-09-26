from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .forms import UserLoginForm


class CustomLoginView(LoginView):
    authentication_form = UserLoginForm
    success_message = _("You are logged in")
    success_url = reverse_lazy("index")
    redirect_authenticated_user = True
    template_name = "general_form.html"
    error_message = _(
        "Please enter the correct username and password. "
        "Both fields can be case-sensitive."
    )
    form_title = _("Login")
    form_submit = _("Log in")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    success_message = _("You are logged out")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)


class IndexView(TemplateView):
    template_name = "index.html"
