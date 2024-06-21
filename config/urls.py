from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/services/', include('apps.salon_services.urls')),
    path('api/salons/', include('apps.salons.urls')),
    path('api/bookings/', include('apps.bookings.urls')),
]
