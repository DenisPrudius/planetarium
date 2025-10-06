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
        "create": [IsAdminUser],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [IsAdminUser],
    }

    @action(detail=True, methods=["get"], url_path="available-seats")
    def available_seats(self, request, pk=None):
        session = self.get_object()
        dome = session.planetarium_dome
        total = dome.rows * dome.seats_in_row

        booked_tickets = session.tickets.all()

        booked = [{"row": t.row, "seat": t.seat} for t in booked_tickets]

        return Response({
            "total_seats": total,
            "booked_count": len(booked),
            "booked_seats": booked,
            "available": total - len(booked)
        })
