from django.db import models
import datetime
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.conf import settings
from .managers import UserManager,NepaliStudentManager,DanceStudentManager
from django.contrib.auth.models import AbstractBaseUser, Group,AbstractUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission,Group
from rest_framework.authtoken.models import Token as AuthToken


# Create your models here.


gender_choices = [
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other'),
    ]

skills = [
        ('0','0'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    ]

session_choices=[
        ('Group Class 1 seesion per week','Group Class 1 session per week'),
        ('Group Class 2 seesion per week','Group Class 2 session per week'),
        ('One-One class 1 session per week','One-One class 1 session per week'),
        ('One-One class 2 session per week','One-One class 2 session per week'),
    ]
class_timing = [
        ('Sunday Morning','Sunday Morning'),
        ('Sunday Evening','Sunday Evening'),
        ('Monday Morning','Monday Morning'),
        ('Monday Evening','Monday Evening'),
        ('Tuesday Morning','Tuesday Morning'),
        ('Tuesday Evening','Tuesday Evening'),
        ('Wednesday Morning','Wednesday Morning'),
        ('Wednesday Evening','Wednesday Evening'),
        ('Thursday Morning','Thursday Morning'),
        ('Thursday Evening','Thursday Evening'),
        ('Friday Morning','Friday Morning'),
        ('Friday Evening','Friday Evening'),
        ('Saturday Morning','Saturday Morning'),
        ('Saturday Evening','Saturday Evening'),
    ]

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10,choices=gender_choices)
    photo = models.ImageField(null=True,blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return self.email

class NepaliStudent(models.Model):
    
    course_level=[
        ('L0','Get comfortable before learnign alphabets'),
        ('L1 White','Learn Alphabets'),
        ('L2 Orange','Learn Alphabets and words'),
        ('L3 Blue','Learn Alphabets, words and sentences'),
        ('L4 Yellow','Learn Alphabets, words, sentences and reading'),
    ]
    
    extra_classes = [
        ('Dance Classes','Dance Classes'),
        ('Music Classes','Music Classes'),
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
    class_time = MultiSelectField(choices=class_timing,max_choices=3,max_length=100)
    goal_for_class = models.TextField(null=True)
    hear_from = models.CharField(max_length=30)
    special_request = models.TextField(null=True,blank=True)
    other_classes = MultiSelectField(max_length=15,choices=extra_classes,max_choices=2)
    is_nepali_student = models.BooleanField(default=True)
    

    def __str__(self):
        return self.user.email

    


class DanceStudent(models.Model):
    dance_style_choice =[
        ('Nepali Classical Dance','Nepali Classical Dance'),
        ('Nepali Folk/Freestyle/Fusion','Nepali Folk/Freestyle/Fusion'),
        ('Indian Classical Dance','Indian Classical Dance'),
        ('Bollywood Dance','Bollywood Dance'),
    ]
    
    extra_classes = [
        ('Nepali Classes','Nepali Classes'),
        ('Music Classes','Music Classes'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    signing_for = models.CharField(max_length=20)
    parents_name = models.CharField(max_length=50)
    dance_skills = models.CharField(max_length=1,choices=skills)
    dance_style = models.CharField(max_length=30,choices=dance_style_choice)
    session_type = models.CharField(max_length=32,choices=session_choices)
    class_time = MultiSelectField(choices=class_timing,max_choices=3,max_length=100)
    goal_for_class = models.TextField(null=True)
    hear_from = models.CharField(max_length=30)
    special_request = models.TextField(null=True,blank=True)
    other_classes = MultiSelectField(max_length=15,choices=extra_classes,max_choices=2)
    is_dance_student = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email


teacher_choices = [
        ('Nepali Teacher','Nepali Teacher'),
        ('Dance Teacher','Dance Teacher'),
]


class Teacher(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_type = models.CharField(max_length=20,choices=teacher_choices)
    zoom_link = models.URLField(max_length=250)
    is_teacher = models.BooleanField(default=True)
    

    def __str__(self):
        return self.user.email





class ManagementStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_management_staff = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email



class Token(AuthToken):
    key = models.CharField("Key", max_length=128, db_index=True, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="auth_token",
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    expiration_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.expiration_date is None:
            self.expiration_date = timezone.now() + datetime.timedelta(days=30)
        super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email