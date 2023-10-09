from django.urls import path
from django.http import HttpResponse
from .views import (
    NepaliClassView,
    DanceClassView,
    NepaliClassDetailView,
    DanceClassDetailView,
    AssignmentView,
    AssignmentDetailView,
    AssignmentSubmissionView,
    AssignmentSubmissionDetailView,


)

app_name = 'classes_api'
urlpatterns = [
    path('nepali-class/', NepaliClassView.as_view(), name='nepali-class'),
    path('nepali-class/<int:pk>/', NepaliClassDetailView.as_view(), name='nepali-class-detail'),
    path('dance-class/', DanceClassView.as_view(), name='dance-class'),
    path('dance-class/<int:pk>/', DanceClassDetailView.as_view(), name='dance-class-detail'),
    path('assignment/', AssignmentView.as_view(), name='assignment'),
    path('assignment/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('assignment-submission/', AssignmentSubmissionView.as_view(), name='assignment-submission'),
    path('assignment-submission/<int:pk>/', AssignmentSubmissionDetailView.as_view(), name='assignment-submission-detail'),


]