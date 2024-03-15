from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='home'),
    path('signup/', views.signupPage, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('doctor-blogposts', views.doctor_dashboard, name="doctor-dashboard"),
    path('blogpost-list/', views.patient_dashboard, name="patient-dashboard"),
    path('create-blogpost/', views.create_blogpost, name='create-blogpost'),
    path('edit-blogpost/<int:pk>/', views.edit_blogpost, name='edit-blogpost'),
    path('delete-blogpost/<int:pk>/', views.delete_blogpost, name='delete-blogpost'),
    path('blogpost-detail/<int:pk>/', views.blogpost_detail, name="blogpost-detail"),
    path('user-profile/<int:pk>/', views.user_profile, name="user-profile"),
    path('doctors-list/', views.doctors_list, name="doctors-list"),
    path('appointment-form/<int:doc_id>/', views.appointment_form, name='appointment-form'),
    path('appointment-detail/<int:pk>/', views.appointment_detail, name='appointment-detail'),
    path('appointment-list/', views.appointment_list, name='appointment-list'),

    path('google_oauth/redirect/', views.RedirectOauthView, name="redir"),
    path('google_oauth/callback/', views.CallbackView, name="callb"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)