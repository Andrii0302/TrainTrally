from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import ChatGroup, ChatMessage  # Ensure your models are imported
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)

        # Add this channel to the chatroom group
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )

        # Add the user to online users if not already present
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, close_code):
        # Remove this channel from the chatroom group
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )

        # Remove the user from online users
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        # Create the chat message
        message = ChatMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )

        event = {
            'type': 'message_handler',
            'message_id': str(message.id),  
            'user_id': str(self.user.id),    
        }

        # Send the event to the chatroom group
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = ChatMessage.objects.get(id=message_id)

        # Prepare the context for rendering the message
        context = {
            "message": message,
            'user': self.user,
        }

        # Render the message HTML
        html = render_to_string('realtimechat/partials/chat_message_p.html', context=context)

        # Send the rendered HTML to the WebSocket
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1  
        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
        }

        # Send the online count event to the chatroom group
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            event
        )

    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string('realtimechat/partials/online_count.html', {'online_count': online_count})

        # Send the updated online count to the WebSocket
        self.send(text_data=html)
