from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from planetarium.mixins import ActionSerializerPermissionMixin
from ticket.models import Reservation
from ticket.serializers import ReservationSerializer


class ReservationViewSet(ActionSerializerPermissionMixin, viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    action_serializer_classes = {
        "list": ReservationSerializer,
        "retrieve": ReservationSerializer,
        "create": ReservationSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
