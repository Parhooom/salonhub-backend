from django.db import models
from django.contrib.auth import get_user_model

from apps.salons.models import Salon, DayOfWeek

TIME_SLOTS = (
    (1, '08:00-10:00'),
    (2, '10:00-12:00'),
    (3, '14:00-16:00'),
    (4, '16:00-18:00'),
    (5, '18:00-20:00'),
)

class TimeSlot(models.Model):
    time_range = models.IntegerField(choices=TIME_SLOTS, unique=True)

    def __str__(self) -> str:
        return self.get_time_range_display()


class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='bookings')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='bookings')
    day = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE, related_name='bookings')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='bookings')

    class Meta:
        unique_together = ('salon', 'day', 'time_slot')

    def __str__(self):
        return f"{self.user} - {self.salon} - {self.day} - {self.time_slot}"