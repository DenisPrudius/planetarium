from django.db import models


class AstronomyShow(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    themes = models.ManyToManyField("ShowTheme", related_name="astronomy_shows")

    def __str__(self):
        return self.title


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



