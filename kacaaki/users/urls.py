from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import include
from rest_framework import  routers

from .views import (
    PasswordChangeView,
    UserLoginView,
    LogoutView,
    NepaliStudentView,
    NepaliStudentDPDView,
    
)

router = routers.DefaultRouter()

urlpatterns = [
    path('',include(router.urls)),
    path('nepali-student/',NepaliStudentView.as_view(),name='nepali_student'),
    path('nepali-student/<int:pk>/',NepaliStudentDPDView.as_view(),name='nepali_student'),
    path('user/login/',UserLoginView.as_view(),name='login'),
    path('user/change-password/',PasswordChangeView.as_view(),name="password"),
    path('user/logout/',LogoutView.as_view(),name='logout'),
    
    
   
]