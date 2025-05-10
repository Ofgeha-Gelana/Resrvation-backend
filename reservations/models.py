# reservations/models.py
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    number_of_tables = models.PositiveIntegerField()
    floor_number = models.IntegerField()
    image = models.ImageField(upload_to='rooms/')
    assigned_staff_email = models.EmailField()

    def __str__(self):
        return self.name

class Table(models.Model):
    room = models.ForeignKey(Room, related_name='tables', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='tables/')

    def __str__(self):
        return f"{self.name} ({self.room.name})"

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    number_of_guests = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.table.name}"