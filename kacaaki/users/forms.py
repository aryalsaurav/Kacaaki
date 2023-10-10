from django import forms
from .models import *

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','password','full_name','phone','age','gender','photo','city','state','zip_code','country']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            if field == "password":
                self.fields[field].widget.attrs.update(
                    {'class':'form-control',
                     'placeholder':'Enter Password',
                        'type':'password'})
            
            #show gender choices options
            else:
                self.fields[field].widget.attrs.update(
                    {
                        'class':'form-control',
                        'placeholder':f'Enter {field.title()}',
                    })


        
