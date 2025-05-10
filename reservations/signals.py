# reservations/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reservation
from django.core.mail import send_mail

@receiver(post_save, sender=Reservation)
def send_staff_notification(sender, instance, created, **kwargs):
    if created:
        room = instance.table.room
        subject = f"New Reservation for {instance.table.name}"
        message = f"{instance.customer_name} has booked table {instance.table.name} from {instance.start_time} to {instance.end_time}."
        send_mail(subject, message, 'noreply@yourdomain.com', [room.assigned_staff_email])
