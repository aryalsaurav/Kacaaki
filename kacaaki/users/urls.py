from django.urls import path,re_path
from . import views

app_name = 'users'
urlpatterns = [
    path('teachers/list/',views.teachers_list,name='teachers_list'),
    path("register/",views.UserRegistrationView.as_view(),name="user-register"),
    
]
