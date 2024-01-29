from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from users.models import User
from .models import ChatRoom,ChatMessage
from django.core import serializers
from django.db.models import Count,Max,F
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Create your views here.


class ChatRoomListView(LoginRequiredMixin,View):
    

    template_name = 'chat/chatroom.html'
    def get(self,request):
        user = request.user
        chat_rooms = ChatRoom.objects.filter(users=user).annotate(
            last_message_time=Max('chatmessage__timestamp')).order_by('-last_message_time')
        
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




def user_search(request):
    name = request.GET.get('name')
    users = User.objects.filter(full_name__icontains=name).values('id','full_name')
    return JsonResponse({'users':list(users)}, safe=False)
    

def room_get_create(request):
    user_id = request.GET.get('user_id')
    search_user = User.objects.get(id=user_id)
    logged_user = request.user
    chat_room = ChatRoom.objects.filter(users=logged_user).filter(users=search_user)
    if chat_room:
        chat_room = chat_room[0]
    else:
        chat_room = ChatRoom.objects.create()
        chat_room.users.add(logged_user,search_user)
        chat_room.save()
    return JsonResponse({'room_id':chat_room.id}, safe=False)



def room_detail(request,pk):
    room = ChatRoom.objects.get(id=pk)
    non_message = ChatMessage.objects.filter(room=room).order_by('-timestamp')[:10]
    messages = non_message.annotate(user_name=F('user__full_name'))
    messages_list = [{'id': message.id, 'fields': {'user_name': message.user_name,'user':message.user.id, 'message': message.message,'timestamp':message.timestamp.isoformat()}} for message in messages]
    if not room.name:
        all_users = room.users.all()
        logged_user = request.user
        user = all_users.exclude(id=logged_user.id)[0]
        room_name = user.full_name
    else:
        room_name = room.name
    room_data = serializers.serialize('json', [room,])
    messages_data = json.dumps( messages_list)
    context = {
        'room_data':room_data,
        'messages_data':messages_data,
        'room_name':room_name,
        'message_len':len(messages),
    }
    return JsonResponse(context, safe=False)



@login_required
def chat_with_id(request,pk):
    user = request.user
    chat_rooms = ChatRoom.objects.filter(users=user).annotate(
        last_message_time=Max('chatmessage__timestamp')).order_by('-last_message_time')
    room = ChatRoom.objects.get(id=pk)
    messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')[:10]
    
    if not room.name:
        all_users = room.users.all()
        logged_user = request.user
        user = all_users.exclude(id=logged_user.id)[0]
        room_name = user.full_name
    else:
        room_name = room.name
    context = {
        'room_data':room,
        'chat_rooms':chat_rooms,
        'messages_data':reversed(messages),
        'room_name':room_name,
        'message_len':len(messages),
    }
    return render(request,'chat/chatroom.html',context)
    