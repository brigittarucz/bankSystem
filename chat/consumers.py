import json
from channels.generic.websocket import AsyncWebsocketConsumer
from auth_app.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


# from channels.consumer import SyncConsumer
# from asgiref.sync import async_to_sync



# class EchoConsumer(SyncConsumer):

#     def websocket_connect(self, event):
#         self.room_name = 'broadcast'
# #We can do validation at this point to accept or reject the connection
#         self.send({
#             'type': 'websocket.accept'
#         })
#         #channel_name is the same as say ssh connection id
#         async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
#         print(f'[{self.channel_name} - You-re connected')

#     def websocket_receive(self, event):
#         print(f'[{self.channel_name} - Received Message - {event["text"]}')
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_name,
#             {
#             'type':'websocket.message',
#             'text': event.get('text')
#             }
#         )

        
#     def websocket_message(self, event):
#         print(f'[{self.channel_name} - Message Sent - {event["text"]}')
#         self.send({
#             'type':'websocket.send',
#             'text': event.get('text')
#         })




        
#     def websocket_disconnect(self, event):
#         print(f'[{self.channel_name} - Disconnected')
#         async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)




