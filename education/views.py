from django.shortcuts import render
from .models import Article


def transition_guide(request):
    """Guide on transitioning dogs to new food"""
    context = {
        'title': 'How to Transition Your Dog to New Food',
    }
    return render(request, 'education/transition_guide.html', context)


def portion_guide(request):
    """Guide on portion sizes based on activity level"""
    context = {
        'title': 'Feeding Guide: Portions by Size & Activity',
    }
    return render(request, 'education/portion_guide.html', context)


def nutrition_basics(request):
    """Basic nutrition information"""
    context = {
        'title': 'Dog Nutrition Basics',
    }
    return render(request, 'education/nutrition_basics.html', context)