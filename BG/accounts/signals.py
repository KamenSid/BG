import os
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import AppUser
from BG.members.models import AppUserProfile, Replay


@receiver(post_save, sender=AppUser)
def create_user_profile(instance, created, **kwargs):
    if created:
        AppUserProfile.objects.create(app_user=instance)


@receiver(pre_delete, sender=Replay)
def delete_replay_file(instance, **kwargs):
    if instance.video_upload:
        file_path = instance.video_upload.path
        if os.path.exists(file_path):
            os.remove(file_path)
