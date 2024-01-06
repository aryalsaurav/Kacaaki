from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views import View
from .models import ChatRoom,ChatMessage
from users.models import User


# Create your views here.


class ChatRoomListView(View):
    template_name = 'chat/chatroom.html'
    def get(self,request):
        chat_rooms = ChatRoom.objects.all()
        
        context = {
            'chat_rooms':chat_rooms,
        }
        return render(request,self.template_name,context)
    
    
class ChatRoomView(View):
    template_name = 'chat/chatting.html'
    
    def get(self,request,pk):
        chat_room = ChatRoom.objects.get(id=pk)
        chat_messages = ChatMessage.objects.filter(room=chat_room).order_by('timestamp')
        context = {
            'chat_room':chat_room,
            'chat_messages':chat_messages,
        }
        return render(request,self.template_name,context)