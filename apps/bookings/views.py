from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import CreateBookingSerializer, BookingSerializer, TimeSlotSerializer, BookingUSerializer

from .models import Booking, TimeSlot
from apps.salons.models import Salon, DayOfWeek



@extend_schema(
    summary='Create a new booking',
    description='Create a new booking for a user in a specific salon, day and time',
    request=CreateBookingSerializer,
    responses={
        201: BookingSerializer,
        400: OpenApiResponse(description='Invalid input data')
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    serializer = CreateBookingSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        salon = Salon.objects.get(id=serializer.validated_data['salon_id'])
        day = DayOfWeek.objects.get(id=serializer.validated_data['day_id'])
        time_slot = TimeSlot.objects.get(id=serializer.validated_data['time_slot_id'])

        booking = Booking.objects.create(
            user=request.user,
            salon=salon,
            day=day,
            time_slot=time_slot
        )

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(
    summary='Get all booking for the authenticated user',
    description='Retrieve a list of all bookings made by the authenticated user',
    responses={
        200: BookingUSerializer(many=True),
        401: OpenApiResponse(description='Authentication credentials were not provided or invalid')
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    serializer = BookingUSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Delete a booking",
    description="Delete a specific booking made by the authenticated user.",
    responses={
        204: OpenApiResponse(description='Booking deleted successfully'),
        404: OpenApiResponse(description='Booking not found or not authorized to delete this booking')
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found or not authorized to delete this booking.'}, status=status.HTTP_404_NOT_FOUND)
    
    booking.delete()
    return Response({'message': 'Booking deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Get available times for a salon",
    description="Retrieve available time slots for a specific salon.",
    responses={
        200: OpenApiResponse(description='A dictionary with available time slots', examples={
            'application/json': {
                'Saturday': [{'id': 1, 'time_range': '8:00-10:00'}],
                'Sunday': [{'id': 2, 'time_range': '10:00-12:00'}],
            }
        }),
        404: OpenApiResponse(description='Salon does not exist')
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_times(request, salon_id):
    try:
        salon = Salon.objects.get(id=salon_id)
    except Salon.DoesNotExist:
        return Response({'error': 'Salon does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    available_times = {}
    working_days = salon.working_days.all()
    time_slots = TimeSlot.objects.all()

    for day in working_days:
        booked_time_slots = Booking.objects.filter(salon=salon, day=day).values_list('time_slot_id', flat=True)
        available_time_slots = time_slots.exclude(id__in=booked_time_slots)
        available_times[day.get_day_display()] = TimeSlotSerializer(available_time_slots, many=True).data

    return Response(available_times, status=status.HTTP_200_OK)

