# reservations/admin.py
from django.contrib import admin
from .models import Room, Table, Reservation

admin.site.register(Room)
admin.site.register(Table)
admin.site.register(Reservation)