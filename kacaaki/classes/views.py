from django.db.models.query import QuerySet
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
from .mixins import (
    SuperUserRequiredMixin,
    StaffRequiredMixin,
    TeacherRequiredMixin,
    StaffOrNepaliTeacherRequiredMixin,
    NepaliTeacherOrStudentRequiredMixin,
    NeapliTeacherOrStudentInClassRequiredMixin,
)
from django.template.loader import render_to_string
from main.utils import send_email_task
from .utils import find_next_weekday_date
# Create your views here.





class NepaliClassAddView(LoginRequiredMixin,StaffOrNepaliTeacherRequiredMixin, View):
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
            for student in students:
                student.current_status = 'Enrolled'
                student.save()
            messages.success(request, 'Class added successfully')
            return redirect('classes:nepaliclass_list')
        else:
            messages.error(request, 'Class not added')
            return redirect('classes:nepaliclass_list')
        



class DashboardNepaliClassListView(LoginRequiredMixin,ListView):
    template_name = 'classes/nepaliclass/dashboard_nepaliclass_list.html'
    login_url = '/login/'
    model = NepaliClass
    paginate_by = 20
    
    def get_queryset(self,*args,**kwargs):
        queryset =  super().get_queryset().filter(deleted_at=None).order_by('-created_at')
        teacher = self.request.GET.get('teacher',None)
        class_type = self.request.GET.get('class_type',None)
        student = self.request.GET.get('student',None)
        time = self.request.GET.get('time',None)
        query = (Q(teacher__id=teacher) if teacher else Q()) & (Q(class_type=class_type) if class_type else Q()) & (Q(students__id=student) if student else Q()) & (Q(time=time) if time else Q())
        queryset = queryset.filter(query)
        
        return queryset
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['teachers'] = Teacher.objects.filter(user__deleted_at=None).all()
        context['students'] = NepaliStudent.objects.filter(user__deleted_at=None).all()
        return context


class NepaliClassListView(LoginRequiredMixin,NepaliTeacherOrStudentRequiredMixin,ListView):
    template_name = 'classes/nepaliclass/nepaliclass_list.html'
    
    login_url = '/login/'
    model = NepaliClass
    paginate_by = 10
    
    
    
    def get_queryset(self):
        
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
        else:
            query = ''
        classes = super().get_queryset().select_related('teacher')
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
            elif 'Nepali Teacher' in self.request.user.user_type :
                
                queryset =  classes.filter(teacher=self.request.user.teacher).filter(
                        Q(name__icontains=query) |
                        Q(day__icontains=query) |
                        Q(time__icontains=query) |
                        Q(teacher__user__full_name__icontains=query)|
                        Q(students__user__full_name__icontains=query)
                    ).distinct()
            
            elif 'Nepali Student' in self.request.user.user_type:
                queryset = classes.filter(students__in= [self.request.user.nepali_student]).filter(
                    Q(name__icontains=query) |
                    Q(day__icontains=query) |
                    Q(time__icontains=query) |
                    Q(teacher__user__full_name__icontains=query)|
                    Q(students__user__full_name__icontains=query)
                ).distinct()
        except:
            return classes.none()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Pass the query to the context
        return context
                
        
        
        # paginator = Paginator(np_classes, self.paginate_by)
        # page_number = request.GET.get('page')
        
        

class NepaliClassUpdateView(LoginRequiredMixin,StaffOrNepaliTeacherRequiredMixin, View):
    template_name = "classes/nepaliclass/nepaliclass_update.html"
    login_url = '/login/'
    
    def get(self,request,*args,**kwargs):
        np_classes = get_object_or_404(NepaliClass, pk=self.kwargs['pk'])
        form = NepaliClassUpdateForm(instance=np_classes)
        context = {
            'form':form,
        }
        return render(request, self.template_name, context)
    
    def post(self,request,*args,**kwargs):
        np_classes = get_object_or_404(NepaliClass, pk=self.kwargs['pk'])
        detail = request.POST.get('uid')
        form = NepaliClassUpdateForm(request.POST, instance=np_classes)
        if form.is_valid():
            students = form.cleaned_data['students']
            np_class = form.save(commit=False)
            np_class.save()
            if students.count() > 5:
                messages.error(request,"You cannot add more than 4 students")
            np_class.students.set(students)
            np_class.save()
            messages.success(request, 'Class updated successfully')
            if detail == 'detail':
                return HttpResponseRedirect(reverse('classes:nepaliclass_detail', kwargs={'pk':self.kwargs['pk']}))
            else:
                return redirect('classes:nepaliclass_list')
        else:
            messages.error(request, 'Class not updated')
            return HttpResponseRedirect(reverse('classes:nepaliclass_list'))
        




