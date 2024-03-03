from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('signup/', views.signupPage, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('doctor-dashboard', views.doctor_dashboard, name="doctor-dashboard"),
    path('patient-dashboard', views.patient_dashboard, name="patient-dashboard"),
]
