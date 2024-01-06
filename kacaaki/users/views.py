from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from classes.models import *

from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import User,NepaliStudent,DanceStudent,Teacher
from .forms import *
from dal import autocomplete

# Create your views here.

# class StudentsAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         # Don't forget to filter out results depending on the visitor !
#         if not self.request.user.is_authenticated:
#             return NepaliStudent.objects.none()

#         qs = NepaliStudent.objects.all()

#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)

#         return qs



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
            user.user_type = ["Nepali Student"]
            user.save()
            nepali_student = nepali_student_form.save(commit=False)
            nepali_student.user = user
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
            user.user_type = ["Dance Student"]
            user.save()
            dance_student = dance_student_form.save(commit=False)
            dance_student.user = user
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
        
        
        
class ProfileView(View):
    template_name = "users/profile.html"

    def get(self,request):
        if request.user.is_authenticated:
            user = request.user
            nepali_classes = None
            dance_classes = None
            if  "Nepali Student" in user.user_type :
                nepali_student = NepaliStudent.objects.get(user=user)
                nepali_classes = NepaliClass.objects.filter(students=nepali_student).all()
            elif "Dance Student" in user.user_type:
                dance_student = DanceStudent.objects.get(user=user)
                dance_classes = DanceClass.objects.filter(students=dance_student).all()
            elif "Nepali Teacher" in user.user_type:
                teacher = Teacher.objects.get(user=user)
                nepali_classes = NepaliClass.objects.filter(teacher=teacher).all()
            elif "Dance Teacher" in user.user_type:
                teacher = Teacher.objects.get(user=user)
                dance_classes = DanceClass.objects.filter(teacher=teacher).all()
            print(nepali_classes,'nepali_classes')
            context = {
                'user':user,
                'nepali_classes':nepali_classes,
                'dance_classes':dance_classes,
                
            }
            return render(request,self.template_name,context)
        else:
            return HttpResponseRedirect('/login')