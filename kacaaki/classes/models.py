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


class Assignment(models.Model):
    topic = models.CharField(max_length=250)
    nepali_class = models.ForeignKey(NepaliClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic



class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    
    student = models.ForeignKey(NepaliStudent, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.assignment.topic + ' - ' + self.student.user.full_name



    class Meta:
        unique_together = ('assignment', 'student',)
        verbose_name_plural = 'Assignment Submissions'

    

    


class AssignmentFile(models.Model):
    assignment_submission = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE)
    a_file = models.FileField(upload_to='assignments/')

    def __str__(self):
        return self.assignment_submission.assignment.topic + ' - ' + self.assignment_submission.student.user.full_name
    


class DanceClass(models.Model):
    name = models.CharField(max_length=100, unique=True)
    teacher = models.ForeignKey(Teacher,limit_choices_to={'teacher_type':'Dance Teacher'}, on_delete=models.CASCADE)
    students = models.ManyToManyField(DanceStudent, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name





