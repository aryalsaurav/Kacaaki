from django.shortcuts import render, redirect,HttpResponseRedirect,get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import *
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from dal import autocomplete

# Create your views here.



class StudentsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print("is this function being executed?")
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            print("none user")
            return NepaliStudent.objects.none()

        qs = NepaliStudent.objects.filter(students__user__is_active=True)

        if self.q:
            qs = qs.filter(students__user__full_name__icontains=self.q)
        print("hello ")

        print(qs)
        print("no qs")
        return qs

class NepaliClassAddView(LoginRequiredMixin,View):
    template_name = 'classes/nepaliclass_add.html'
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        form = NepaliClassForm()
        context = {
            'form':form,
        }
        return render(request, self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        form = NepaliClassForm(request.POST)
        if form.is_valid():
            np_class = form.save()

            messages.success(request, 'Class added successfully')
            return redirect('/')
        else:
            messages.error(request, 'Class not added')
            return redirect('classes:nepaliclass_list')