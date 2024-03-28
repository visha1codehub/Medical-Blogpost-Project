from django.urls import path
from . import views


urlpatterns = [
    path('appointment-form/<int:doc_id>/', views.appointment_form, name='appointment-form'),
    path('appointment-detail/<int:pk>/', views.appointment_detail, name='appointment-detail'),
    path('appointment-list/', views.appointment_list, name='appointment-list'),
    path('google_oauth/redirect/', views.RedirectOauthView, name="redir"),
    path('google_oauth/callback/', views.CallbackView, name="callb"),
]

