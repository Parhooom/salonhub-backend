from django.db import models
from django.contrib.auth import get_user_model

from apps.salon_services.models import Service


DAYS_OF_WEEK = (
    (1, 'Saturday'),
    (2, 'Sunday'),
    (3, 'Monday'),
    (4, 'Tuesday'),
    (5, 'Wednesday'),
    (6, 'Thursday'),
    (7, 'Friday'),
)


class DayOfWeek(models.Model):
    day = models.IntegerField(choices=DAYS_OF_WEEK, unique=True)

    def __str__(self):
        return self.get_day_display()


class Salon(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    address = models.CharField(max_length=255)
    working_days = models.ManyToManyField(DayOfWeek, related_name='salons')
    working_hours_from = models.TimeField()
    working_hours_to = models.TimeField()
    services = models.ManyToManyField(Service, related_name='salons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pic_id = models.CharField(max_length=200, null=True, blank=True, default='image')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='salons')

    def __str__(self):
        return self.name