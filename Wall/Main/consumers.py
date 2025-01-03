import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from Main.models import Message, Room, Users
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Save message to database
        await self.save_message(username, message)
        chat_history = await self.get_chat_history()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chat_history': chat_history
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chat_history = event['chat_history']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chat_history': chat_history
        }))

    @sync_to_async
    def save_message(self, username, message):
        user = Users.objects.get(username=username)
        room = Room.objects.get(id=self.room_id)
        Message.objects.create(room=room, sender=user, content=message)

    @sync_to_async
    def get_chat_history(self):
        room = Room.objects.get(id=self.room_id)
        messages = Message.objects.filter(room=room).order_by('timestamp')
        return [{'username': msg.sender.username, 'message': msg.content, 'timestamp': msg.timestamp} for msg in messages]