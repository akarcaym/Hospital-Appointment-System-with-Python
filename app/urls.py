
from django.urls import path
from django.conf.urls import url
from app import views



urlpatterns = [
    path('', views.homepage, name='home'),
    path('contact/', views.contactpage, name='contact'),
    path('whoarewe/', views.whoarewe, name='whoarewe'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('getappointment/', views.dept_select, name='getappointment'),
    path('doctorlist/<int:pk>/', views.doctor_select),
    path('schedule/<int:pk>/', views.schedule_view),
    path('appointment/<int:pk>/', views.appointment),
    path('delete/<int:pk>/', views.delete_appointment),
    path('appointment/', views.appointmentdata),
    path('blog/', views.blog, name="blog"),
    path('doctorappointment/', views.appointmentdoc, name="doctor"),
    path('rate/<int:pk>/', views.rate_app, name="rate")
    ]