from django.test import TestCase
from django.contrib.auth import get_user_model
from show.models import AstronomyShow
from show_sessions.models import PlanetariumDome, ShowSession
from ticket.models import Ticket, Reservation
from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()

class TicketReservationModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="12345")

        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=5, seats_in_row=10)

        self.show = AstronomyShow.objects.create(title="Galaxy Exploration", description="Explore the galaxy!")

        self.show_time = timezone.now()
        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time=self.show_time
        )

        self.reservation = Reservation.objects.create(user=self.user)

    def test_ticket_creation_valid(self):
        ticket = Ticket.objects.create(row=1, seat=1, show_session=self.session, reservation=self.reservation)
        self.assertEqual(ticket.row, 1)
        self.assertEqual(ticket.seat, 1)
        self.assertEqual(ticket.show_session, self.session)
        self.assertEqual(ticket.reservation, self.reservation)

    def test_ticket_str(self):
        ticket = Ticket.objects.create(row=2, seat=3, show_session=self.session)
        self.assertEqual(str(ticket), f"Row 2, Seat 3 ({ticket.show_session})")

    def test_ticket_row_seat_validation(self):
        ticket = Ticket(row=0, seat=1, show_session=self.session)
        with self.assertRaises(ValidationError):
            ticket.full_clean()

        ticket = Ticket(row=1, seat=11, show_session=self.session)
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_ticket_unique_constraint(self):
        Ticket.objects.create(row=1, seat=1, show_session=self.session)
        with self.assertRaises(ValidationError):
            t = Ticket(row=1, seat=1, show_session=self.session)
            t.full_clean()

    def test_reservation_creation(self):
        reservation = Reservation.objects.create(user=self.user)
        self.assertEqual(reservation.user, self.user)
        self.assertIsNotNone(reservation.created_at)

    def test_reservation_str(self):
        reservation = Reservation.objects.create(user=self.user)
        self.assertEqual(str(reservation), str(reservation.created_at))