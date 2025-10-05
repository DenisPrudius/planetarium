from django.urls import path

from users.views import CreateUserView, LoginUserView, ManageUserView
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="get_token"),
    path("me/", ManageUserView.as_view(), name="manage-user"),
]

app_name = "users"