from django.urls import path
from . import views

urlpatterns = [
    path('transition/', views.transition_guide, name='transition_guide'),
    path('portions/', views.portion_guide, name='portion_guide'),
    path('nutrition/', views.nutrition_basics, name='nutrition_basics'),
]