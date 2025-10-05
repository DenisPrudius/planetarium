from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from users.serializers import UserSerializer

User = get_user_model()

class UserSerializerTestCase(TestCase):

    def test_create_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "strongpass"
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("strongpass"))

    def test_create_user_short_password(self):
        data = {
            "username": "shortpassuser",
            "email": "user@example.com",
            "password": "123"
        }
        serializer = UserSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_update_user_password(self):
        user = User.objects.create_user(username="olduser", password="oldpass")
        data = {"password": "newstrongpass"}
        serializer = UserSerializer(user, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()
        self.assertTrue(updated_user.check_password("newstrongpass"))

    def test_update_user_fields(self):
        user = User.objects.create_user(username="olduser", password="oldpass", email="old@example.com")
        data = {"username": "updateduser", "email": "updated@example.com"}
        serializer = UserSerializer(user, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.email, "updated@example.com")
        self.assertTrue(updated_user.check_password("oldpass"))
