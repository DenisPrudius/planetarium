from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from show.models import AstronomyShow
from show_sessions.models import PlanetariumDome, ShowSession
from ticket.models import Ticket
from django.utils import timezone

User = get_user_model()

class ShowSessionViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="user", password="12345")
        self.staff_user = User.objects.create_user(username="staff", password="12345", is_staff=True)

        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=5, seats_in_row=10)

        self.show = AstronomyShow.objects.create(title="Galaxy Exploration", description="Explore the galaxy!")

        self.show_time = timezone.now()
        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time=self.show_time
        )

    def test_list_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/show_sessions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/show_sessions/{self.session.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.session.id)

    def test_create_non_staff_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "astronomy_show": self.show.id,
            "planetarium_dome": self.dome.id,
            "show_time": self.show_time
        }
        response = self.client.post("/api/show_sessions/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_staff_allowed(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {
            "astronomy_show": self.show.id,
            "planetarium_dome": self.dome.id,
            "show_time": self.show_time
        }
        response = self.client.post("/api/show_sessions/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_available_seats_action(self):
        self.client.force_authenticate(user=self.user)

        Ticket.objects.create(row=1, seat=1, show_session=self.session)
        Ticket.objects.create(row=1, seat=2, show_session=self.session)

        response = self.client.get(f"/api/show_sessions/{self.session.id}/available-seats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["total_seats"], 50)  # 5*10
        self.assertEqual(data["booked_count"], 2)
        self.assertEqual(data["available"], 48)
        self.assertIn({"row": 1, "seat": 1}, data["booked_seats"])
        self.assertIn({"row": 1, "seat": 2}, data["booked_seats"])