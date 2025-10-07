from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from inertia import location
from inertia import render as inertia_render

from backend.mixins import CustomLoginRequiredMixin
from backend.tasks.models import Task

from .forms import StatusForm
from .models import Status


class StatusesIndexView(CustomLoginRequiredMixin, ListView):
    model = Status
    
    def get(self, request):
        try:
            statuses = Status.objects.all()
            return inertia_render(
                request,
                "Statuses",
                props={"statuses": statuses}
            )
        except Exception as e:
            return inertia_render(
                request,
                "Error",
                props={"error": str(e)}
            )


class StatusesCreateView(CustomLoginRequiredMixin, CreateView):
    form_class = StatusForm
    success_message = _("The status was created successfully")

    def get(self, request, *args, **kwargs):
        return inertia_render(request, "StatusesCreate", props={})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return location("/statuses/")
        
        return inertia_render(
            request, 
            "StatusesCreate", 
            props={
                "error": f"{form.errors.as_text()}",
            }
        )


class StatusesUpdateView(CustomLoginRequiredMixin, UpdateView):
    form_class = StatusForm
    model = Status
    success_message = _("The status was updated successfully")

    def get(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=kwargs['pk'])
        return inertia_render(
            request, 
            "StatusesUpdate", 
            props={"status": status}
        )

    def post(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=status)
        
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return location("/statuses/")
        
        data = {"status": status, "error": f"{form.errors.as_text()}"}
        return inertia_render(request, "StatusesUpdate", props=data)


class StatusesDeleteView(
    CustomLoginRequiredMixin,
    DeleteView
):
    model = Status
    success_delete_message = _("The status was deleted successfully")
    error_delete_message = _("Cannot delete status because it is in use.")

    def get(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=kwargs['pk'])
        return inertia_render(
            request, 
            "StatusesDelete", 
            props={"status": status}
        )
    
    def post(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=kwargs['pk'])
        
        if Task.objects.filter(status=status).exists():
            messages.error(
                request, self.error_delete_message
            )
            return location("/statuses/")
        status.delete()
        messages.success(request, self.success_delete_message)
        return location("/statuses/")
