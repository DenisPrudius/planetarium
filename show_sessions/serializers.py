from rest_framework import serializers
from .models import PlanetariumDome, ShowSession
from show.serializers import AstronomyShowListSerializer


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ["id", "name", "rows", "seats_in_row"]

class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = AstronomyShowListSerializer(read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(read_only=True)

    class Meta:
        model = ShowSession
        fields = ["id", "astronomy_show", "planetarium_dome", "show_time"]


class ShowSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ["id", "astronomy_show", "planetarium_dome", "show_time"]
