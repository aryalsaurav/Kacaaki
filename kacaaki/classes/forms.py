from django import forms
from .models import *
from users.models import *
from django.core.exceptions import ValidationError
from django.utils import timezone
from dal import autocomplete



class NepaliClassForm(autocomplete.FutureModelForm):
    
    students  = forms.ModelMultipleChoiceField(
        queryset=NepaliStudent.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='classes:nepali-student-autocomplete')
    )
    class Meta:
        model = NepaliClass
        fields = ('name', 'teacher', 'students',)
        # widgets = {
        #     'name': forms.TextInput(attrs={'class':'form-control'}),
        #     'teacher': forms.Select(attrs={'class':'form-control'}),
        #     'students': autocomplete.ModelSelect2Multiple(url='classes:nepali-student-autocomplete')
        # }
        
    # def __init__(self, *args, **kwargs):
    #     super(NepaliClassForm, self).__init__(*args, **kwargs)
    #     self.fields['teacher'].queryset = Teacher.objects.filter(teacher_type='Nepali Teacher')

        # for field in iter(self.fields):
        #     if field == "students":
        #         self.fields[field].queryset = NepaliStudent.objects.filter(user__is_active=True)
        #         self.fields[field].widget.attrs.update({
        #             'class': 'select2',
        #             'data-placeholder': 'Autocomplete ...',
        #             'data-minimum-input-length': 3,
        #         })
        # self.fields['students'].queryset = NepaliStudent.objects.filter(user__is_active=True)

        # for field in self.fields:
        #     self.fields[field].widget.attrs['class'] = 'form-control'
