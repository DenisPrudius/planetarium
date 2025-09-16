from rest_framework import serializers
from .models import Ticket, Reservation


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "show_session", "reservation"]


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True, source="tickets")

    class Meta:
        model = Reservation
        fields = ["id", "user", "created_at", "tickets"]
        read_only_fields = ["user", "created_at"]