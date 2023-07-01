from django.urls import path
from BG.members import views

urlpatterns = [
    path("", views.upload_replay, name="upload-replay"),
    path("update/<int:replay_pk>", views.update_replay, name="update-replay"),
    path("like/<int:replay_pk>", views.like_replay, name="like-replay"),
]
