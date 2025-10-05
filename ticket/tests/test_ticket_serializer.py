from django.test import TestCase
from django.contrib.auth import get_user_model
from show_sessions.models import PlanetariumDome, ShowSession
from show.models import AstronomyShow
from ticket.models import Ticket, Reservation
from ticket.serializers import TicketSerializer, ReservationSerializer, ReservationCreateSerializer, ReservationDetailSerializer
from django.utils import timezone

User = get_user_model()

class ReservationSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="12345")

        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=5, seats_in_row=10)
        self.show = AstronomyShow.objects.create(title="Galaxy Exploration", description="Explore the galaxy!")
        self.show_time = timezone.now()
        self.session = ShowSession.objects.create(astronomy_show=self.show, planetarium_dome=self.dome, show_time=self.show_time)

    def test_ticket_serializer(self):
        ticket = Ticket.objects.create(row=1, seat=1, show_session=self.session)
        serializer = TicketSerializer(ticket)
        data = serializer.data
        self.assertEqual(data["row"], 1)
        self.assertEqual(data["seat"], 1)
        self.assertEqual(data["show_session"], self.session.id)

    def test_reservation_create_serializer(self):
        data = {
            "tickets": [
                {"row": 1, "seat": 1, "show_session": self.session.id},
                {"row": 1, "seat": 2, "show_session": self.session.id},
            ]
        }
        serializer = ReservationCreateSerializer(data=data, context={"request": type("Req", (), {"user": self.user})()})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        reservation = serializer.save()
        self.assertEqual(reservation.user, self.user)
        self.assertEqual(reservation.tickets.count(), 2)

    def test_reservation_serializer_read(self):
        reservation = Reservation.objects.create(user=self.user)
        Ticket.objects.create(row=1, seat=1, show_session=self.session, reservation=reservation)
        Ticket.objects.create(row=1, seat=2, show_session=self.session, reservation=reservation)

        serializer = ReservationSerializer(reservation)
        data = serializer.data
        self.assertEqual(data["user"], self.user.id)
        self.assertEqual(len(data["tickets"]), 2)

    def test_reservation_detail_serializer(self):
        reservation = Reservation.objects.create(user=self.user)
        Ticket.objects.create(row=1, seat=1, show_session=self.session, reservation=reservation)
        serializer = ReservationDetailSerializer(reservation)
        data = serializer.data
        self.assertEqual(data["user"], self.user.id)
        self.assertEqual(len(data["tickets"]), 1)
        self.assertEqual(data["tickets"][0]["row"], 1)