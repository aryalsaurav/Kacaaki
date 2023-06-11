from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from users.models import User, NepaliStudent, DanceStudent, Teacher
# Create your models here.



class NepaliClass(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    teacher = models.ForeignKey(Teacher,limit_choices_to={'teacher_type':'Nepali Teacher'}, on_delete=models.CASCADE)
    students = models.ManyToManyField(NepaliStudent, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name



    


class DanceClass(models.Model):
    name = models.CharField(max_length=100, unique=True)
    teacher = models.ForeignKey(Teacher,limit_choices_to={'teacher_type':'Dance Teacher'}, on_delete=models.CASCADE)
    students = models.ManyToManyField(DanceStudent, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


