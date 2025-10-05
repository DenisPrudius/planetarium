from django.contrib.sessions.models import Session
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError

User = get_user_model()

class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    show_session = models.ForeignKey("show_sessions.ShowSession", on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, related_name="tickets", null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "show_session"], name="unique_ticket_rows"),
        ]

    def __str__(self):
        return f"Row {self.row}, Seat {self.seat} ({self.show_session})"

    def clean(self):
        if not (1 <= self.row <= self.show_session.planetarium_dome.rows):
            raise ValidationError({"row": f"Row must be between 1 and {self.show_session.planetarium_dome.rows}"})
        if not (1 <= self.seat <= self.show_session.planetarium_dome.seats_in_row):
            raise ValidationError(
                {"seat": f"Seat must be between 1 and {self.show_session.planetarium_dome.seats_in_row}"})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)