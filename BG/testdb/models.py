from embed_video.fields import EmbedVideoField

from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField()


class Replay(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    video = EmbedVideoField(User, blank=True, null=True)
    description = models.CharField(max_length=300)
    likes = models.ManyToManyField(User, related_name='liked_replays')
    game = models.CharField(max_length=30, default="None")

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author}"
