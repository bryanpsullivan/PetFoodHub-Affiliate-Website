from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('pet/add/', views.add_pet, name='add_pet'),
    path('pet/<int:pet_id>/edit/', views.edit_pet, name='edit_pet'),
]