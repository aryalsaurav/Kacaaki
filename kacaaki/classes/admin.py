from django.contrib import admin
from .models import NepaliClass, DanceClass, Assignment, AssignmentSubmission, AssignmentFile

# Register your models here.

admin.site.register(NepaliClass)
admin.site.register(DanceClass)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(AssignmentFile)

