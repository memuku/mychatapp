from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    members = models.ManyToManyField(User)
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Block(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by_users')

    class Meta:
        unique_together = ('user', 'blocked_user')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content}"

class Block(models.Model):
    user = models.ForeignKey(User, related_name='blocked_users', on_delete=models.CASCADE, null=True)
    blocked_user = models.ForeignKey(User, related_name='blocked_by_users', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} blocked {self.blocked_user.username}"