class NepaliClassDeleteView(LoginRequiredMixin,StaffOrNepaliTeacherRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        np_class = get_object_or_404(NepaliClass, pk=self.kwargs['pk'])
        np_class.delete()
        messages.success(request, 'Class deleted successfully')
        return redirect('classes:nepaliclass_list')
    
    
    

class NepaliClassDetailView(LoginRequiredMixin,NeapliTeacherOrStudentInClassRequiredMixin,View):
    template_name = 'classes/nepaliclass/nepaliclass_detail.html'
    login_url = '/login/'
    model = NepaliClass
    
    def get(self,request,*args,**kwargs):
        np_class = get_object_or_404(NepaliClass, pk=self.kwargs['pk'])
        assignments = Assignment.objects.filter(nepali_class=np_class).order_by('-created_at')[:10]
        
        context = {
            'np_class':np_class,
            'object_list':assignments,
            'form':StudentForm(),
            'students':NepaliStudent.objects.filter(user__deleted_at=None).all(),
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
        file = request.FILES.get('file')
        print(file,'dddddddddd')
        class_id = request.POST.get('uid')
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
            redirect_url = reverse('classes:assignment_list') + f'?uid={class_id}'
            return HttpResponseRedirect(redirect_url)
        else:
            messages.error(request, 'Assignment not added')
            print(form.errors)
            return render(request, self.template_name, {'form':form})
        


class AssignmentListView(LoginRequiredMixin,NeapliTeacherOrStudentInClassRequiredMixin,ListView):
    template_name = 'classes/nepaliclass/assignment/assignment_list.html'
    model = Assignment
    paginate_by = 10
    
    def get_queryset(self):
        class_id = self.request.GET.get('uid')
        if class_id:
            queryset =  super().get_queryset().filter(nepali_class__pk=class_id).order_by('-created_at')
            queryset =  queryset.filter(Q(nepali_class__teacher__user=self.request.user) | Q(nepali_class__students__user=self.request.user)).order_by('-created_at')
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
    
    
class AssignmentSubmissionView(LoginRequiredMixin,View):
    template_name = 'classes/nepaliclass/assignment/assignment_submission.html'
    def get(self,request,*args,**kwargs):
        return render(request, self.template_name)
    
    def post(self,request,*args,**kwargs):
        files = request.FILES.getlist('file')
        print(files)
        assignment_id = request.POST.get('uid')
        try:
            assignment = Assignment.objects.get(pk=assignment_id)
            if not request.user.nepali_student in assignment.nepali_class.students.all():
                raise PermissionDenied
            assignment_submission,_ = AssignmentSubmission.objects.get_or_create(assignment=assignment, student=request.user.nepali_student)
            assignment_file = AssignmentFile.objects.filter(assignment_submission=assignment_submission)
            if assignment_file.count() >= 6:
                messages.error(request, 'You cannot add more than 6 files')
                return HttpResponseRedirect(reverse('classes:assignment_detail', kwargs={'pk':assignment.pk}))
            if assignment_file.count() + len(files) > 6:
                messages.error(request, 'You cannot add more than 6 files')
                return HttpResponseRedirect(reverse('classes:assignment_detail', kwargs={'pk':assignment.pk}))
            for file in files:
                print('kna aayena ta??')
                AssignmentFile.objects.create(assignment_submission=assignment_submission, a_file=file)
            messages.success(request, 'Assignment submitted successfully')
            return HttpResponseRedirect(reverse('classes:assignment_detail', kwargs={'pk':assignment.pk}))
        except Exception as e:
            print(e,'errorrrrrrrr')
            messages.error(request, 'Assignment not submitted')
            return HttpResponseRedirect(reverse('classes:assignment_detail', kwargs={'pk':assignment_id}))
        


def student_class_change(request):
    student_id = request.GET.get('student_id')
    status  = request.GET.get('status')
    np_class_id = int(request.GET.get('class_id'))
    nepali_class = NepaliClass.objects.get(pk=np_class_id)
    student = NepaliStudent.objects.get(pk=student_id)
    nepali_class.students.remove(student)
    nepali_class.save()
    student.current_status = status
    student.save()
    return HttpResponse('success')


def student_email_send(request):
    student_id = request.GET.get('student_id')
    student = NepaliStudent.objects.get(pk=student_id)
    class_id = request.GET.get('class_id')
    np_class = NepaliClass.objects.get(pk=class_id)
    student_email = student.user.email
    class_week = np_class.day
    class_time = np_class.time
    teacher_name = np_class.teacher.user.full_name
    zoom_link = np_class.teacher.zoom_link
    start_date = find_next_weekday_date(class_week)
    payment_portal_group = "https://kakaaki.com/payment"
    payment_portal_one2one = "https://kakaaki.com/payment-one-to-one"
    class_type = np_class.class_type
    context = {
        'class_day':class_week,
        'class_time':class_time,
        'teacher_name':teacher_name,
        'zoom_link':zoom_link,
        'start_date':start_date,
        'payment_portal':payment_portal_group if class_type == 'Group Class' else payment_portal_one2one,
        'book_link': 'https://kakaaki.com/buy-book',
    }
    # message = render_to_string(message_template, context)
    send_email_task.delay(student_email,context)
    return HttpResponse('success')
    


def student_add(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        np_class = NepaliClass.objects.get(pk=class_id)
        student_id = request.POST.get('student')
        student = NepaliStudent.objects.get(pk=student_id)
        np_class.students.add(student)
        np_class.save()
        student.current_status = 'Enrolled'
        student.save()
        return HttpResponse('success')