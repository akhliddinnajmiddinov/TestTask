from django.urls import path
from .views import (
    CategoryListRetrieveView, CategoryCreateAPIView, CategoryRetrieveAPIView, 
    CategoryUpdateView, CategoryDestroyView
    )


app_name = 'category'
urlpatterns = [
    path('', CategoryListRetrieveView.as_view(), name='list'),
    path('create/', CategoryCreateAPIView.as_view(), name='create'),
    path('<int:pk>/', CategoryRetrieveAPIView.as_view(), name='retrieve'),
    path('<int:pk>/update', CategoryUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', CategoryDestroyView.as_view(), name='destroy'),
]