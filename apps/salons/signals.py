from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import DayOfWeek, DAYS_OF_WEEK


@receiver(post_migrate)
def create_days_of_week(sender, **kwargs):
    if sender.name == 'apps.salons':
        for key, value in DAYS_OF_WEEK:
            DayOfWeek.objects.get_or_create(day=key)
