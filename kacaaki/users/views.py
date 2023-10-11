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


class NepaliStudentRegisterView(View):
    template_name = "users/nepali_student_registration.html"

    def get(self,request):
        
        context = {
            'user_form':UserRegistrationForm(),
            'nepali_student':NepaliStudentRegistrationForm(),
        }
        return render(request,self.template_name,context)

    def post(self,request):
        user_form = UserRegistrationForm(request.POST,request.FILES)
        nepali_student_form = NepaliStudentRegistrationForm(request.POST)
        if user_form.is_valid() and nepali_student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            nepali_student = nepali_student_form.save(commit=False)
            nepali_student.user = user
            nepali_student.is_nepali_student = True
            nepali_student.save()
            messages.success(request,"Your account has been created successfully")
            return HttpResponseRedirect('/')
        else:
            messages.error(request,"Please correct the error below")
            context = {
            'user_form':user_form,
            'nepali_student':nepali_student_form,
            }
            return render(request,self.template_name,context)
        

class DanceStudentRegisterView(View):
    template_name = "users/dance_student_registration.html"

    def get(self,request):
        
        context = {
            'user_form':UserRegistrationForm(),
            'dance_student':DanceStudentRegistrationForm(),
        }
        return render(request,self.template_name,context)

    def post(self,request):
        user_form = UserRegistrationForm(request.POST,request.FILES)
        dance_student_form = DanceStudentRegistrationForm(request.POST)
        if user_form.is_valid() and dance_student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            dance_student = dance_student_form.save(commit=False)
            dance_student.user = user
            dance_student.is_dance_student = True
            dance_student.save()
            messages.success(request,"Your account has been created successfully")
            return HttpResponseRedirect('/')
        else:
            messages.error(request,"Please correct the error below")
            context = {
            'user_form':user_form,
            'dance_student':dance_student_form,
            }
            return render(request,self.template_name,context)