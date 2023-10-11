from django import forms
from crispy_forms.helper import FormHelper
from django.contrib import messages
from .models import *

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(),label="Confirm Password")
    class Meta:
        model = User
        fields = ['email','password','password2','full_name','phone','age','gender','photo','city','state','zip_code','country']


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError(
                "Password does not match"
            )
        return cleaned_data


        
class NepaliStudentRegistrationForm(forms.ModelForm):
    class_time = forms.MultipleChoiceField(widget=forms.SelectMultiple,choices=ClassTime.choices)
    # class_time = forms.MultipleChoiceField(choices=ClassTime.choices,widget=forms.SelectMultiple)
    # other_classes = forms.MultipleChoiceField(choices =NepaliExtraClasses.choices,widget=forms.SelectMultiple)
    class Meta:
        model = NepaliStudent
        exclude = ['is_nepali_student','user']

    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.helper = FormHelper()


class DanceStudentRegistrationForm(forms.ModelForm):
    class_time = forms.MultipleChoiceField(widget=forms.SelectMultiple,choices=ClassTime.choices)
    # class_time = forms.MultipleChoiceField(choices=ClassTime.choices,widget=forms.SelectMultiple)
    # other_classes = forms.MultipleChoiceField(choices =NepaliExtraClasses.choices,widget=forms.SelectMultiple)
    class Meta:
        model = DanceStudent
        exclude = ['is_dance_student','user']

    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.helper = FormHelper()