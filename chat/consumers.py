import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    """
    A consumer does three things:
    1. Accepts connections.
    2. Receives messages from client.
    3. Disconnects when the job is done.
    """

    async def connect(self):
        user = self.scope['user']

        if user.is_authenticated:
            self.room_group_name = f"chat_{user.username}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        profile_pic = text_data_json['profile_pic']
        user_id = text_data_json['user_id']

        recipient = await sync_to_async(User.objects.get)(id=user_id)
        await self.channel_layer.group_send(
            f"chat_{recipient.username}",
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'profile_pic': profile_pic,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'profile_pic': event['profile_pic'],
        }))

    @sync_to_async
    def save_message(self, message, username, profile_pic, room):
        """
        Save message to the database
        """
        if room:
            Message.objects.create(
                message_content=message,
                username=username,
                profile_pic=profile_pic,
                room=room
            )
        else:
            raise ValueError("Room cannot be empty")
