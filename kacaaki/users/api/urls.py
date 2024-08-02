from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import include
from rest_framework import  routers

from .views import (
    PasswordChangeView,
    AdminUserView,
    AdminUserDPDView,
    UserLoginView,
    LogoutView,
    NepaliStudentView,
    NepaliStudentDPDView,
    DanceStudentView,
    DanceStudentDPDView,
    TeacherView,
    TeacherDPDView,
    VerifyEmailView,
    PasswordResetEmail,
    PasswordResetView,
    NepaliStudentFilterView,
    DanceStudentFilterView,
    TeacherFilterView,
    UserFilterView,
    UserListView,
    VideoView,
    OtpRequestView


    

    
)

router = routers.DefaultRouter()


app_name = 'users_api'
urlpatterns = [
    path('',include(router.urls)),
    path('admin-user/',AdminUserView.as_view(),name='admin_user'),
    path('admin-user/<int:pk>/',AdminUserDPDView.as_view(),name='admin_user_dpd'),
    path('nepali-student/',NepaliStudentView.as_view(),name='nepali_student'),
    path('nepali-student/<int:pk>/',NepaliStudentDPDView.as_view(),name='nepali_student_dpd'),
    path('dance-student/',DanceStudentView.as_view(),name='dance_student'),
    path('dance-student/<int:pk>/',DanceStudentDPDView.as_view(),name='dance_student_dpd'),
    path('teacher/',TeacherView.as_view(),name='teacher'),
    path('teacher/<int:pk>/',TeacherDPDView.as_view(),name='teacher_dpd'),
    path('user/login/',UserLoginView.as_view(),name='login'),
    path('user/change-password/',PasswordChangeView.as_view(),name="password"),
    path('user/logout/',LogoutView.as_view(),name='logout'),
    path('user/verify-email/<str:token>/',VerifyEmailView.as_view(),name='verify_email'),
    path('user/password-reset-email/',PasswordResetEmail.as_view(),name='password_reset_email'),
    path('user/reset-password/<str:token>/',PasswordResetView.as_view(),name='password_reset'),
    path('nepali-student/filter/',NepaliStudentFilterView.as_view(),name='nepali_student_filter'),
    path('dance-student/filter/',DanceStudentFilterView.as_view(),name='dance_student_filter'),
    path('teacher/filter/',TeacherFilterView.as_view(),name='teacher_filter'),
    path('user/filter/',UserFilterView.as_view(),name='user_filter'),
    path('user/list/view/',UserListView.as_view(),name='user_list_view'),
    path('upload/video/',VideoView.as_view(),name='video_upload'),
    path('otp/request/',OtpRequestView.as_view(),name='otp_request'),


    


    
   
]