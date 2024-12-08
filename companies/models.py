from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    """
    Company model.
    Default logo set
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(
        upload_to='images/', default='../default_logo_keaza8', 
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
    # credentials = ManyToManyField(credential, )
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{self.id} {self.title}'
