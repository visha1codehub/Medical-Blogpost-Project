from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signupPage, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user-profile/<int:pk>/', views.user_profile, name="user-profile"),
    path('doctors-list/', views.doctors_list, name="doctors-list"),
]

