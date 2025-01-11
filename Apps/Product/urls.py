from django.urls import path
from .views import (
    ProductMixinView, ProductRetrieveAPIView, 
    ProductUpdateView, ProductDestroyView
    )


app_name = 'product'
urlpatterns = [
    path('', ProductMixinView.as_view(), name='product'), # for creating and listing categories
    path('<int:pk>/', ProductRetrieveAPIView.as_view(), name='retrieve'),
    path('<int:pk>/update',ProductUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', ProductDestroyView.as_view(), name='delete'),
]