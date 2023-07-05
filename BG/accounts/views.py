from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


class LogInUserView(LoginView):
    template_name = 'accounts/login_user.html'


class LogOutUser(LogoutView):
    next_page = 'index'


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration success!")
            return redirect("index")
    else:
        form = UserCreationForm()

    context = {
        "username": "Unknown",
        "form": form
    }
    return render(request, "accounts/register_user.html", context)
