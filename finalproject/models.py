from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class SavedEvents(models.Model):
    name = models.CharField(max_length=64, default='')
    image = models.CharField(max_length=64, default='')
    date = models.CharField(max_length=64, default='')
    time = models.CharField(max_length=64, default='')
    venue = models.CharField(max_length=64, default='')
    city = models.CharField(max_length=64, default='')
    state = models.CharField(max_length=64, default='')
    address = models.CharField(max_length=64, default='')
    link = models.CharField(max_length=128, default='')
