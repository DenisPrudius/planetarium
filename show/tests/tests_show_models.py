from django.test import TestCase
from django.contrib.auth import get_user_model

from show.models import ShowTheme, AstronomyShow

User = get_user_model()

class AstronomyShowTestCase(TestCase):

    def setUp(self):
        self.theme1 = ShowTheme.objects.create(name="Space")
        self.theme2 = ShowTheme.objects.create(name="Stars")

    def test_show_creation(self):
        show = AstronomyShow.objects.create(title="Galaxy Exploration", description="Explore the galaxy!")
        show.themes.add(self.theme1, self.theme2)

        self.assertEqual(show.title, "Galaxy Exploration")
        self.assertEqual(show.description, "Explore the galaxy!")
        self.assertEqual(show.themes.count(), 2)
        self.assertIn(self.theme1, show.themes.all())
        self.assertIn(self.theme2, show.themes.all())

    def test_show_str(self):
        show = AstronomyShow.objects.create(title="Solar System", description="Planets and more")
        self.assertEqual(str(show), "Solar System")

    def test_theme_str(self):
        theme = ShowTheme.objects.create(name="Nebula")
        self.assertEqual(str(theme), "Nebula")