from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins, permissions, authentication
from .models import Product
from Category.models import Category
from .serializers import ProductSerializer

class ProductListRetrieveView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        # listing all products of category if category_id is given
        category_id = kwargs.get('category_id')
        if category_id is not None:
            category = get_object_or_404(Category, pk=category_id)
            self.queryset = self.queryset.filter(category=category)
        return self.list(request, *args, **kwargs)


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]



class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, partial=True, **kwargs)


class ProductDestroyView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'