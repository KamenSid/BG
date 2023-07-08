from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from BG.accounts.forms import AppUserCreationForm
from BG.members.models import AppUserProfile


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

        profile = AppUserProfile(app_user=user)  # Creating Profile for the User
        profile.save()
        messages.success(self.request, 'Registration success!')
        return response
