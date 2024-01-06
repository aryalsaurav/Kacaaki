from django import template

register = template.Library()

@register.filter(name='is_staff_or_teacher')
def is_staff_or_teacher(user):
    try:
        if user.is_superuser or user.is_staff or  user.teacher.is_teacher:
            return True
        return False
    except:
        return False


@register.filter(name='nepali_student')
def student_name(user):
    try:
        if 'Nepali Student' in user.user_type  :
            return True
        return False
    except:
        return False
    
    
@register.filter(name='dance_student')
def dance_student(user):
    try:
        if 'Dance Student' in user.user_type  :
            return True
        return False
    except:
        return False
    


@register.filter(name='nepali_teacher')
def teacher_name(user):
    try:
        if 'Nepali Teacher' in user.user_type  :
            return True
        return False
    except:
        return False


@register.filter(name='dance_teacher')
def dance_teacher(user):
    try:
        if 'Dance Teacher' in user.user_type  :
            return True
        return False
    except:
        return False
    