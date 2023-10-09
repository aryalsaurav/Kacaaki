from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class Testomonial(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(null=True,blank=True,upload_to="testomonials")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_photo_url(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url