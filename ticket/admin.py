from django.contrib import admin
from .models import Ticket, Reservation

admin.site.register(Ticket)
admin.site.register(Reservation)