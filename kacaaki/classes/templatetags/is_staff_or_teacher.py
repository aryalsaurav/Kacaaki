from django import template
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from urllib.parse import urlparse, parse_qs
import re
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


@register.filter(name='remove_page_param')
def remove_query_param(url, param_name):

    parsed_url = urlparse(url)
    query_dict = parse_qs(parsed_url.query)
    
    # Remove the specified parameter
    query_dict.pop(param_name, None)
    
    # Reconstruct the query string without the removed parameter
    new_query = urlencode(query_dict, doseq=True)
    
    # Reconstruct the URL with the new query string
    new_url = parsed_url._replace(query=new_query).geturl()
    
    return new_url



@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url