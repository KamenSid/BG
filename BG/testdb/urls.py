from django.urls import path

from BG.testdb import views

urlpatterns = (
    path('', views.test_view, name="test_db_base"),
    path('delete/<int:pk>', views.delete_replay, name="delete")
)
