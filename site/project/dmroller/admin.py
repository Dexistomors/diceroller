from django.contrib import admin
from .models import Room
from .models import RoomUser
from .models import RollConfig
from .models import RollResult

admin.site.register(Room)
admin.site.register(RoomUser)
admin.site.register(RollConfig)
admin.site.register(RollResult)
