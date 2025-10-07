from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DeleteView, ListView, UpdateView
from inertia import location
from inertia import render as inertia_render

from backend.mixins import CustomLoginRequiredMixin
from backend.tasks.models import Task

from .forms import CustomUserCreationForm
from .models import User


class UserListView(ListView):
    model = User
    
    def get(self, request):
        users = User.objects.all().order_by("id")
        return inertia_render(
            request,
            "Users",
            props={"users": users},
        )


class UserCreateView(View):
    form_class = CustomUserCreationForm
    message_success = _("The user has been successfully registered")

    def get(self, request, *args, **kwargs):
        return inertia_render(request, "Registration", props={})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.message_success)
            return location("/login/")
        
        return inertia_render(
            request, 
            "Registration", 
            props={
                "error": f"{form.errors.as_text()}",
            }
        )


class UserUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    message_warning_perm = _("You don't have the rights to change it.")
    message_success = _("User successfully edited")
    message_warning_log = _("You are not registered ! Please log in")

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        return inertia_render(request, "UsersUpdate", props={"user": user})

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=user)

        if form.is_valid():
            user_obj = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            if password:
                user_obj.set_password(password)
            user_obj.save()
            messages.success(request, self.message_success)
            return location("/users/")

        data = {
            "user": user,
            "error": f"{form.errors.as_text()}"
        }
        return inertia_render(request, "UsersUpdate", props=data)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.message_warning_log)
            return location('/login/')
        user = get_object_or_404(User, pk=kwargs['pk'])
        if user != request.user:
            messages.error(request, self.message_warning_perm)
            return location('/users/')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = User
    message_warning_perm = _("You don't have the rights to change it.")
    message_success = _("User successfully deleted")
    message_perm = _(
        'It is not possible to delete a user because it is being used'
    )
    message_warning_log = _("You are not registered ! Please log in")

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        if user != request.user:
            messages.error(request, self.message_warning_perm)
            return location("/users/")
        return inertia_render(request, "UsersDelete", props={"user": user})

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        if Task.objects.filter(executor=user).exists():
            messages.error(request, self.message_perm)
            return location("/users/")
        user.delete()
        messages.success(request, self.message_success)
        return location("/users")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.message_warning_log)
            return location('/login/')
        user = get_object_or_404(User, pk=kwargs['pk'])
        if user != request.user:
            messages.error(request, self.message_warning_perm)
            return location('/users/')
        return super().dispatch(request, *args, **kwargs)