from django.urls import path
from django.http import HttpResponse
from .views import (
    NepaliClassView,
    DanceClassView,
    NepaliClassDetailView,
    DanceClassDetailView,
)

urlpatterns = [
    path('nepali-class/', NepaliClassView.as_view(), name='nepali-class'),
    path('nepali-class/<int:pk>/', NepaliClassDetailView.as_view(), name='nepali-class-detail'),
    path('dance-class/', DanceClassView.as_view(), name='dance-class'),
    path('dance-class/<int:pk>/', DanceClassDetailView.as_view(), name='dance-class-detail'),


]