from django.urls import path, include
from rest_framework.routers import DefaultRouter

from show.views import AstronomyShowViewSet

router = DefaultRouter()
router.register("", AstronomyShowViewSet, basename="show")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "show"