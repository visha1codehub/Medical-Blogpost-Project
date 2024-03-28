from django.urls import path
from . import views


urlpatterns = [
    path('doctor-blogposts', views.doctor_dashboard, name="doctor-dashboard"),
    path('blogpost-list/', views.patient_dashboard, name="patient-dashboard"),
    path('create-blogpost/', views.create_blogpost, name='create-blogpost'),
    path('edit-blogpost/<int:pk>/', views.edit_blogpost, name='edit-blogpost'),
    path('delete-blogpost/<int:pk>/', views.delete_blogpost, name='delete-blogpost'),
    path('blogpost-detail/<int:pk>/', views.blogpost_detail, name="blogpost-detail"),
]
