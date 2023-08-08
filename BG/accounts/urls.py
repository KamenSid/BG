from django.urls import path
from BG.accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login", views.LogInUserView.as_view(), name="log-in-user"),
    path("logout", views.LogoutView.as_view(), name="log-out-user"),
    path("register_user", views.RegisterUserView.as_view(), name="register-user"),
    path("pass_change", views.PasswordChangeView.as_view(), name="password-change"),
    path("pass_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password-change-done"),
]
