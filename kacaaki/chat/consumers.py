import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from .models import ChatRoom,ChatMessage
from users.models import User
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
import base64
import asyncio

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
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def close(self,code=3000):
        await super().close(code)
    
    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        data_type = text_data_json['type']
        message = text_data_json['message']
        user = text_data_json['user']
        room_id = text_data_json['room_id']
        if data_type == "file":
            file_name = text_data_json['file_name']
            file_data = message.split(';base64,')[1]
            file_content = base64.b64decode(file_data)
            await sync_to_async(self.save_message)(file_content,user,room_id,data_type,file_name=file_name)
        
        
        elif data_type == "audio":
            pass
        
        else:
            await sync_to_async(self.save_message)(message,user,room_id,data_type)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':data_type,
                'message':message,
                'user':user,
                'room_id':room_id,
            })
        
        
    async def webrtc_signaling(self, event):
        message = event['message']
        user = event['user']
        room_id = event['room_id']
        signal_type = event['signal_type']

        # Send signaling message to WebSocket
        await self.send(text_data=json.dumps({
            'type': signal_type,
            'message': message,
            'user': user,
            'room_id': room_id,
        }))
    
        
    
    async def file(self,event):
        message = event['message']
        user = event['user']
        room_id = event['room_id']
        
        
        await self.send(text_data=json.dumps({
            'message':message,
            'user':user,
            'room_id':room_id,
            'type':'file',
            
        }))
        
        
    async def text(self,event):
        message = event['message']
        user = event['user']
        room_id = event['room_id']
        
        await self.send(text_data=json.dumps({
            'message':message,
            'user':user,
            'room_id':room_id,
            'type':'text',
        }))
        
        
    @staticmethod   
    def save_message(message,user,room_id,data_type,file_name=None):
        chat_room = ChatRoom.objects.get(id=room_id)
        user = User.objects.get(id=user)
        if data_type == "text":
            chat_message = ChatMessage.objects.create(room=chat_room,user=user,message=message)
        else:
            # file = ContentFile(message)
            chat_message = ChatMessage.objects.create(room=chat_room,user=user)
            chat_message.image.save(file_name,ContentFile(message),save=True)
        chat_message.save()
    
    