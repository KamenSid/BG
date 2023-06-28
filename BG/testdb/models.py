from embed_video.fields import EmbedVideoField

from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()


class Replay(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    video = EmbedVideoField(User, blank=True, null=True)
    description = models.CharField(max_length=300)
    likes_count = models.IntegerField
    game = models.CharField(max_length=30, default="None")

    def __str__(self):
        return f"{self.title} by {self.author}"
