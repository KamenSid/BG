from django.urls import path

from BG.testdb import views

urlpatterns = (
    path('', views.test_view, name="test_db_base"),
    path("delete/<int:pk>", views.ReplayDeleteView.as_view(), name="replay-delete"),
    path("details/<int:pk>", views.ReplayDetailsView.as_view(), name="replay-details"),
)
