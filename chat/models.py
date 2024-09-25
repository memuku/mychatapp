from datetime import time
from django.utils import timezone

from django.db import models

# Create your models here.


class Message(models.Model):
    username = models.CharField(max_length=50)
    room = models.CharField(max_length=50, null=True)
    message_content = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ('date_added', )

    def __str__(self):
        return f"{self.username}: {self.message_content}"


class Room(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)