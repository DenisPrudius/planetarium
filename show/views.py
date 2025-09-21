import django_filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from planetarium.mixins import ActionSerializerPermissionMixin
from .serializers import AstronomyShowListSerializer, AstronomyShowDetailSerializer

from show.models import AstronomyShow



class AstronomyShowFilter(django_filters.FilterSet):
    themes = django_filters.BaseInFilter(field_name="themes__id", lookup_expr='in')

    class Meta:
        model = AstronomyShow
        fields = ['themes']

class AstronomyShowViewSet(ActionSerializerPermissionMixin, viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AstronomyShowFilter

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

