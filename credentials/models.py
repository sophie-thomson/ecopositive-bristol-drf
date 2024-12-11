from django.db import models
from django.contrib.auth.models import User

CREDENTIAL_GROUPS = [
    ("Eco-Conscious Approach", "Eco-Conscious Approach"),
    ("Membership / Accreditation", "Membership / Accreditation"),
    ("Socially Responsible", "Socially Responsible"),
    (
        "Sustainable Production / Materials",
        "Sustainable Production / Materials"
    ),
]


class Credential(models.Model):
    """
    Credential model, related to 'Company'.
    A credential can be assigned to many companies, and one
    company can have multiple credentials.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=True)
    group = models.CharField(choices=CREDENTIAL_GROUPS, max_length=40)
    link = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['group']

    def __str__(self):
        return f'{self.name}, ({self.group})'
