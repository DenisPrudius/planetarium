from django.test import TestCase
from show.models import AstronomyShow, ShowTheme
from show.serializers import ShowThemeSerializer, AstronomyShowListSerializer, AstronomyShowDetailSerializer

class ShowSerializerTestCase(TestCase):

    def setUp(self):
        self.theme1 = ShowTheme.objects.create(name="Space")
        self.theme2 = ShowTheme.objects.create(name="Stars")

        self.show = AstronomyShow.objects.create(title="Galaxy Exploration", description="Explore the galaxy!")
        self.show.themes.add(self.theme1, self.theme2)

    def test_show_theme_serializer(self):
        serializer = ShowThemeSerializer(self.theme1)
        data = serializer.data
        self.assertEqual(data["id"], self.theme1.id)
        self.assertEqual(data["name"], "Space")

    def test_astronomy_show_list_serializer(self):
        serializer = AstronomyShowListSerializer(self.show)
        data = serializer.data
        self.assertEqual(data["id"], self.show.id)
        self.assertEqual(data["title"], "Galaxy Exploration")
        self.assertEqual(len(data["themes"]), 2)
        self.assertEqual(data["themes"][0]["name"], "Space")
        self.assertEqual(data["themes"][1]["name"], "Stars")

    def test_astronomy_show_detail_serializer(self):
        serializer = AstronomyShowDetailSerializer(self.show)
        data = serializer.data
        self.assertEqual(data["id"], self.show.id)
        self.assertEqual(data["title"], "Galaxy Exploration")
        self.assertEqual(data["description"], "Explore the galaxy!")
        self.assertEqual(len(data["themes"]), 2)
        self.assertEqual(data["themes"][0]["name"], "Space")
        self.assertEqual(data["themes"][1]["name"], "Stars")