from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    election_id = models.CharField(max_length=100, blank=True, null=True)


class Nominee(models.Model):
    name = models.CharField(max_length=100)
    election_id = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()

class Vote(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    nominee = models.ForeignKey(Nominee, on_delete=models.CASCADE)
    election_id = models.CharField(max_length=100)

    class Meta:
        # Enforce uniqueness of votes based on the user
        unique_together = ('user', 'election_id')
