from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from Category.models import Category
from Product.models import Product
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class ProductJWTAPITests(APITestCase):
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
        cls.category = Category.objects.create(name="Electronics", description="All electronics")
        cls.category2 = Category.objects.create(name="Clothing", description="All clothing")

        # Create products
        cls.product1 = Product.objects.create(name="Laptop", price=999.99, category=cls.category)
        cls.product2 = Product.objects.create(name="Smartphone", price=599.99, category=cls.category)

        # JWT endpoint
        cls.token_url = reverse("token_obtain_pair")

        # Product endpoints
        cls.list_url = reverse("product:list")
        cls.list_category_products_url = "/api/product/category/{category_id}/"
        cls.create_url = reverse("product:create")
        cls.detail_url = reverse("product:retrieve", kwargs={"pk": cls.product1.pk})
        cls.update_url = reverse("product:update", kwargs={"pk": cls.product1.pk})
        cls.delete_url = reverse("product:destroy", kwargs={"pk": cls.product1.pk})

    def authenticate(self, email, password):
        """
        Authenticate and set the token for subsequent requests.
        """
        response = self.client.post(self.token_url, {"email": email, "password": password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_products_unauthenticated(self):
        """
        Test listing products without authentication.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_products_authenticated(self):
        """
        Test listing products with authentication.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_product_unauthenticated(self):
        """
        Test retrieving a product without authentication.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product_authenticated(self):
        """
        Test retrieving a product with authentication.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product1.name)

    def test_list_products_by_category(self):
        """
        Test listing products filtered by category.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        # Fetch products belonging to the first category
        print(self.list_category_products_url.format(category_id=self.category.pk))
        response = self.client.get(self.list_category_products_url.format(category_id=self.category.pk))
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(product["category"]["id"] == self.category.pk for product in response.data))

    def test_list_products_by_non_existent_category(self):
        """
        Test listing products with a non-existent category.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        # Use a non-existent category ID
        response = self.client.get(self.list_category_products_url.format(category_id=99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_product_admin(self):
        """
        Test creating a product as an admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        data = {"name": "Tablet", "price": 399.99, "category_id": self.category.pk}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name=data["name"]).exists())

    def test_create_product_non_admin(self):
        """
        Test creating a product as a non-admin user.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        data = {"name": "Unauthorized Product", "price": 199.99, "category_id": self.category.pk}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_admin(self):
        """
        Test updating a product as an admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        data = {"name": "Updated Laptop", "price": 1099.99}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, data["name"])

    def test_update_product_non_admin(self):
        """
        Test updating a product as a non-admin user.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        data = {"name": "Unauthorized Update"}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_admin(self):
        """
        Test deleting a product as an admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product1.pk).exists())

    def test_delete_product_non_admin(self):
        """
        Test deleting a product as a non-admin user.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_missing_fields(self):
        """
        Test creating a product with missing fields as admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        data = {"price": 199.99}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_retrieve_non_existent_product(self):
        """
        Test retrieving a product that does not exist.
        """
        self.authenticate(email="user@example.com", password="userpassword")
        response = self.client.get(reverse("product:retrieve", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_non_existent_product(self):
        """
        Test updating a non-existent product as admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        data = {"name": "Non-Existent Update"}
        response = self.client.put(reverse("product:update", kwargs={"pk": 999}), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existent_product(self):
        """
        Test deleting a non-existent product as admin.
        """
        self.authenticate(email="admin@example.com", password="adminpassword")
        response = self.client.delete(reverse("product:destroy", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
