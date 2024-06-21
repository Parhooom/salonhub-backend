from rest_framework import serializers

from .models import Booking, TimeSlot

from apps.salons.models import Salon, DayOfWeek


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'salon', 'day', 'time_slot']

class CreateBookingSerializer(serializers.Serializer):
    salon_id = serializers.IntegerField()
    day_id = serializers.IntegerField()
    time_slot_id = serializers.IntegerField()

    def validate(self, data):
        user = self.context['request'].user
        salon_id = data.get('salon_id')
        day_id = data.get('day_id')
        time_slot_id = data.get('time_slot_id')

        if not Salon.objects.filter(id=salon_id).exists():
            raise serializers.ValidationError('Salon does not exist.')
        
        if not DayOfWeek.objects.filter(id=day_id).exists():
            raise serializers.ValidationError('Day does not exist.')

        if not TimeSlot.objects.filter(id=time_slot_id).exists():
            raise serializers.ValidationError('Time slot does not exist.')

        if Booking.objects.filter(salon_id=salon_id, day_id=day_id, time_slot_id=time_slot_id).exists():
            raise serializers.ValidationError('This time slot is already booked for the selected day and salon.')

        return data


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'time_range']




class SalonUSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = ['name']


class DayOfWeekUSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_display')

    class Meta:
        model = DayOfWeek
        fields = ['day', 'day_name']


class TimeSlotUSerializer(serializers.ModelSerializer):
    time_range = serializers.CharField(source='get_time_range_display')

    class Meta:
        model = TimeSlot
        fields = ['time_range']


class BookingUSerializer(serializers.ModelSerializer):
    salon = SalonUSerializer(read_only=True)
    day = DayOfWeekUSerializer(read_only=True)
    time_slot = TimeSlotUSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'salon', 'day', 'time_slot']