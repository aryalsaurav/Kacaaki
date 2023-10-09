from django.urls import path,re_path
from . import views

app_name = 'main'
urlpatterns = [
    path('',views.home,name='home'),
    path('about-us/',views.about_us,name='about_us'),
    path('contact-us/',views.ContactUsView.as_view(),name='contact_us'),
    path('testomonials/',views.TestomonialListView.as_view(),name='testomonials'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.logout_view,name='logout'),
]
