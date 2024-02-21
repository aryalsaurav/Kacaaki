from django.urls import path,re_path
from . import views

app_name = 'users'
urlpatterns = [
    path('teachers/list/',views.teachers_list,name='teachers_list'),
    path("register/nepali/student/",views.NepaliStudentRegisterView.as_view(),name="nepali-student-register"),
    path("register/dance/student/",views.DanceStudentRegisterView.as_view(),name="dance-student-register"),
    path("user/profile/",views.ProfileView.as_view(),name="user-profile"),
    path("nepali/student/list/",views.NepaliStudentListView.as_view(),name="nepali-student-list"),
    # path('nepalistudent/autocomplete/',views.StudentsAutocomplete.as_view(), name='nepali-student-autocomplete'),

    
]
