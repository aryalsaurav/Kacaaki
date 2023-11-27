from .models import *
from users.models import *
from django.shortcuts import redirect,HttpResponseRedirect
from django.core.exceptions import PermissionDenied


class SuperUserRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/')
        return super(SuperUserRequiredMixin, self).dispatch(request, *args, **kwargs)
    


class StaffRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('/')
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


class TeacherRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            if not request.user.teacher.is_teacher:
                return redirect('/')
            return super(TeacherRequiredMixin, self).dispatch(request, *args, **kwargs)
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class StaffOrNepaliTeacherRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:

            if request.user.is_staff or request.user.user_type == "Nepali Teacher":
                return super().dispatch(request, *args, **kwargs)
            return redirect('/')
        except Exception as e:
            print(e, "error")
            return redirect('/')
        
        

class NepaliTeacherOrStudentRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.is_staff or request.user.user_type == "Nepali Teacher" or request.user.user_type == "Nepali Student":
                return super().dispatch(request, *args, **kwargs)
            return redirect('/')
        except Exception as e:
            print(e, "error")
            return redirect('/')
        
        

class NeapliTeacherOrStudentInClassRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('uid'):
            pk = request.GET.get('uid')
        else:
            pk = kwargs['pk']
        try:
            if request.user.is_staff or request.user.user_type == "Nepali Teacher" or request.user.user_type == "Nepali Student":
                if request.user.user_type == "Nepali Student":
                    if request.user.nepali_student.nepaliclass_set.filter(pk=pk).exists():
                        return super().dispatch(request, *args, **kwargs)
                    else:
                        return redirect('/')
                elif request.user.user_type == "Nepali Teacher":
                    if request.user.teacher.nepaliclass_set.filter(pk=pk).exists():
                        return super().dispatch(request, *args, **kwargs)
                    else:
                        raise PermissionDenied
                elif request.user.is_staff:
                    return super().dispatch(request, *args, **kwargs)
                else:
                    raise PermissionDenied
                    
                return super().dispatch(request, *args, **kwargs)
            return redirect('/')
        except Exception as e:
            print(e, "error")
            return redirect('/')