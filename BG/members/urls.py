from django.urls import path, include
from BG.members import views

urlpatterns = [
    path("upload/", views.UploadReplayView.as_view(), name="upload-replay"),
    path("update/<int:replay_pk>/", views.update_replay, name="update-replay"),
    path("like/<int:replay_pk>/", views.like_replay, name="like-replay"),
    path("profile/<int:pk>/", include([
        path("update/", views.UpdateProfileView.as_view(), name="update-profile")])
    ),
    path("guild/", views.GuildDetailsView.as_view(), name="guild-details")
]
