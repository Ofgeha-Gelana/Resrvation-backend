# Generated by Django 5.2.1 on 2025-05-13 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_remove_room_floor_number_room_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='image',
        ),
    ]
