import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from common import db_retrieve_or_none
from .models import Thread, ChatMessage

# class ChatConsumer(WebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         self.room_group_name = None
#         self.room_name = None
#         self.user = None
#
#     def connect(self):
#         self.user = self.scope["user"]
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_room_{self.user.username}"
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
#
#         self.accept()
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         username = self.user.username
#
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {"type": "chat.message", "message": message, "username": username},
#         )
#
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]
#         username = event["username"]
#         # Send message to WebSocket
#         self.send(
#             text_data=json.dumps(
#                 {
#                     "type": "chat",
#                     "message": message,
#                     "username": username,
#                 }
#             )
#         )
#
#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.chat_room = None

    def connect(self):
        self.user = self.scope["user"]
        self.chat_room = f'user_chatroom_{self.user.id}'
        async_to_sync(self.channel_layer.group_add)(
            self.chat_room, self.channel_layer
        )
        self.accept()

    def receive(self, text_data):
        received_json = json.loads(text_data)
        message = received_json.get("message")
        sending_user_id = received_json.get("sent_by")
        receiving_user_id = received_json.get("send_to")
        thread_id = received_json.get("thread_id")

        if not message:
            print("Error: empty message")
            return False

        sending_user_instance = self.get_user_instance(sending_user_id)
        receiving_user_instance = self.get_user_instance(receiving_user_id)

        thread_instance = self.get_thread(thread_id)

        if not sending_user_instance:
            print("Error: SUI is incorrect")
        if not receiving_user_instance:
            print("Error: RUI is incorrect")
        if not thread_instance:
            print("Error: thread instance is incorrect")

        self.create_chat_message(thread_instance, sending_user_instance, message)

        target_chat_room = f'user_chatroom_{receiving_user_id}'

        response_object = {
            "type": "chat.message",
            "message": message,
            "sent_by": self.user.id,
            "thread_id": thread_id,
        }

        # Send to self chat room

        self.channel_layer.group_send(
            self.chat_room,
            response_object
        )

        # Send to target chat room
        self.channel_layer.group_send(
            target_chat_room,
            response_object
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "sent_by": event["sent_by"],
            "thread_id": event["thread_id"]
        }))

    def disconnect(self, close_code):
        pass

    def get_user_instance(self, user_id):
        return db_retrieve_or_none(User, user_id)

    def get_thread(self, thread_id):
        return db_retrieve_or_none(Thread, thread_id)

    def create_chat_message(self, thread, user, message):
        ChatMessage.objects.create(thread=thread, user=user, message=message)







