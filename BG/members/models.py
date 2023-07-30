from django.contrib.auth import get_user_model
from django.db import models
from BG.testdb.models import Replay

AppUser = get_user_model()


class Guild(models.Model):
    GUILD_NAME_MAX_LENGTH = 100

    name = models.CharField(max_length=GUILD_NAME_MAX_LENGTH, null=False, blank=False, unique=True)
    leader = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='leader')
    members = models.ManyToManyField(AppUser, related_name='guild')
    banner = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class AppUserProfile(models.Model):
    USERNAME_MAX_LENGTH = 50
    STEAM_NAME_MAX_LENGTH = 100

    app_user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=USERNAME_MAX_LENGTH, null=True, blank=True)
    steam_name = models.CharField(max_length=STEAM_NAME_MAX_LENGTH, null=True, blank=True)
    steam_id = models.CharField(null=True, blank=True)
    picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    guild = models.ForeignKey(Guild, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.app_user.email.split('@')[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User: {self.username} | Guild: {self.guild}"


class Like(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING)
    replay = models.ForeignKey(Replay, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.replay}"
