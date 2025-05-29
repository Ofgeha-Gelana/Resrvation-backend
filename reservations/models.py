# reservations/models.py
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    number_of_tables = models.PositiveIntegerField()
    address = models.CharField(max_length=255, null=True, blank=True)  # 👈 Add this line
    # image = models.ImageField(upload_to='rooms/')
    assigned_staff_email = models.EmailField()



    def __str__(self):
        return self.name

class Table(models.Model):
    room = models.ForeignKey(Room, related_name='tables', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='tables/')
    amenities = models.CharField(max_length=255, null=True, blank=True)  # 👈 Add this line


    def __str__(self):
        return f"{self.name} ({self.room.name})"

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    customer_name = models.CharField(max_length=100)
    refreshments=models.TextField(null=True)
    email = models.EmailField()
    number_of_guests = models.PositiveIntegerField()
    description=models.TextField(null=True)
    guest_email=models.TextField(help_text="Comma-separated list of emails",null=True)
    start_time = models.DateTimeField()    
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_email_list(self):
        return [email.strip() for email in self.guest_email.split(",") if email.strip()]