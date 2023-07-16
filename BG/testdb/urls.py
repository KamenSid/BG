from django.urls import path

from BG.testdb import views

urlpatterns = (
    path('profile/<int:pk>', views.ProfileView.as_view(), name="profile-details"),
    path("delete/<int:pk>", views.ReplayDeleteView.as_view(), name="replay-delete"),
    path("details/<int:pk>", views.ReplayDetailsView.as_view(), name="replay-details"),
    path("search/", views.SearchView.as_view(), name="search"),
)
