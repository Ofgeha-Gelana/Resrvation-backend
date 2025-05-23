from django.contrib.auth.models import User
from django.db import models

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_room = models.ForeignKey('reservations.Room', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
