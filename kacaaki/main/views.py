from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from users.models import User,NepaliStudent,DanceStudent,Teacher
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import *


import logging

from classes.models import NepaliClass

logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
    template_name = "layouts/base.html"
    return render(request,template_name)


def about_us(request):
    logger.info("About us page visited")
    template_name = "layouts/about_us.html"
    return render(request,template_name)


class ContactUsView(View):
    template_name = "layouts/contact_us.html"

    def get(self,request):
        template_name = "layouts/contact_us.html"
        return render(request,template_name,{'forms':ContactForm()})

    def post(self,request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your message has been sent successfully.")
            return HttpResponseRedirect("/contact-us")
        else:
            
            return HttpResponseRedirect("/contact-us")
        

class TestomonialListView(View):
    template_name = "layouts/testomonials.html"

    def get(self,request,*args,**kwargs):
        testomonials = Testomonial.objects.all().order_by('-created_at')
        context = {
            'testomonials':testomonials
        }
        return render(request,self.template_name,context)
    
    





class LoginView(View):
    template_name = "layouts/login.html"


    def get(self,request):
        if request.user.is_authenticated:
            print("user is authenticated")
            return redirect("/")
        else:
            return render(request,self.template_name)

    def post(self,request,*args,**kwargs):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = username,password=password)
        next_url = request.POST.get('next')
        print("next",next_url)
        if user:
            login(request,user)
            # next_url = kwargs.get('next')

            
            if next_url:
                return HttpResponseRedirect(next_url)  # Redirect to 'next' URL
            else:
                return HttpResponseRedirect(reverse('main:home'))
        else:
            messages.error(request,"Invalid username or password")
            return HttpResponseRedirect(reverse('main:login'))
        

def logout_view(request):
    logout(request)
    return redirect("/")



class DashboardView(View):
    template_name = "layouts/dashboard.html"

    def get(self,request):
        context = {}
        all_nepali_students = NepaliStudent.objects.all()
        context['total_nepali_students'] = all_nepali_students.count()
        context['total_enrolled_students'] = all_nepali_students.filter(current_status="Enrolled").count()
        context['pending_students'] = all_nepali_students.filter(current_status="Not Enrolled").count()
        context['paused_students'] = all_nepali_students.filter(current_status="Paused").count()
        context['dropped_students'] = all_nepali_students.filter(current_status="Dropped").count()
        context['total_nepali_classes'] = NepaliClass.objects.filter(deleted_at=None).count()
        return render(request,self.template_name,context)
        