from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView
from inertia import location
from inertia import render as inertia_render

from backend.labels.models import Label
from backend.mixins import CustomLoginRequiredMixin
from backend.statuses.models import Status
from backend.users.models import User

from .forms import TaskFilter, TaskForm
from .models import Task


class TaskListView(CustomLoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    
    def get(self, request):
        try:
            tasks = Task.objects.all()
            filterset = TaskFilter(request.GET, queryset=tasks, request=request)
            labels = Label.objects.all()
            users = User.objects.all()
            statuses = Status.objects.all()
            return inertia_render(
                request,
                "Tasks",
                props={
                    "tasks": filterset.qs,
                    "labels": labels,
                    "users": users,
                    "statuses": statuses,
                    "filter": dict(request.GET),
                },
            )
        except Exception as e:
            return inertia_render(
                request,
                "Error",
                props={"error": str(e)}
            )
    

class TaskCreateView(CustomLoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_message = _("Task created successfully")

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        users = User.objects.all()
        statuses = Status.objects.all()
        return inertia_render(
            request, 
            "TasksCreate", 
            props={
                "labels": labels,
                "users": users,
                "statuses": statuses,
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, self.success_message)
            return location("/tasks/")
        
        labels = Label.objects.all()
        users = User.objects.all()
        statuses = Status.objects.all()
        return inertia_render(
            request,
            "TasksCreate",
            props={
                "error": f"{form.errors.as_text()}",
                "labels": labels,
                "users": users,
                "statuses": statuses,
            },
        )
    

class TaskUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_message = _("Task updated successfully")

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        labels = Label.objects.all()
        users = User.objects.all()
        statuses = Status.objects.all()
        return inertia_render(
            request,
            "TasksUpdate",
            props={
                "task": task,
                "labels": labels,
                "users": users,
                "statuses": statuses,
            },
        )

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=task)
        
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return location("/tasks/")
        
        props = {"task": task, "error": f"{form.errors.as_text()}"}
        return inertia_render(request, "TasksUpdate", props=props)


class TaskDeleteView(
    CustomLoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Task
    success_delete_message = _("Task successfully deleted")
    permission_denied_message = _("A task can only be deleted by its author")

    def test_func(self):
        return self.request.user == self.get_object().owner

    def handle_no_permission(self):
        if not self.test_func():
            messages.error(
                self.request,
                self.permission_denied_message)
            return location("/tasks/")
        messages.error(self.request, self.permission_denied_message)
        return super().handle_no_permission()

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        if task.owner.id != request.user.id:
            messages.error(
                request, self.permission_denied_message
            )
            return location("/tasks/")
        return inertia_render(
            request,
            "TasksDelete",
            props={
                "task": task,
            },
        )

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        task.delete()
        messages.success(request, self.success_delete_message)
        return location("/tasks/")


class TaskDetailView(CustomLoginRequiredMixin, DetailView):
    model = Task

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        return inertia_render(request, "TasksShow", props={"task": task})