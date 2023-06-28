from django.db import models
from django.contrib.auth.models import User
from BG.testdb.models import Replay


class Like(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    given_to = models.ManyToManyField(Replay)

    def __str__(self):
        return f"{self.id} - {self.owner}"
