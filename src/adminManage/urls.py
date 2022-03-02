from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home-admin'),
    path('manage-user/', views.manage_user, name='manage_user'),
    path('manage-user/<str:username>/', views.manage_user_detail, name='manage_user_detail'),
    path('manage-user/<str:username>/delete/', views.manage_user_delete, name='manage_user_delete'),
]