from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("api/roll/", views.api_roll, name = "api_roll"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("roller/", views.roller, name = "roller"),
    path("api/room/", views.room, name= "api_room")
]