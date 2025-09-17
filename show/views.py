from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from planetarium.mixins import ActionSerializerPermissionMixin
from .serializers import AstronomyShowListSerializer, AstronomyShowDetailSerializer

from show.models import AstronomyShow


class AstronomyShowViewSet(ActionSerializerPermissionMixin, viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowDetailSerializer
    permission_classes = [IsAuthenticated]

    action_serializer_classes = {
        "list": AstronomyShowListSerializer,
        "retrieve": AstronomyShowDetailSerializer,
        "create": AstronomyShowDetailSerializer,
        "update": AstronomyShowDetailSerializer,
        "partial_update": AstronomyShowDetailSerializer,
        "destroy": AstronomyShowDetailSerializer,
    }

    action_permission_classes = {
        "destroy": [IsAdminUser],
    }
