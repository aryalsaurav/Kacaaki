from django.db import models
import datetime
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.conf import settings
from .managers import UserManager,NepaliStudentManager,DanceStudentManager
from django.contrib.auth.models import AbstractBaseUser, Group,AbstractUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from rest_framework.authtoken.models import Token as AuthToken
from django.contrib.postgres.fields import ArrayField
# from .fields import UserAgentField


# Create your models here.



gender_choices = [
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others'),
    ]

skills = [
        ('0','0 (None)'),
        ('1','1 (Low)'),
        ('2','2 (Medium)'),
        ('3','3 (Good)'),
        ('4','4 (Very Good)'),
        ('5','5 (Well)'),
    ]

session_choices=[
        ('Group Class 1 seesion per week','Group Class 1 session per week'),
        ('Group Class 2 seesion per week','Group Class 2 session per week'),
        ('One-One class 1 session per week','One-One class 1 session per week'),
        ('One-One class 2 session per week','One-One class 2 session per week'),
    ]
# 

class ClassTime(models.TextChoices):
        Sunday_Morning = 'Sunday Morning', 'Sunday Morning'
        Sunday_Evening = 'Sunday Evening', 'Sunday Evening'
        Monday_Morning = 'Monday Morning', 'Monday Morning'
        Monday_Evening = 'Monday Evening', 'Monday Evening'
        Tuesday_Morning = 'Tuesday Morning', 'Tuesday Morning'
        Tuesday_Evening = 'Tuesday Evening', 'Tuesday Evening'
        Wednesday_Morning = 'Wednesday Morning', 'Wednesday Morning'
        Wednesday_Evening = 'Wednesday Evening', 'Wednesday Evening'
        Thursday_Morning = 'Thursday Morning', 'Thursday Morning'
        Thursday_Evening = 'Thursday Evening', 'Thursday Evening'
        Friday_Morning = 'Friday Morning', 'Friday Morning'
        Friday_Evening = 'Friday Evening', 'Friday Evening'
        Saturday_Morning = 'Saturday Morning', 'Saturday Morning'
        Saturday_Evening = 'Saturday Evening', 'Saturday Evening'


