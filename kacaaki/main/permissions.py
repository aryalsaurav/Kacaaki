from django.contrib.auth.mixins import UserPassesTestMixin
from classes.models import NepaliClass


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
    
class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        try: 
            return self.request.user.teacher.is_teacher   
        except:
            return False
    
    
class NepaliStudentRequired(UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.student.is_neplai_student
        except:
            return False
        

class DanceStudentRequired(UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.student.is_dance_student
        except:
            return False



class TeacherOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            return (self.request.user.teacher.is_teacher or
                    self.request.user.is_superuser or
                    self.request.user.is_staff
                    )
        except:
            return False


class InClassTeacherOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            return (self.request.user.teacher.nepaliclass_set.filter(id=self.kwargs['pk']).exists() or 
                self.request.user.is_superuser or 
                self.request.user.is_staff
                )
        except:
            return False
        
        

class InClassOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            user = self.request.user
            nepali_class = NepaliClass.objects.get(id=self.kwargs['pk'])
        except:
            return False

        is_teacher = user.teacher.is_teacher if hasattr(user, 'teacher') else False
        is_superuser = user.is_superuser
        is_staff = user.is_staff
        is_student_in_class = user.nepali_student in nepali_class.students.all() if hasattr(user, 'nepali_student') else False

        result = (is_teacher or is_superuser or is_staff or is_student_in_class)
        print("is_teacher:", is_teacher)
        print("is_superuser:", is_superuser)
        print("is_staff:", is_staff)
        print("is_student_in_class:", is_student_in_class)
        print("Result:", result)
        
        return result
        



class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    


        

class DanceTeacherMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.teacher.teacher_type == 'Dance Teacher' or self.request.user.is_superuser or self.request.user.is_staff
        except:
            return False