from django.shortcuts import render
from rest_framework import generics, mixins, permissions, authentication
from .models import Category
from .serializers import CategorySerializer

class CategoryListRetrieveView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]



class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'


class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, partial=True, **kwargs)


class CategoryDestroyView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'