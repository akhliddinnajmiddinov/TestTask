from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins, permissions, authentication
from .models import Product
from Category.models import Category
from .serializers import ProductSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProductListRetrieveView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of products. Optionally filter by category using category_id.",
        manual_parameters=[openapi.Parameter('category_id', openapi.IN_PATH, description="Category ID to filter products by", type=openapi.TYPE_INTEGER)],
        responses={200: ProductSerializer(many=True)}
    )
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

    @swagger_auto_schema(
        operation_description="Create a new product.",
        responses={201: ProductSerializer()},
        request_body=ProductSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_description="Retrieve a product by its ID.",
        responses={200: ProductSerializer()},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_description="Update an existing product.",
        responses={200: ProductSerializer()},
        request_body=ProductSerializer
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, partial=True, **kwargs)


class ProductDestroyView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_description="Delete a product by its ID.",
        responses={204: openapi.Response("No content")},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)