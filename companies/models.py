from django.db import models
from django.contrib.auth.models import User
from credentials.models import Credential


class Company(models.Model):
    """
    Company model holding the company's listing details.
    We need the related_name attribute so that django can differentiate.
    between the 'owner' of the listing and 'company_owner' who both are
    User model instances.
    Default logo image set.
    """
    owner = models.ForeignKey(
        User,
        related_name='listing_owner',
        on_delete=models.CASCADE
    )
    company_owner = models.ForeignKey(
        User,
        related_name='company_owner',
        on_delete=models.CASCADE
    )
    logo = models.ImageField(
        upload_to='images/',
        default='../default_logo_keaza8',
        blank=True
    )
    name = models.CharField(max_length=250, unique=True)
    website_url = models.URLField(
        max_length=250,
        null=True,
        blank=True
    )
    excerpt = models.CharField(max_length=500)
    description = models.TextField()
    credentials = models.ManyToManyField(Credential)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'#{self.id} - {self.name}'
