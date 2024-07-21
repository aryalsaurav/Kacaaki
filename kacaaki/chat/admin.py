from django.contrib import admin
from .models import ChatRoom,ChatMessage,Person,Group,Membership

# Register your models here.

admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(Person) 
admin.site.register(Group)
admin.site.register(Membership)