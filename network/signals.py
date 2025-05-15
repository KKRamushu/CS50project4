from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User_Profile
from django.contrib.auth.models import User

@receiver(post_save, sender = User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)
    else:
        instance.profile.save()