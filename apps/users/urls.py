from django.urls import path
from .views import signup, verify_otp, login, logout


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('verifyotp/', verify_otp, name='verifyotp')
]
