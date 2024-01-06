from django.db import models
from users.models import User

# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField('Room Name', max_length=50)
    users = models.ManyToManyField(User, related_name='chat_rooms',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    
    
    def __str__(self):
        return self.name
    
    


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return str(self.message)[:15] + ' - ' + self.user.full_name