from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from users.models import User, NepaliStudent, DanceStudent, Teacher
# Create your models here.



day_choices = (
    ('Sunday','Sunday'),
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday')
)


class_type_choices = (
    ('Group Class','Group Class'),
    ('One-One Class','One-One Class')
)
class NepaliClass(models.Model):
    
    name = models.CharField("Class Name",max_length=100, unique=True)
    day = models.CharField("Class Day",max_length=100,choices=day_choices)
    time = models.CharField("Class Time",max_length=100)
    class_type = models.CharField("Class Type",max_length=100,choices=class_type_choices)
    teacher = models.ForeignKey(Teacher,limit_choices_to={'teacher_type':'Nepali Teacher'}, on_delete=models.CASCADE)
    students = models.ManyToManyField(NepaliStudent)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.name
    
    
    
    # def save(self, *args, **kwargs):
    #     # Check if the instance is being updated
    #     is_update = self.pk is not None

    #     if is_update:
    #         # If this is an update, remove students from other instances
    #         for nepali_class in NepaliClass.objects.exclude(pk=self.pk):
    #             nepali_class.students.remove(*self.students.all())

    #     super(NepaliClass, self).save(*args, **kwargs)


    
    
    


class Assignment(models.Model):
    topic = models.CharField(max_length=250)
    file_f = models.FileField("File", upload_to='files/', blank=True, null=True)
    nepali_class = models.ForeignKey(NepaliClass, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.topic



class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE) 
    student = models.ForeignKey(NepaliStudent, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approval = models.CharField(max_length=15, choices=(('Approved','Approved'),('Rejected','Rejected'),('Submitted','Submitted')), default='Submitted')
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.assignment.topic + ' - ' + self.student.user.full_name

    class Meta:
        unique_together = ('assignment', 'student',)
        verbose_name_plural = 'Assignment Submissions'


    #automatically save the student to be the one who is logged in
    

    


class AssignmentFile(models.Model):
    assignment_submission = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE,related_name='assignment_files')
    a_file = models.FileField("Homework File",upload_to='assignments/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.assignment_submission.assignment.topic + ' - ' + self.assignment_submission.student.user.full_name
    


class DanceClass(models.Model):
    name = models.CharField(max_length=100, unique=True)
    day = models.CharField("Class Day",max_length=100,choices=day_choices)
    time = models.CharField("Class Time",max_length=100)
    class_type = models.CharField("Class Type",max_length=100,choices=class_type_choices)
    teacher = models.ForeignKey(Teacher,limit_choices_to={'teacher_type':'Dance Teacher'}, on_delete=models.CASCADE)
    students = models.ManyToManyField(DanceStudent, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    

    
    



class DanceAssignment(models.Model):
    topic = models.CharField(max_length=250)
    dance_class = models.ForeignKey(DanceClass, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.topic




