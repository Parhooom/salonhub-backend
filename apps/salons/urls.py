from django.urls import path
from . import views


urlpatterns = [
    path('image/<str:salon_id>/', views.serve_image, name='serve_image'),
    path('save/', views.create_salon, name='save_salon'),
    path('get/<int:salon_id>/', views.get_salon, name='get_salon'),
    path('get/', views.get_all_salons, name='get_all_salons'),
    path('getu/', views.get_all_user_salons, name='get_all_user_salons'),
    path('update/<int:salon_id>/', views.update_salon, name='update_salon'),
    path('delete/<int:salon_id>/', views.delete_salon, name='delete_salon'),
]
