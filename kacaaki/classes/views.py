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
from main.permissions import *
from django.core.paginator import Paginator

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

class NepaliClassAddView(NepaliTeacherMixin,LoginRequiredMixin,View):
    template_name = 'classes/nepaliclass/nepaliclass_add.html'
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
            np_class = form.save(commit=False)
            students = form.cleaned_data['students']
            if students.count() > 5:
                messages.error(request, 'You cannot add more than 4 students')
                return HttpResponseRedirect(reverse('classes:nepaliclass_add'))
            
            np_class.save()
            np_class.students.add(*students)
            np_class.save()
            messages.success(request, 'Class added successfully')
            return redirect('classes:nepaliclass_list')
        else:
            messages.error(request, 'Class not added')
            return redirect('classes:nepaliclass_list')
        
        


class NepaliClassListView(NepaliTeacherMixin,LoginRequiredMixin,ListView):
    template_name = 'classes/nepaliclass/nepaliclass_list.html'
    login_url = '/login/'
    model = NepaliClass
    paginate_by = 10
    
    def get_queryset(self):
        
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
        else:
            query = ''
        classes = super().get_queryset()
        
        if self.request.user.is_superuser or self.request.user.is_staff:
            queryset = classes.filter(
                    Q(name__icontains=query) |
                    Q(day__icontains=query) |
                    Q(time__icontains=query) |
                    Q(teacher__user__full_name__icontains=query)|
                    Q(students__user__full_name__icontains=query)
                ).distinct()
        else:
            queryset =  classes.filter(teacher=self.request.user.teacher).filter(
                    Q(name__icontains=query) |
                    Q(day__icontains=query) |
                    Q(time__icontains=query) |
                    Q(teacher__user__full_name__icontains=query)|
                    Q(students__user__full_name__icontains=query)
                ).distinct()
        
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Pass the query to the context
        
        return context
                
        
        
        # paginator = Paginator(np_classes, self.paginate_by)
        # page_number = request.GET.get('page')
        
        

class NepaliClassUpdateView(LoginRequiredMixin,TeacherInNepaliClass,View):
    template_name = "classes/nepaliclass/nepaliclass_update.html"
    login_url = '/login/'
    
    def get(self,request,*args,**kwargs):
        np_classes = get_object_or_404(NepaliClass, pk=self.kwargs['pk'])
        form = NepaliClassForm(instance=np_classes)
        context = {
            'form':form,
        }
        return render(request, self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        np_classes = get_object_or_404(NepaliClass, pk=self.kwargs['pk'])
        detail = request.POST.get('where')
        form = NepaliClassForm(request.POST, instance=np_classes)
        if form.is_valid():
            np_class = form.save(commit=False)
            students = form.cleaned_data['students']
            if students.count() > 5:
                messages.error(request, 'You cannot add more than 4 students')
                return HttpResponseRedirect(reverse('classes:nepaliclass_add'))
            np_class.save()
            np_class.students.add(*students)
            np_class.save()
            messages.success(request, 'Class updated successfully')
            if detail:
                
                return HttpResponseRedirect(reverse('classes:nepaliclass_detail', kwargs={'pk':self.kwargs['pk']}))
            else:
                return redirect('classes:nepaliclass_list')
        else:
            print(form.errors)
            messages.error(request, 'Class not updated')
            return redirect('classes:nepaliclass_list')
        




class NepaliClassDeleteView(LoginRequiredMixin,TeacherInNepaliClass, View):
    
    def get(self,request,*args,**kwargs):
        np_class = get_object_or_404(NepaliClass, pk=self.kwargs['pk'])
        np_class.delete()
        messages.success(request, 'Class deleted successfully')
        return redirect('classes:nepaliclass_list')
    
    
    

class NepaliClassDetailView(LoginRequiredMixin,TeacherInNepaliClass,View):
    template_name = 'classes/nepaliclass/nepaliclass_detail.html'
    login_url = '/login/'
    model = NepaliClass
    paginate_by = 1
    
    def get(self,request,*args,**kwargs):
        np_class = get_object_or_404(NepaliClass, pk=self.kwargs['pk'])
        assignments = Assignment.objects.filter(nepali_class=np_class).order_by('-created_at')[:10]
        context = {
            'np_class':np_class,
            'object_list':assignments,
        }
        return render(request, self.template_name, context)

    



class AssignmentAddView(LoginRequiredMixin,View):
    template_name = 'classes/nepaliAssignment/assignment_add.html'
    def get(self,request,*args,**kwargs):
        form = AssignmentForm()
        context = {
            'form':form,
        }
        return render(request, self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            nepali_class = NepaliClass.objects.get(pk=request.POST.get('class'))
            assignment.nepali_class = nepali_class
            assignment.save()
            messages.success(request, 'Assignment added successfully')
            return redirect('classes:nepaliclass_detail', pk=nepali_class.pk)
        else:
            messages.error(request, 'Assignment not added')
            print(form.errors)
            return render(request, self.template_name, {'form':form})