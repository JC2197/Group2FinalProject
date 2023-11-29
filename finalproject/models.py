from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class SavedEvents(models.Model):
    event_name = ""
    event_image = ""
    event_date = ""
    event_time = ""
    venue_name = ""
    venue_city = ""
    venue_state = ""
    venue_address = ""
    ticket_link = ""
