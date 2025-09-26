from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from backend.mixins import CustomLoginRequiredMixin

from .forms import StatusForm
from .models import Status

SUCCESS_URL = "statuses:statuses_index"


class StatusesIndexView(CustomLoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/statuses_index.html"
    context_object_name = "statuses"


class StatusesCreateView(CustomLoginRequiredMixin, CreateView):
    form_class = StatusForm
    template_name = 'general_form.html'
    success_url = reverse_lazy(SUCCESS_URL)
    success_message = _("The status was created successfully")
    form_title = _("Create status")
    form_submit = _("Create")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class StatusesUpdateView(CustomLoginRequiredMixin, UpdateView):
    form_class = StatusForm
    model = Status
    template_name = 'general_form.html'
    success_url = reverse_lazy(SUCCESS_URL)
    success_message = _("The status was updated successfully")
    form_title = _("Edit stutus")
    form_submit = _("Edit")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class StatusesDeleteView(
    CustomLoginRequiredMixin,
    DeleteView
):
    model = Status
    template_name = 'general_delete_form.html'
    success_url = reverse_lazy(SUCCESS_URL)
    success_delete_message = _("The status was deleted successfully")
    error_delete_message = _("Cannot delete status because it is in use.")
    form_title = _("Delete status")

    def form_valid(self, form):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(self.request, self.success_delete_message)
        except ValidationError:
            messages.error(self.request, self.error_delete_message)
        return redirect(self.success_url)
