from .models import Service
from .serializers import ServiceSerializer

# from users.permissions import IsOwner

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]


        return super().get_permissions()
    

    