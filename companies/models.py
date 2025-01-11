from django.db import models
from django.contrib.auth.models import User
from credentials.models import Credential
from django_resized import ResizedImageField


class Company(models.Model):
    """
    Company model holding the company's listing details.
    Default logo image set.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = ResizedImageField(
        upload_to='images/',
        default='../default_logo_keaza8',
        size=[300, 300],
        quality=75,
        force_format="WEBP",
        blank=True,
    )
    name = models.CharField(max_length=250, unique=True)
    website_url = models.URLField(
        max_length=250,
        null=True,
        blank=True,
    )
    excerpt = models.CharField(max_length=500)
    description = models.TextField()
    credentials = models.ManyToManyField(Credential, blank=True)
    key_words = models.TextField(null=True, blank=True)
    street = models.CharField(max_length=25, null=True, blank=True)
    city = models.CharField(max_length=25, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    contact_name = models.CharField(max_length=40)
    contact_email = models.EmailField(unique=True, max_length=250)
    role = models.CharField(max_length=50)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'#{self.id} ({self.name})'
