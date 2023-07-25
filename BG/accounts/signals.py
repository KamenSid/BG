from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AppUser
from BG.members.models import AppUserProfile


@receiver(post_save, sender=AppUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        AppUserProfile.objects.create(app_user=instance)
