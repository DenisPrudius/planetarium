from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from show.models import AstronomyShow, ShowTheme

User = get_user_model()

class AstronomyShowViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="user", password="12345")
        self.staff_user = User.objects.create_user(username="staff", password="12345", is_staff=True)

        self.theme1 = ShowTheme.objects.create(name="Space")
        self.theme2 = ShowTheme.objects.create(name="Stars")

        self.show1 = AstronomyShow.objects.create(title="Galaxy Exploration", description="Explore the galaxy!")
        self.show1.themes.add(self.theme1, self.theme2)

        self.show2 = AstronomyShow.objects.create(title="Solar System", description="Planets and more")
        self.show2.themes.add(self.theme1)

    def test_list_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/shows/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/shows/{self.show1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Galaxy Exploration")

    def test_create_non_staff_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": "New Show", "description": "Test"}
        response = self.client.post("/api/shows/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_staff_allowed(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {"title": "New Show", "description": "Test"}
        response = self.client.post("/api/shows/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AstronomyShow.objects.filter(title="New Show").count(), 1)

    def test_filter_by_theme(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/shows/?themes={self.theme2.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Galaxy Exploration")