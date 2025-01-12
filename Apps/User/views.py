from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CustomUser
from .serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


    @swagger_auto_schema(
        operation_description="Create a new user with email, password, and optional personal details.",
        request_body=UserSerializer,
        responses={
            201: UserSerializer(),
            400: openapi.Response('Bad Request - Invalid data or password weaknesses'),
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new user, admin-only access. A password validation will be performed before saving.
        """
        return super().post(request, *args, **kwargs)