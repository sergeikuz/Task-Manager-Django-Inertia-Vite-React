from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from backend.mixins import CustomLoginRequiredMixin

from .forms import CustomUserCreationForm
from .models import User

SUCCESS_URL = 'users:user_list'


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'general_form.html'
    success_url = reverse_lazy('login')
    message_success = _("The user has been successfully registered")
    form_title = _("Register User")
    form_submit = _("Register")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.message_success)
        return response


class UserUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'general_form.html'
    success_url = reverse_lazy(SUCCESS_URL)
    message_warning_perm = _("You don't have the rights to change it.")
    message_success = _("User successfully edited")
    message_warning_log = _("You are not registered ! Please log in")
    form_title = _("Edit User")
    form_submit = _("Edit")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.message_warning_log)
            return redirect('login')
        elif self.get_object() != request.user:
            messages.error(self.request, self.message_warning_perm)
            return redirect(SUCCESS_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.cleaned_data['password1']:
            self.object.set_password(form.cleaned_data['password1'])
            self.object.save()
        response = super().form_valid(form)
        messages.success(self.request, self.message_success)
        return response


class UserDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = User
    template_name = 'general_delete_form.html'
    success_url = reverse_lazy(SUCCESS_URL)
    message_warning_perm = _("You don't have the rights to change it.")
    message_success = _("User successfully deleted")
    message_perm = _(
        'It is not possible to delete a user because it is being used'
    )
    message_warning_log = _("You are not registered ! Please log in")
    form_title = _('Delete user')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.message_warning_log)
            return redirect('login')
        elif self.get_object() != request.user:
            messages.error(self.request, self.message_warning_perm)
            return redirect(SUCCESS_URL)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, self.message_success)
            return response
        except ProtectedError:
            messages.error(request, self.message_perm)
            return redirect(self.success_url)
