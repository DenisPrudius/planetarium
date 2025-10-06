from django.urls import path, include
from rest_framework.routers import DefaultRouter

from show_sessions.views import ShowSessionViewSet

app_name = "show_sessions"

router = DefaultRouter()
router.register("", ShowSessionViewSet, basename="show-session")

urlpatterns = [
    path("", include(router.urls)),
]