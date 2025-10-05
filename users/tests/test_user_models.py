from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTestCase(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(username="testuser", password="testpass", email="user@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "user@example.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("testpass"))

    def test_create_superuser(self):
        admin = User.objects.create_superuser(username="admin", password="adminpass", email="admin@example.com")
        self.assertEqual(admin.username, "admin")
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password("adminpass"))

    def test_str_method(self):
        user = User.objects.create_user(username="testuser2", password="pass")
        self.assertEqual(str(user), user.username)