from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from backend.mixins import CustomLoginRequiredMixin

from .forms import LabelForm
from .models import Label

SUCCESS_URL = "labels:labels_index"


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/labels_index.html"
    context_object_name = "labels"


class LabelCreateView(CustomLoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'general_form.html'
    success_url = reverse_lazy(SUCCESS_URL)
    success_message = _("Label created successfully")
    form_title = _("Create label")
    form_submit = _("Create")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class LabelUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy(SUCCESS_URL)
    template_name = 'general_form.html'
    success_message = _("Label updated successfully")
    form_title = _("Edit label")
    form_submit = _("Edit")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class LabelDeleteView(
    CustomLoginRequiredMixin,
    DeleteView
):
    model = Label
    template_name = 'general_delete_form.html'
    success_url = reverse_lazy(SUCCESS_URL)
    success_delete_message = _("Label deleted successfully")
    message_warning_perm = _("Label is in use and cannot be deleted.")
    form_title = _("Delete label")

    def form_valid(self, form):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(self.request, self.success_delete_message)
        except ValidationError:
            messages.error(self.request, self.message_warning_perm)
        return redirect(self.success_url)
