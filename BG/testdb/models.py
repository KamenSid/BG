from django.contrib.auth import get_user_model
from embed_video.fields import EmbedVideoField
from django.db import models
from django.contrib.auth.models import User
from BG import settings

user_model = get_user_model()


class Replay(models.Model):
    TITLE_MAX_LENGTH = 30
    DESCRIPTION_MAX_LENGTH = 300
    GAME_MAX_LENGTH = 30

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    author = models.ForeignKey(user_model, null=True, blank=True, on_delete=models.CASCADE)
    video_url = EmbedVideoField(settings.AUTH_USER_MODEL, blank=True, null=True)
    video_upload = models.FileField(upload_to='replays/', blank=True, null=True)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH, null=True, blank=True)
    game = models.CharField(max_length=GAME_MAX_LENGTH, default="None")

    class Meta:
        ordering = ['title']

        permissions = [
            ('can_add_replay', 'Can add replay'),
            ('can_change_replay', 'Can change replay'),
            ('can_delete_replay', 'Can delete replay'),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"


class Comment(models.Model):
    MAX_COLOR_LENGTH = 10

    author = models.ForeignKey(user_model, on_delete=models.CASCADE)
    replay = models.ForeignKey(Replay, on_delete=models.CASCADE)
    content = models.TextField()
    background_color = models.CharField(max_length=MAX_COLOR_LENGTH, null=True, blank=True)
    font_color = models.CharField(max_length=MAX_COLOR_LENGTH, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
