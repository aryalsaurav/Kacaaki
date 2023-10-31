from django.urls import path
from . import views


app_name = 'classes'
urlpatterns = [
    path('nepali/add/', views.NepaliClassAddView.as_view(), name='nepaliclass_add'),
    path('nepalistudent/autocomplete/',views.StudentsAutocomplete.as_view(), name='nepali-student-autocomplete'),
]