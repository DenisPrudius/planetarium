from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from planetarium.mixins import ActionSerializerPermissionMixin
from show_sessions.models import ShowSession
from show_sessions.serializers import ShowSessionListSerializer, ShowSessionCreateSerializer


class ShowSessionViewSet(ActionSerializerPermissionMixin, viewsets.ModelViewSet):
    queryset = ShowSession.objects.select_related("astronomy_show", "planetarium_dome").all()
    serializer_class = ShowSessionListSerializer
    permission_classes = [IsAuthenticated]

    action_serializer_classes = {
        "list": ShowSessionListSerializer,
        "retrieve": ShowSessionListSerializer,
        "create": ShowSessionCreateSerializer,
        "update": ShowSessionCreateSerializer,
        "partial_update": ShowSessionCreateSerializer,
    }

    action_permission_classes = {
        "destroy": [IsAdminUser],
    }

    @action(detail=True, methods=["get"], url_path="available-seats")
    def available_seats(self, request, pk=None):
        session = self.get_object()
        dome = session.planetarium_dome
        total = dome.rows * dome.seats_in_row
        booked = session.tickets.count()
        return Response({"total_seats": total, "booked": booked, "available": total - booked})