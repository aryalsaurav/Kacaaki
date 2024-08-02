from django.db import models
from users.models import User

# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField('Room Name', max_length=50,blank=True,null=True)
    users = models.ManyToManyField(User, related_name='chat_rooms',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
    
    


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(blank=True,null=True,upload_to='chat_images/')
    
    def __str__(self):
        return str(self.message)[:15] + ' - ' + self.user.full_name
    
    
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None
        
        




class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Group(models.Model):
    name = models.CharField(max_length=100,help_text="hllo world")
    members = models.ManyToManyField(Person, related_name='groups',through='Membership')
    
    def __str__(self):
        return self.name
    
    



class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.person) + ' - ' + str(self.group)