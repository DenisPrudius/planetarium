from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserJWTApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "user@example.com",
            "password": "strongpass"
        }
        self.user = User.objects.create_user(**self.user_data)

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_user(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newstrongpass"
        }
        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_user_jwt(self):
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }
        response = self.client.post("/api/users/token/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_manage_user_get_authenticated_jwt(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/api/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_manage_user_update_authenticated_jwt(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {"username": "updateduser", "password": "newpass123"}
        response = self.client.patch("/api/users/me/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertTrue(self.user.check_password("newpass123"))

    def test_manage_user_unauthenticated(self):
        response = self.client.get("/api/users/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)