user_type_choices = (
        ('Nepali Student','Nepali Student'),
        ('Dance Student','Dance Student'),
        ('Nepali Teacher','Nepali Teacher'),
        ('Dance Teacher','Dance Teacher'),
        ('Admin','Admin'),
        ('Management','Management'),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    full_name = models.CharField(max_length=50)
    phone = models.CharField("Phone number",max_length=20)
    age = models.IntegerField("Age",null=True,blank=True)
    gender = models.CharField("Gender",max_length=10,choices=gender_choices)
    photo = models.ImageField("Photo",null=True,blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip_code = models.CharField("Zip Code",max_length=20,null=True,blank=True)
    country = models.CharField(max_length=20)
    user_type = ArrayField(models.CharField(max_length=255,choices=user_type_choices),null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    deleted_at = models.DateTimeField(null=True,blank=True)
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.full_name
    

    def imageURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url
    

class NepaliExtraClasses(models.TextChoices):
    Dance_Classes = 'Dance Classes', 'Dance Classes'
    Music_Classes = 'Music Classes', 'Music Classes'
    
    
CURRENT_STATUS_CHOICES = (
    ("Enrolled","Enrolled"),
    ("Paused","Paused"),
    ("Dropped","Dropped"),
    ("Not Enrolled","Not Enrolled"),
    ("Not Interested","Not Interested"),
    ("Other","Other"),
)

class NepaliStudent(models.Model):
    
    course_level=[
        ('L0','Get comfortable before learnign alphabets'),
        ('L1 White','Learn Alphabets'),
        ('L2 Orange','Learn Alphabets and words'),
        ('L3 Blue','Learn Alphabets, words and sentences'),
        ('L4 Yellow','Learn Alphabets, words, sentences and reading'),
    ]
    
   
    nepali_speaking_at_home = [
        ('Always','Always'),
        ('Sometimes','Sometimes'),
        ('Never','Never'),
    ]
    



    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='nepali_student')
    signing_for = models.CharField(max_length=20)
    parents_name = models.CharField(max_length=50)
    nepali_at_home = models.CharField(max_length=15,choices=nepali_speaking_at_home)
    listening = models.CharField(max_length=1,choices=skills)
    speaking = models.CharField(max_length=1,choices=skills)
    reading = models.CharField(max_length=1,choices=skills)
    writing = models.CharField(max_length=1,choices=skills)
    course_level = models.CharField(max_length=20,choices=course_level)
    session_type = models.CharField(max_length=32,choices=session_choices)
    class_time = MultiSelectField(choices=ClassTime.choices,max_choices=3,max_length=100,blank=True,null=True)
    goal_for_class = models.TextField(null=True)
    special_request = models.TextField(null=True,blank=True)
    hear_from = models.CharField(max_length=30)
    other_classes = MultiSelectField(max_length=50,choices=NepaliExtraClasses.choices,max_choices=2,blank=True,null=True)
    current_status = models.CharField(max_length=15,null=True,blank=True,choices=CURRENT_STATUS_CHOICES,default='Not Enrolled')

    def __str__(self):
        return self.user.full_name
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)

    


class DanceExtraClasses(models.TextChoices):
        Nepali_Classes = 'Nepali Classes', 'Nepali Classes'
        Music_Classes = 'Music Classes', 'Music Classes'


class DanceStudent(models.Model):
    dance_style_choice =[
        ('Nepali Classical Dance','Nepali Classical Dance'),
        ('Nepali Folk/Freestyle/Fusion','Nepali Folk/Freestyle/Fusion'),
        ('Indian Classical Dance','Indian Classical Dance'),
        ('Bollywood Dance','Bollywood Dance'),
    ]
    
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='dance_student')
    signing_for = models.CharField(max_length=20)
    parents_name = models.CharField(max_length=50)
    dance_skills = models.CharField(max_length=1,choices=skills)
    dance_style = models.CharField(max_length=30,choices=dance_style_choice)
    session_type = models.CharField(max_length=32,choices=session_choices)
    class_time = MultiSelectField(choices=ClassTime.choices,max_choices=3,max_length=100)
    goal_for_class = models.TextField(null=True)
    special_request = models.TextField(null=True,blank=True)
    hear_from = models.CharField(max_length=30)
    other_classes = MultiSelectField(max_length=50,choices=DanceExtraClasses.choices,max_choices=2,blank=True,null=True)

    def __str__(self):
        return self.user.full_name
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)


teacher_choices = [
        ('Nepali Teacher','Nepali Teacher'),
        ('Dance Teacher','Dance Teacher'),
]


class Teacher(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_type = models.CharField(max_length=20,choices=teacher_choices)
    zoom_link = models.URLField(max_length=250)
    

    def __str__(self):
        return self.user.full_name
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)









class Token(AuthToken):
    key = models.CharField("Key", max_length=128, db_index=True, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="auth_token",
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    expiration_date = models.DateTimeField()
    # user_agent = UserAgentField()

    def save(self, *args, **kwargs):
        if self.expiration_date is None:
            self.expiration_date = timezone.now() + datetime.timedelta(days=30)
        super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email
    




# class (models.Model):

    

#     class Meta:
#         verbose_name = _("")
#         verbose_name_plural = _("s")

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("_detail", kwargs={"pk": self.pk})



class OPT(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.full_name
    



class VideoUpload(models.Model):
    video = models.FileField(upload_to='videos/',null=True,blank=True)
    adminVideo = models.FileField(upload_to='adminVideos/',null=True,blank=True)
    clientVideo = models.FileField(upload_to='clientVideos/',null=True,blank=True)
    
    
    