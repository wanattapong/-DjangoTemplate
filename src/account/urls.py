from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='singin'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('profile/', views.profile_view, name='profile'),

]