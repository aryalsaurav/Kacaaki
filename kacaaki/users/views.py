from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import User,NepaliStudent,DanceStudent,Teacher

# Create your views here.


def teachers_list(request):
    template_name = "users/teachers_list.html"
    teachers = Teacher.objects.filter(user__is_active=True).all()
    context = {
        'teachers':teachers
    }
    return render(request,template_name,context)


