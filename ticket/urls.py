from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet, TicketViewSet

app_name = "ticket"

router = DefaultRouter()
router.register("create", TicketViewSet, basename="ticket")
router.register("reservations", ReservationViewSet, basename="reservation")

urlpatterns = [
    path("", include(router.urls)),
]