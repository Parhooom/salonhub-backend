from rest_framework import serializers
from .models import Salon, DayOfWeek
from apps.salon_services.models import Service
from apps.salon_services.serializers import ServiceSerializer


class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek
        fields = ['id', 'day']


class SalonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = ['name', 'city', 'phone_number', 'email', 'description', 'price', 'address']

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class SalonSerializer(serializers.ModelSerializer):
    working_days = DayOfWeekSerializer(many=True, read_only=True)
    working_days_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DayOfWeek.objects.all(),
        required=False
    )
    # services = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Service.objects.all(),
    #     required=False
    # )
    services = ServiceSerializer(many=True, read_only=True)
    services_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.all(),
        required=False
    )

    class Meta:
        model = Salon
        fields = [
            'id', 'name', 'city', 'phone_number', 'email', 'description', 
            'price', 'address', 'working_days', 'working_days_ids',
            'working_hours_from', 'working_hours_to', 'services', 'services_ids', 
            'created_at', 'updated_at', 'pic_id', 'user'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user']


    def create(self, validated_data):
        working_days_ids = validated_data.pop('working_days_ids', [])
        services = validated_data.pop('services_ids', [])
    
        user = self.context['request'].user
        salon = Salon.objects.create(user=user, **validated_data)

        for day_id in working_days_ids:
            salon.working_days.add(day_id)

        for service in services:
            salon.services.add(service)

        return salon
