import json
from datetime import datetime
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
        message_content = data['message']
        username = data['username']

        # Save message to the database and get its ID
        message_id = await self.save_message(username, message_content)

        # Send the new message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_id': message_id
            }
        )

    async def chat_message(self, event):
        message_id = event.get('message_id')
        message = await self.get_message_by_id(message_id)
        timestamp = message['timestamp']
        # Send formatted message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message['content'],
            'username': message['sender'],
            'timestamp': timestamp
        }))

    @sync_to_async
    def save_message(self, username, message):
        user = Users.objects.get(username=username)
        room = Room.objects.get(id=self.room_id)
        msg = Message.objects.create(room=room, sender=user, content=message)
        return msg.id

    @sync_to_async
    def get_message_by_id(self, message_id):
        message = Message.objects.get(id=message_id)
        timestamp = message.timestamp.strftime('%b. %d, %Y, %I:%M %p').lstrip('0').replace("PM","p.m").replace("AM","a.m")
        return {
            'content': message.content,
            'sender': message.sender.username,
            'timestamp': timestamp
        }
