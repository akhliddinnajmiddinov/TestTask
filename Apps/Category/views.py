from django.shortcuts import render
from rest_framework import generics, mixins, permissions, authentication
from .models import Category
from .serializers import CategorySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CategoryListRetrieveView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of categories.",
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description="Create a new category.",
        responses={201: CategorySerializer()},
        request_body=CategorySerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'


    @swagger_auto_schema(
        operation_description="Retrieve a category by its ID.",
        responses={200: CategorySerializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'


    @swagger_auto_schema(
        operation_description="Update an existing category.",
        responses={200: CategorySerializer()},
        request_body=CategorySerializer
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, partial=True, **kwargs)


class CategoryDestroyView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_description="Delete a category by its ID.",
        responses={204: openapi.Response("No content")},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)