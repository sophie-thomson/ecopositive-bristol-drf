from django.db import models
from django.contrib.auth.models import User
from companies.models import Company


class Comment(models.Model):
    """
    Comment model, related to User and Company
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    approved = models.BooleanField(default=True)
    reported = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'"{self.content}" - {self.company}'
