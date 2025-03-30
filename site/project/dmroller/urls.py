from django.urls import include, path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name = "index"),
    path("api/roll/", views.api_roll, name = "api_roll"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("roller/", views.roller, name = "roller"),
    path("api/room/", views.room, name = "api_room"),
    path("api/roll_config/", csrf_exempt(views.api_rollconfig), name = "api_rollconfig"), #csrf_exempt() for testing purposes

]
