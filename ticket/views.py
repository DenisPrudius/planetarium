from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from planetarium.mixins import ActionSerializerPermissionMixin
from ticket.models import Reservation, Ticket
from ticket.serializers import ReservationSerializer, TicketSerializer, ReservationCreateSerializer, \
    ReservationDetailSerializer


class ReservationViewSet(ActionSerializerPermissionMixin, viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    action_serializer_classes = {
        "list": ReservationSerializer,
        "retrieve": ReservationDetailSerializer,
        "create": ReservationCreateSerializer,
        "update": ReservationDetailSerializer,
        "partial_update": ReservationCreateSerializer,
    }

    action_permission_classes = {
        "destroy": [IsAdminUser],
    }

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TicketViewSet(ActionSerializerPermissionMixin, viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("show_session", "reservation").all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    action_serializer_classes = {
        "list": TicketSerializer,
        "retrieve": TicketSerializer,
        "create": TicketSerializer,
    }

    action_permission_classes = {
        "destroy": [IsAdminUser],
    }