from django.urls import path
from . import views


app_name = 'classes'
urlpatterns = [
    path('nepali/add/', views.NepaliClassAddView.as_view(), name='nepaliclass_add'),
    path('nepali/list/', views.NepaliClassListView.as_view(), name='nepaliclass_list'),
    path('nepali/<int:pk>/update/', views.NepaliClassUpdateView.as_view(), name='nepaliclass_update'),
    path('nepali/<int:pk>/delete/', views.NepaliClassDeleteView.as_view(), name='nepaliclass_delete'),
    path('nepali/<int:pk>/detail/', views.NepaliClassDetailView.as_view(), name='nepaliclass_detail'),
    path('nepalistudent/autocomplete/',views.StudentsAutocomplete.as_view(), name='nepali-student-autocomplete'),
]