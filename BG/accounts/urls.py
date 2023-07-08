from django.urls import path
from BG.accounts import views


urlpatterns = [
    path("login", views.LogInUserView.as_view(), name="log-in-user"),
    path("logout", views.LogoutView.as_view(), name="log-out-user"),
    path("register_user", views.RegisterUserView.as_view(), name="register-user"),
]