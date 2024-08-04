from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid
# Create your models here.

class Room(models.Model):
    room_code = models.CharField(max_length=8,blank=True,null=True,unique=True)
    def save(self, *args, **kwargs):
        while not self.room_code:
            temp = uuid.uuid4().hex[:8].upper()
            if not Room.objects.filter(room_code=temp).exclude(pk=self.pk).exists():
                self.room_code = temp
                break
        super(Room, self).save(*args, **kwargs)

class RoomUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

class RollConfig(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    roll_config = models.TextField()
    name = models.TextField(default=None, blank=True, null=True, unique=True)

class RollResult(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    roll_config = models.ForeignKey(RollConfig, on_delete=models.CASCADE)
    roll_result = models.TextField()