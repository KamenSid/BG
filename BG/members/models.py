from django.db import models

from BG.accounts.models import AppUser
from BG.testdb.models import Replay


class AppUserProfile(models.Model):
    app_user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, null=True, blank=True)
    steam_name = models.CharField(max_length=100, null=True, blank=True)
    steam_id = models.CharField(null=True, blank=True)
    picture = models.ImageField(upload_to='profile_pictures/')

    def save(self, *args, **kwargs):

        if not self.username:
            self.username = self.app_user.email.split('@')[0]
        super().save(*args, **kwargs)
