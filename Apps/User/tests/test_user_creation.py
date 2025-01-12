from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

CustomUser = get_user_model()


class AdminCreateUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create an admin user
        cls.admin_email = "admin@example.com"
        cls.admin_password = "adminpassword"
        cls.admin_user = CustomUser.objects.create_superuser(
            email=cls.admin_email,
            password=cls.admin_password
        )
        
        # Endpoint to test
        cls.create_user_url = "/api/user/create/"

    def setUp(self):
        # Generate an admin token
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_create_user_success(self):
        """
        Test that an admin can successfully create a user.
        """
        data = {
            "email": "newuser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "password": "securepassword123"
        }
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])
        self.assertTrue(CustomUser.objects.filter(email=data["email"]).exists())

    def test_create_user_missing_fields(self):
        """
        Test that creating a user with missing fields returns validation errors.
        """
        data = {
            "email": "incompleteuser@example.com"
        }
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_invalid_email(self):
        """
        Test that creating a user with an invalid email returns an error.
        """
        data = {
            "email": "invalid-email",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "password": "securepassword123"
        }
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_user_weak_password(self):
        """
        Test that creating a user with a weak password returns an error.
        """
        data = {
            "email": "weakpassworduser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "password": "123"
        }
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_unauthorized_access(self):
        """
        Test that unauthorized users cannot access the endpoint.
        """
        self.client.credentials()  # Remove authorization header
        data = {
            "email": "unauthorizeduser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "password": "securepassword123"
        }
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_access(self):
        """
        Test that non-admin users cannot access the endpoint.
        """
        non_admin_user = CustomUser.objects.create_user(
            email="nonadmin@example.com",
            password="userpassword"
        )
        refresh = RefreshToken.for_user(non_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        
        data = {
            "email": "nonadminattempt@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "phone_number": "+0987654321",
            "password": "securepassword123"
        }
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_duplicate_email(self):
        """
        Test that creating a user with an email that already exists returns an error.
        """
        existing_email = "existinguser@example.com"
        CustomUser.objects.create_user(
            email=existing_email,
            password="somepassword"
        )
        data = {
            "email": existing_email,
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "password": "securepassword123"
        }
        response = self.client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
