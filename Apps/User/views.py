from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]