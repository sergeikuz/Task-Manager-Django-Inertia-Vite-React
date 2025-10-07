from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from inertia import location
from inertia import render as inertia_render

from backend.mixins import CustomLoginRequiredMixin
from backend.tasks.models import Task

from .forms import LabelForm
from .models import Label


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    
    def get(self, request):
        try:
            labels = Label.objects.all()
            return inertia_render(
                request,
                "Labels",
                props={"labels": labels}
            )
        except Exception as e:
            return inertia_render(
                request,
                "Error",
                props={"error": str(e)}
            )


class LabelCreateView(CustomLoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    success_message = _("Label created successfully")

    def get(self, request, *args, **kwargs):
        return inertia_render(request, "LabelsCreate", props={})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return location("/labels/")
        
        return inertia_render(
            request, 
            "LabelsCreate", 
            props={
                "error": f"{form.errors.as_text()}",
            }
        )


class LabelUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    success_message = _("Label updated successfully")

    def get(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=kwargs['pk'])
        return inertia_render(request, "LabelsUpdate", props={"label": label})

    def post(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=label)
        
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return location("/labels/")
        
        data = {"label": label, "error": f"{form.errors.as_text()}"}
        return inertia_render(request, "LabelsUpdate", props=data)


class LabelDeleteView(
    CustomLoginRequiredMixin,
    DeleteView
):
    model = Label
    success_delete_message = _("Label deleted successfully")
    message_warning_perm = _("Label is in use and cannot be deleted.")

    def get(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=kwargs['pk'])
        return inertia_render(request, "LabelsDelete", props={"label": label})
    
    def post(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=kwargs['pk'])
        
        if Task.objects.filter(labels=label).exists():
            messages.error(
                request, self.message_warning_perm
            )
            return location("/labels/")
        label.delete()
        messages.success(request, self.success_delete_message)
        return location("/labels/")
