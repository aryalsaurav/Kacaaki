from django.urls import path
from . import views


app_name = 'classes'
urlpatterns = [
    path('nepali/add/', views.NepaliClassAddView.as_view(), name='nepaliclass_add'),
    path('nepali/list/', views.NepaliClassListView.as_view(), name='nepaliclass_list'),
    path('nepali/<int:pk>/update/', views.NepaliClassUpdateView.as_view(), name='nepaliclass_update'),
    path('nepali/<int:pk>/delete/', views.NepaliClassDeleteView.as_view(), name='nepaliclass_delete'),
    path('nepali/<int:pk>/detail/', views.NepaliClassDetailView.as_view(), name='nepaliclass_detail'),
    path('nepali/assignment/add/', views.AssignmentAddView.as_view(), name='assignment_add'),
    path('nepali/assignment/list/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('nepali/assignment/<int:pk>/detail/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('nepali/assignment/<int:pk>/update/', views.AssignmentUpdateView.as_view(), name='assignment_update'),
    path('nepali/assignment/submission/',views.AssignmentSubmissionView.as_view(),name='assignment_submission'),
    path('dashboard/nepali/class/list/',views.DashboardNepaliClassListView.as_view(),name='dashboard-nepali-class-list'),
    path('student/class/change',views.student_class_change,name='student_class_change'),
    path('student/send/class/email/',views.student_email_send,name='send_class_email'),
    path('student/add/class/',views.student_add,name='student_add_class'),
]