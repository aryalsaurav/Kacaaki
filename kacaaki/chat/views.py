from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from users.models import User
from .models import ChatRoom,ChatMessage
from django.core import serializers


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
        chat_messages = ChatMessage.objects.filter(room=chat_room).order_by('-timestamp')[:10]
        context = {
            'chat_room':chat_room,
            'chat_messages':reversed(chat_messages),
        }
        return render(request,self.template_name,context)
    
    

def load_more_messages(request):
    room_id = request.GET.get('room_id')
    offset = int(request.GET.get('offset'))

    room = ChatRoom.objects.get(id=room_id)
    messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')[offset:offset + 10]

    serialized_messages = serializers.serialize('json', messages)
    

    return JsonResponse({'messages':serialized_messages}, safe=False)