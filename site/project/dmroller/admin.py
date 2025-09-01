from django.contrib import admin
from .models import Room
from .models import RoomUser
from .models import User_RollConfig
from .models import RollResult

admin.site.register(Room)
admin.site.register(RoomUser)
admin.site.register(User_RollConfig)
admin.site.register(RollResult)
