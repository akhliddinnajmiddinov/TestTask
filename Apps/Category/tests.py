from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category
from user.models import CustomUser 
from rest_framework_simplejwt.tokens import RefreshToken

class TestCategoryAPITests(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.admin_user = CustomUser .objects.create_superuser(
            email='admin@example.com',
            password='adminpassword'
        )
        self.category = Category.objects.create(name='Test Category')

        # Generate JWT token for the admin user
        self.token = self.get_jwt_token(self.admin_user)

    def get_jwt_token(self, user):
        # Generate a JWT token for the given user
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_list_categories(self):
        url = reverse('category:list')  # Adjust the name based on your URL configuration
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming one category is created

    def test_create_category(self):
        url = reverse('category:create')  # Adjust the name based on your URL configuration
        data = {'name': 'New Category'}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)  # One existing + one new

    def test_retrieve_category(self):
        url = reverse('category:retrieve', args=[self.category.pk])  # Adjust the name based on your URL configuration
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    def test_update_category(self):
        url = reverse('category:update', args=[self.category.pk])  # Adjust the name based on your URL configuration
        data = {'name': 'Updated Category'}
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_destroy_category(self):
        url = reverse('category:destroy', args=[self.category.pk])  # Adjust the name based on your URL configuration
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)  # Category should be deleted