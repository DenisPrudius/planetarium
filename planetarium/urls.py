"""
URL configuration for planetarium project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from ticket.views import ReservationViewSet, TicketViewSet
from show.views import AstronomyShowViewSet
from show_sessions.views import ShowSessionViewSet

router = DefaultRouter()
router.APIRootView.permission_classes = [AllowAny]
router.register("shows", AstronomyShowViewSet, basename="show")
router.register("show-sessions", ShowSessionViewSet, basename="show_session")
router.register("tickets", TicketViewSet, basename="ticket")
router.register("reservations", ReservationViewSet, basename="reservation")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls", namespace="user")),
    path("api/", include(router.urls)),
]
