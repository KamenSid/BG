from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from BG.accounts.forms import AppUserCreationForm, CustomPasswordChangeForm


class LogInUserView(LoginView):
    template_name = 'accounts/login_user.html'


class LogOutUser(LogoutView):
    next_page = 'index'


class RegisterUserView(CreateView):
    form_class = AppUserCreationForm
    template_name = 'accounts/register_user.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)

        email = form.cleaned_data['email']  # Logging in after registration
        password = form.cleaned_data['password1']
        user = authenticate(username=email, password=password)
        login(self.request, user)

        messages.success(self.request, 'Registration success!')
        return response


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    form_class = CustomPasswordChangeForm
    success_url = '/'
