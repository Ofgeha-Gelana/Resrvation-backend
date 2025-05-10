
# reservations/apps.py (enable signals)
from django.apps import AppConfig

class ReservationsConfig(AppConfig):
    name = 'reservations'

    def ready(self):
        import reservations.signals
