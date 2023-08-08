from django.urls import path, include
from BG.members import views


urlpatterns = [

    path("delete/<int:pk>", views.ReplayDeleteView.as_view(), name="replay-delete"),
    path("details/<int:pk>", views.ReplayDetailsView.as_view(), name="replay-details"),

    path("upload/", views.UploadReplayView.as_view(), name="upload-replay"),
    path("update/<int:pk>/", views.UpdateReplayView.as_view(), name="update-replay"),
    path("like/<int:replay_pk>/", views.like_replay, name="like-replay"),
    path("profile/<int:pk>/", include([
        path('', views.ProfileView.as_view(), name="profile-details"),
        path("update/", views.UpdateProfileView.as_view(), name="update-profile"),
        path('delete/', views.ProfileDeleteView.as_view(), name='profile-delete')])
         ),
    path("guild/", include([
        path("details/<int:pk>", views.GuildDetailsView.as_view(), name="guild-details"),
        path("create/", views.GuildCreate.as_view(), name="guild-create"),
        path("edit/", views.EditGuildView.as_view(), name="guild-edit"),
        path("addmembers/", views.guild_add_members, name="guild-add-members")]),
         )
]
