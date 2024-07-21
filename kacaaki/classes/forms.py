from django import forms
from .models import *
from users.models import *
from django.core.exceptions import ValidationError
from django.utils import timezone
from dal import autocomplete



class NepaliClassForm(forms.ModelForm):
    time = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
    students = forms.ModelMultipleChoiceField(queryset=NepaliStudent.objects.all())
    
    class Meta:
        model = NepaliClass
        fields = ('name',"day","time",'class_type','teacher','students',)
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(NepaliClassForm, self).__init__(*args, **kwargs)
        # self.fields['teacher'].queryset = Teacher.objects.filter(teacher_type='Nepali Teacher')

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        
        if user and (user.is_superuser or user.is_staff):
            self.fields['teacher'].queryset = Teacher.objects.filter(teacher_type='Nepali Teacher')
        else:
            del self.fields['teacher']
            



class NepaliClassUpdateForm(forms.ModelForm):
    time = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))

    
    class Meta:
        model = NepaliClass
        fields = ('name',"day","time",'class_type','students')
        
    def __init__(self, *args, **kwargs):
        super(NepaliClassUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['teacher'].queryset = Teacher.objects.filter(teacher_type='Nepali Teacher')

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        
        
    
            
    

class AssignmentForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = Assignment
        fields = ['topic', 'file_f', 'deadline']
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            if field == "deadline":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control datetimepicker',
                
                    
                })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
        


class StudentForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=NepaliStudent.objects.all())
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })