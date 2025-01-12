from django.urls import path
from .views import (
    ProductListRetrieveView, ProductCreateAPIView, ProductRetrieveAPIView, 
    ProductUpdateView, ProductDestroyView
    )


app_name = 'product'
urlpatterns = [
    path('', ProductListRetrieveView.as_view(), name='list'),
    path('category/<int:category_id>/', ProductListRetrieveView.as_view(), name='list-category-products'),
    path('create/', ProductCreateAPIView.as_view(), name='create'),
    path('<int:pk>/', ProductRetrieveAPIView.as_view(), name='retrieve'),
    path('<int:pk>/update',ProductUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', ProductDestroyView.as_view(), name='destroy'),
]