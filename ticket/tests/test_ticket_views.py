from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from show.models import AstronomyShow
from show_sessions.models import PlanetariumDome, ShowSession
from ticket.models import Ticket, Reservation
from django.utils import timezone

User = get_user_model()

class ReservationViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="user", password="12345")
        self.other_user = User.objects.create_user(username="other", password="12345")
        self.staff_user = User.objects.create_user(username="staff", password="12345", is_staff=True)

        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=5, seats_in_row=10)
        self.show = AstronomyShow.objects.create(title="Galaxy Exploration", description="Explore the galaxy!")
        self.show_time = timezone.now()
        self.session = ShowSession.objects.create(astronomy_show=self.show, planetarium_dome=self.dome, show_time=self.show_time)

        self.reservation = Reservation.objects.create(user=self.user)
        self.ticket1 = Ticket.objects.create(row=1, seat=1, show_session=self.session, reservation=self.reservation)
        self.ticket2 = Ticket.objects.create(row=1, seat=2, show_session=self.session, reservation=self.reservation)

    def test_list_reservations_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/tickets/reservations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_reservations_unauthenticated(self):
        response = self.client.get("/api/tickets/reservations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_reservation(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "tickets": [
                {"row": 2, "seat": 1, "show_session": self.session.id},
                {"row": 2, "seat": 2, "show_session": self.session.id},
            ]
        }
        response = self.client.post("/api/tickets/reservations/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.filter(user=self.user).count(), 2)

    def test_reservation_access_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(f"/api/tickets/reservations/{self.reservation.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TicketViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="12345")
        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=5, seats_in_row=10)
        self.show = AstronomyShow.objects.create(title="Galaxy Exploration", description="Explore the galaxy!")
        self.session = ShowSession.objects.create(astronomy_show=self.show, planetarium_dome=self.dome, show_time=timezone.now())
        self.ticket = Ticket.objects.create(row=1, seat=1, show_session=self.session)

    def test_list_tickets_anyone(self):
        response = self.client.get("/api/tickets/create/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_ticket_anyone(self):
        data = {"row": 2, "seat": 1, "show_session": self.session.id}
        response = self.client.post("/api/tickets/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 2)
