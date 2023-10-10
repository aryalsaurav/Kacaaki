from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import User,NepaliStudent,DanceStudent,Teacher
from .forms import *

# Create your views here.


def teachers_list(request):
    template_name = "users/teachers_list.html"
    teachers = Teacher.objects.filter(user__is_active=True).all()
    context = {
        'teachers':teachers
    }
    return render(request,template_name,context)


class UserRegistrationView(View):
    template_name = "users/user_registration.html"

    def get(self,request):
        
        context = {
            'form':UserRegistrationForm()
        }
        return render(request,self.template_name,context)

    def post(self,request):
        form = UserRegistrationForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,"Registration Successful")
            return HttpResponseRedirect('/')
        else:
            messages.error(request,"Registration Failed")
            return render(request,self.template_name,{'form':form})