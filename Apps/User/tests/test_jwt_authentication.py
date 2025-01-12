from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

CustomUser = get_user_model()


class JWTAuthenticationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # create an admin user
        cls.email = "testuser@example.com"
        cls.password = "securepassword123"
        cls.user = CustomUser.objects.create_superuser(email=cls.email, password=cls.password)
        
        # login and protected urls
        cls.login_url = "/api/token/"
        cls.protected_url = "/api/user/create/"

    def test_obtain_jwt_token(self):
        """
        Test that a valid user can obtain a JWT token.
        """
        response = self.client.post(self.login_url, {"email": self.email, "password": self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_credentials(self):
        """
        Test that invalid credentials do not return a token.
        """
        response = self.client.post(self.login_url, {"email": self.email, "password": "wrongpassword"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_with_valid_token(self):
        """
        Test that a valid access token allows access to a protected endpoint.
        """
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        # attempting creating user with admin account
        response = self.client.post(self.protected_url, data={"email": "test@gmail.com", "password": "strongpassword"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_access_protected_endpoint_with_invalid_token(self):
        """
        Test that an invalid or expired token denies access to a protected endpoint.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")
        response = self.client.post(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_without_token(self):
        """
        Test that no token denies access to a protected endpoint.
        """
        response = self.client.post(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
