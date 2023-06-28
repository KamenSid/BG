from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from BG.forms import LogInUser


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.success(request, "You are not logged in.")
            form = LogInUser()
            context = {
                "form": form,
                "username": request.user.username
            }
            return render(request, "accounts/login_user.html", context)
    else:
        form = LogInUser()
        context = {
            "form": form,
            "username": "Unknown"
        }
        return render(request, "accounts/login_user.html", context)


def logout_user(request):
    logout(request)
    return redirect("index")


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
