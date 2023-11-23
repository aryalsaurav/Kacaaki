from django.shortcuts import render, redirect,HttpResponseRedirect,get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import *
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from main.permissions import *
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
# Create your views here.





class NepaliClassAddView(LoginRequiredMixin,View):
    template_name = 'classes/nepaliclass/nepaliclass_add.html'
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        form = NepaliClassForm(user=request.user)
        context = {
            'form':form,
        }
        return render(request, self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        form = NepaliClassForm(request.POST, user=request.user)
        if form.is_valid():
            np_class = form.save(commit=False)
            students = form.cleaned_data['students']
            if students.count() > 5:
                messages.error(request, 'You cannot add more than 4 students')
                return HttpResponseRedirect(reverse('classes:nepaliclass_add'))
            try:
                np_class.teacher = request.user.teacher
            except:
                raise PermissionDenied
            np_class.save()
            np_class.students.add(*students)
            np_class.save()
            messages.success(request, 'Class added successfully')
            return redirect('classes:nepaliclass_list')
        else:
            messages.error(request, 'Class not added')
            return redirect('classes:nepaliclass_list')
        
        


class NepaliClassListView(LoginRequiredMixin,ListView):
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
        queryset = []
        try:
            if self.request.user.is_superuser or self.request.user.is_staff:
                queryset = classes.filter(
                        Q(name__icontains=query) |
                        Q(day__icontains=query) |
                        Q(time__icontains=query) |
                        Q(teacher__user__full_name__icontains=query)|
                        Q(students__user__full_name__icontains=query)
                    ).distinct()
            elif self.request.user.teacher:
                
                queryset =  classes.filter(teacher=self.request.user.teacher).filter(
                        Q(name__icontains=query) |
                        Q(day__icontains=query) |
                        Q(time__icontains=query) |
                        Q(teacher__user__full_name__icontains=query)|
                        Q(students__user__full_name__icontains=query)
                    ).distinct()
        except:
            pass
        try:
            queryset = classes.filter(students__in= [self.request.user.nepali_student]).filter(
                    Q(name__icontains=query) |
                    Q(day__icontains=query) |
                    Q(time__icontains=query) |
                    Q(teacher__user__full_name__icontains=query)|
                    Q(students__user__full_name__icontains=query)
                ).distinct()
        except:
            pass
            
        
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Pass the query to the context
        
        return context
                
        
        
        # paginator = Paginator(np_classes, self.paginate_by)
        # page_number = request.GET.get('page')
        
        

class NepaliClassUpdateView(LoginRequiredMixin,View):
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
        detail = request.POST.get('uid')
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
            if detail == 'detail':
                
                return HttpResponseRedirect(reverse('classes:nepaliclass_detail', kwargs={'pk':self.kwargs['pk']}))
            else:
                return redirect('classes:nepaliclass_list')
        else:
            print(form.errors)
            messages.error(request, 'Class not updated')
            return redirect('classes:nepaliclass_list')
        




class NepaliClassDeleteView(LoginRequiredMixin,View):
    
    def get(self,request,*args,**kwargs):
        np_class = get_object_or_404(NepaliClass, pk=self.kwargs['pk'])
        np_class.delete()
        messages.success(request, 'Class deleted successfully')
        return redirect('classes:nepaliclass_list')
    
    
    

class NepaliClassDetailView(LoginRequiredMixin,InClassOrAdminMixin,View):
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
    template_name = 'classes/nepaliclass/assignment/assignment_add.html'
    def get(self,request,*args,**kwargs):
        form = AssignmentForm()
        context = {
            'form':form,
        }
        return render(request, self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        form = AssignmentForm(request.POST, request.FILES)
        class_id = request.POST.get('uid')
        print(class_id)
        if form.is_valid():
            assignment = form.save(commit=False)
            nepali_class = NepaliClass.objects.get(pk=class_id)
            try:
                if not request.user.nepali_student in nepali_class.students.all():
                    raise PermissionDenied
            except:
                pass
            assignment.nepali_class = nepali_class
            assignment.save()
            messages.success(request, 'Assignment added successfully')
            return redirect('classes:nepaliclass_detail', pk=nepali_class.pk)
        else:
            messages.error(request, 'Assignment not added')
            print(form.errors)
            return render(request, self.template_name, {'form':form})
        


class AssignmentListView(LoginRequiredMixin,ListView):
    template_name = 'classes/nepaliclass/assignment/assignment_list.html'
    model = Assignment
    paginate_by = 10
    
    def get_queryset(self):
        class_id = self.request.GET.get('uid')
        if class_id:
            queryset =  super().get_queryset().filter(Q(nepali_class__teacher__user=self.request.user) | Q(nepali_class__students__user=self.request.user) |Q(nepali_class__id=class_id)).order_by('-created_at')
            if self.request.GET.get('q'):
                query = self.request.GET.get('q')
                return queryset.filter(
                        Q(topic__icontains=query) 
                    )
            return queryset
        else:
            return Assignment.objects.none()
        
    
    def get(self,*args,**kwargs):
        values = self.request.GET.get('uid')
        if not values:
            return HttpResponseRedirect(reverse_lazy('classes:nepaliclass_list'))
        else:
            return super().get(*args,**kwargs)
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['value'] = self.request.GET.get('uid', '')
        return context
    
    

class AssignmentDetailView(View):
    template_name = 'classes/nepaliclass/assignment/assignment_detail.html'
    def get(self,request,*args,**kwargs):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        assignment_submissions = AssignmentSubmission.objects.filter(assignment=assignment)
        context = {
            'assignment':assignment,
            'assignment_submissions':assignment_submissions,
        }
        return render(request, self.template_name, context)
    
    
class AssignmentUpdateView(View):
    template_name = 'classes/nepaliclass/assignment/assignment_update.html'
    def get(self,request,*args,**kwargs):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        form = AssignmentForm(instance=assignment)
        context = {
            'form':form,
        }
        return render(request, self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        assignment = get_object_or_404(Assignment, pk=self.kwargs['pk'])
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.save()
            messages.success(request, 'Assignment updated successfully')
            return redirect('classes:assignment_detail', pk=assignment.pk)
        else:
            messages.error(request, 'Assignment not updated')
            print(form.errors)
            return render(request, self.template_name, {'form':form})
    