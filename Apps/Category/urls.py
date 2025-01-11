from django.urls import path
from .views import (
    CategoryMixinView, CategoryRetrieveAPIView, 
    CategoryUpdateView, CategoryDestroyView
    )


app_name = 'category'
urlpatterns = [
    path('', CategoryMixinView.as_view(), name='category'), # for creating and listing categories
    path('<int:pk>/', CategoryRetrieveAPIView.as_view(), name='retrieve'),
    path('<int:pk>/update', CategoryUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', CategoryDestroyView.as_view(), name='delete'),
]