from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import Stop

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'stop')
    
    def __str__(self):
        return f"{self.user.username} - {self.stop.stop_name}"
