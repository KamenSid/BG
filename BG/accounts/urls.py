from django.urls import path
from BG.accounts import views


urlpatterns = [
    path("login", views.login_user, name="log-in-user"),
    path("logout", views.logout_user, name="log-out-user"),
    path("register_user", views.register_user, name="register-user"),
]