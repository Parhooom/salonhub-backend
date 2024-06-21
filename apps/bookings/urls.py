from django.urls import path
from . import views


urlpatterns = [
    path('save/', views.create_booking, name='save_booking'),
    path('getu/', views.get_all_user_bookings, name='get_all_user_bookings'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('available/<int:salon_id>/', views.get_available_times, name='get_available_times'),
]