from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from users.models import User,NepaliStudent,DanceStudent,Teacher
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *

# Create your views here.

def home(request):
    template_name = "layouts/base.html"
    return render(request,template_name)


def about_us(request):
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
            return redirect("/")
        else:
            return render(request,self.template_name)

    def post(self,request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = username,password=password)
        if user:
            login(request,user)
            messages.success(request,"You are logged in.")
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Invalid username or password.")
        

def logout_view(request):
    logout(request)
    return redirect("/")