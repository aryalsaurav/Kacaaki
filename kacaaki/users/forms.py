from django import forms
from crispy_forms.helper import FormHelper
from django.contrib import messages
from .models import *
from dal import autocomplete

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(),label="Confirm Password")
    class Meta:
        model = User
        fields = ['email','full_name','password','password2','phone','age','gender','photo','city','state','zip_code','country']


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError(
                "Password does not match"
            )
        return cleaned_data
    
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })



class_time_choices = (
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
)
        
class NepaliStudentRegistrationForm(forms.ModelForm):
    class_time = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control'}),choices=class_time_choices)
    class Meta:
        model = NepaliStudent
        exclude = ['is_nepali_student','user']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })


class DanceStudentRegistrationForm(forms.ModelForm):
    class_time = forms.MultipleChoiceField(widget=autocomplete.SelectMultiple,choices=ClassTime.choices)
    # class_time = forms.MultipleChoiceField(choices=ClassTime.choices,widget=forms.SelectMultiple)
    # other_classes = forms.MultipleChoiceField(choices =NepaliExtraClasses.choices,widget=forms.SelectMultiple)
    class Meta:
        model = DanceStudent
        exclude = ['is_dance_student','user']

    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.helper = FormHelper()