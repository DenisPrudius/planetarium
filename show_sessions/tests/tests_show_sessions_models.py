from django.test import TestCase
from show.models import AstronomyShow
from show_sessions.models import ShowSession, PlanetariumDome
from django.utils import timezone


class ShowSessionModelTestCase(TestCase):

    def setUp(self):
        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=10, seats_in_row=20)

        self.show = AstronomyShow.objects.create(title="Galaxy Exploration", description="Explore the galaxy!")

    def test_planetarium_dome_creation(self):
        self.assertEqual(self.dome.name, "Main Dome")
        self.assertEqual(self.dome.rows, 10)
        self.assertEqual(self.dome.seats_in_row, 20)
        self.assertEqual(str(self.dome), "Main Dome")

    def test_show_session_creation(self):
        show_time = timezone.now()
        session = ShowSession.objects.create(astronomy_show=self.show, planetarium_dome=self.dome, show_time=show_time)

        self.assertEqual(session.astronomy_show, self.show)
        self.assertEqual(session.planetarium_dome, self.dome)
        self.assertEqual(session.show_time, show_time)
        self.assertEqual(str(session), f"{self.show.title} at {show_time}")