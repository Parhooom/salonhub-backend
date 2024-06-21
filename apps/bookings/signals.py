from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import TimeSlot, TIME_SLOTS

@receiver(post_migrate)
def create_time_slots(sender, **kwargs):
    if sender.name == 'apps.bookings':
       for key, value in TIME_SLOTS:
            TimeSlot.objects.get_or_create(time_range=key)
