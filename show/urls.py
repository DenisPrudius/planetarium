from django.urls import path


urlpatterns = [
    path("", views.show, name='show'),
]

app_name = "show"