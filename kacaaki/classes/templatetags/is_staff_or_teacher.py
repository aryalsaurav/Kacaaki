from django import template

register = template.Library()

@register.filter(name='is_staff_or_teacher')
def is_staff_or_teacher(user):
    if user.is_superuser or user.is_staff or  user.teacher.is_teacher:
        return True
    return False
