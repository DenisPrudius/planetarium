from django.contrib.sessions.models import Session
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    show_session = models.ForeignKey("ShowSession", on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, related_name="tickets", null=True, blank=True)

    def __str__(self):
        return f"Row {self.row}, Seat {self.seat} ({self.show_session})"

    class Meta:
        unique_together = ("show_session", "row", "seat")


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")

    def __str__(self):
        return f"Reservation {self.id} by {self.user}"