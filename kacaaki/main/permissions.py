from django.contrib.auth.mixins import UserPassesTestMixin

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



class TeacherInNepaliClass(UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.teacher.nepaliclass_set.filter(id=self.kwargs['pk']).exists() or self.request.user.is_superuser or self.request.user.is_staff
        except:
            return False


class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    


class NepaliTeacherMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.teacher.teacher_type == 'Nepali Teacher' or self.request.user.is_superuser or self.request.user.is_staff
        except:
            return False
        

class DanceTeacherMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.teacher.teacher_type == 'Dance Teacher' or self.request.user.is_superuser or self.request.user.is_staff
        except:
            return False