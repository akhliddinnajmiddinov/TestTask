from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category

CustomUser = get_user_model()


class CategoryJWTAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create admin and regular users
        cls.admin_user = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )
        cls.regular_user = CustomUser.objects.create_user(
            email="user@example.com", password="userpassword"
        )

        # Create categories
        cls.category1 = Category.objects.create(name="Category 1", description="Description 1")
        cls.category2 = Category.objects.create(name="Category 2", description="Description 2")

        # JWT endpoints
        cls.token_url = reverse("token_obtain_pair")
        cls.list_url = "/api/category/"
        cls.detail_url = "/api/category/{pk}/"
        cls.create_url = "/api/category/create/"
        cls.update_url = "/api/category/{pk}/update/"
        cls.delete_url = "/api/category/{pk}/delete/"

    def authenticate(self, email, password):
        """
        Authenticate and set the token for subsequent requests.
        """
        response = self.client.post(self.token_url, {"email": email, "password": password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_categories_unauthenticated(self):
        """
        Test listing categories without authentication.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_categories_authenticated(self):
        """
        Test listing categories with authentication.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_category_unauthenticated(self):
        """
        Test retrieving a single category without authentication.
        """
        response = self.client.get(self.detail_url.format(pk=self.category1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category_authenticated(self):
        """
        Test retrieving a single category with authentication.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        response = self.client.get(self.detail_url.format(pk=self.category1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category1.name)

    def test_create_category_admin(self):
        """
        Test creating a category as an admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        data = {"name": "New Category", "description": "New Description"}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name=data["name"]).exists())

    def test_create_category_non_admin(self):
        """
        Test creating a category as a non-admin user.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        data = {"name": "Unauthorized Category", "description": "Unauthorized Description"}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_admin(self):
        """
        Test updating a category as an admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        data = {"name": "Updated Category", "description": "Updated Description"}
        response = self.client.put(self.update_url.format(pk=self.category1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, data["name"])
        self.assertEqual(self.category1.description, data["description"])

    def test_update_category_non_admin(self):
        """
        Test updating a category as a non-admin user.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        data = {"name": "Unauthorized Update"}
        response = self.client.put(self.update_url.format(pk=self.category1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_admin(self):
        """
        Test deleting a category as an admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        response = self.client.delete(self.delete_url.format(pk=self.category1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category1.pk).exists())

    def test_delete_category_non_admin(self):
        """
        Test deleting a category as a non-admin user.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        response = self.client.delete(self.delete_url.format(pk=self.category1.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_missing_fields(self):
        """
        Test creating a category with missing fields as admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        data = {"description": "Missing Name"}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_retrieve_non_existent_category(self):
        """
        Test retrieving a category that does not exist.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        response = self.client.get(self.detail_url.format(pk=999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_non_existent_category(self):
        """
        Test updating a non-existent category as admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        data = {"name": "Non-Existent Update"}
        response = self.client.put(self.update_url.format(pk=999), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existent_category(self):
        """
        Test deleting a non-existent category as admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        response = self.client.delete(self.delete_url.format(pk=999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
