from django.test import TestCase
from django.utils import timezone
from show.models import AstronomyShow
from show_sessions.models import PlanetariumDome, ShowSession
from show_sessions.serializers import PlanetariumDomeSerializer, ShowSessionListSerializer, ShowSessionCreateSerializer

class ShowSessionSerializerTestCase(TestCase):

    def setUp(self):
        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=10, seats_in_row=20)

        self.show = AstronomyShow.objects.create(title="Galaxy Exploration", description="Explore the galaxy!")

        self.show_time = timezone.now()
        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time=self.show_time
        )

    def test_planetarium_dome_serializer(self):
        serializer = PlanetariumDomeSerializer(self.dome)
        data = serializer.data
        self.assertEqual(data["id"], self.dome.id)
        self.assertEqual(data["name"], "Main Dome")
        self.assertEqual(data["rows"], 10)
        self.assertEqual(data["seats_in_row"], 20)

    def test_show_session_list_serializer(self):
        serializer = ShowSessionListSerializer(self.session)
        data = serializer.data
        self.assertEqual(data["id"], self.session.id)
        self.assertEqual(data["astronomy_show"]["title"], "Galaxy Exploration")
        self.assertEqual(data["planetarium_dome"]["name"], "Main Dome")
        self.assertEqual(data["show_time"], self.show_time.isoformat().replace("+00:00", "Z"))

    def test_show_session_create_serializer(self):
        data = {
            "astronomy_show": self.show.id,
            "planetarium_dome": self.dome.id,
            "show_time": self.show_time
        }
        serializer = ShowSessionCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.astronomy_show, self.show)
        self.assertEqual(instance.planetarium_dome, self.dome)
        self.assertEqual(instance.show_time, self.show_time)