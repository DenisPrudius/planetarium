from rest_framework import serializers
from show.models import AstronomyShow, ShowTheme


class AstronomyShowSerializer(serializers.ModelSerializer):
    themes = AstronomyShowSerializer(many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ["id", "title", "themes"]


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ["id", "name"]