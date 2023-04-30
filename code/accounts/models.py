
"""
Models for accounts app.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import Stop


class CustomUser(AbstractUser):
    """
    Custom user model that extends the built-in Django User model.
    """
    age = models.PositiveIntegerField(null=True, blank=True)


class Favorite(models.Model):
    """
    Model for a user's favorite bus stop.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)

    class Meta:
        """
        Meta Value for Favorite Class
        """
        unique_together = ('user', 'stop')

    def __str__(self):
        return f"{self.user} - {self.stop}"
