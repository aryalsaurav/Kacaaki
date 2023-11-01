from django import forms
from .models import *
from users.models import *
from django.core.exceptions import ValidationError
from django.utils import timezone
from dal import autocomplete



class NepaliClassForm(forms.ModelForm):
    time = forms.CharField(widget=forms.TextInput(attrs={'type': 'time'}))
    students = forms.ModelMultipleChoiceField(queryset=NepaliStudent.objects.all())
    # teacher = forms.ModelChoiceField(queryset=Teacher.objects.filter(teacher_type='Nepali Teacher'))
    class Meta:
        model = NepaliClass
        fields = ('name',"day","time", 'teacher', 'students',)
        # widgets = {
        #     'name': forms.TextInput(attrs={'class':'form-control'}),
        #     'teacher': forms.Select(attrs={'class':'form-control'}),
        #     'students': autocomplete.ModelSelect2Multiple(url='classes:nepali-student-autocomplete')
        # }
        
    def __init__(self, *args, **kwargs):
        super(NepaliClassForm, self).__init__(*args, **kwargs)
        # self.fields['teacher'].queryset = Teacher.objects.filter(teacher_type='Nepali Teacher')

        for field in iter(self.fields):
            
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            
    
            
    
        
