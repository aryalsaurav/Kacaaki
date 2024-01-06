import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from .models import ChatRoom,ChatMessage
from users.models import User
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name='chat_%s' % self.room_name
        
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    
    async def disconnect(self,close_code):
        print(f"WebSocket disconnected: {close_code}")
        pass
    
    
    
    
    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        room_id = text_data_json['room_id']
        
        await sync_to_async(self.save_message)(message,user,room_id)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'user':user,
                'room_id':room_id,
            })
        
        
        
    # async def send_message(self,text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     user = text_data_json['user']
    #     room_id = text_data_json['room_id']
        
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type':'chat_message',
    #             'message':message,
    #             'user':user,
    #             'room_id':room_id,
    #         })
        
        
    async def chat_message(self,event):
        message = event['message']
        user = event['user']
        room_id = event['room_id']
        
        await self.send(text_data=json.dumps({
            'message':message,
            'user':user,
            'room_id':room_id,
        }))
        
        
    @staticmethod   
    def save_message(message,user,room_id):
        chat_room = ChatRoom.objects.get(id=room_id)
        user = User.objects.get(id=user)
        chat_message = ChatMessage.objects.create(room=chat_room,user=user,message=message)
        chat_message.save()
    
    