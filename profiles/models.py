from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    image = ResizedImageField(
        upload_to='images/',
        default='../default_profile_hcui3f',
        size=[300, 300],
        quality=75,
        force_format="WEBP",
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
