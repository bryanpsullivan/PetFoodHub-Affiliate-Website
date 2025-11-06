from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Meal, Product, SavedMeal, PetProfile
from .meal_calculator import calculate_portions, calculate_45_day_supply, recommend_package_sizes


def home(request):
    """Landing page"""
    featured_meals = Meal.objects.filter(is_featured=True, is_active=True)[:6]
    context = {
        'featured_meals': featured_meals,
    }
    return render(request, 'meals/home.html', context)


def meal_finder(request):
    """Interactive meal finder - step-by-step form"""
    context = {}
    return render(request, 'meals/meal_finder.html', context)


def meal_results(request):
    """Show recommended meals based on user selections"""
    
    # Get user inputs
    weight = int(request.GET.get('weight', 0))
    life_stage = request.GET.get('life_stage', 'adult')
    activity_level = request.GET.get('activity_level', 'moderate')
    preference = request.GET.get('preference', '')
    
    # Validate inputs
    if not weight or weight < 5:
        messages.error(request, 'Please enter a valid weight.')
        return redirect('meal_finder')
    
    # Determine size category
    if weight <= 25:
        size_category = 'small'
    elif weight <= 60:
        size_category = 'medium'
    else:
        size_category = 'large'
    
    # Calculate nutritional needs
    portions = calculate_portions(weight, activity_level, life_stage)
    supply_45_day = calculate_45_day_supply(weight, activity_level, life_stage)
    
    # Filter meals
    meals = Meal.objects.filter(
        size_category=size_category,
        life_stage=life_stage,
        is_active=True
    )
    
    # Apply preference filter if specified
    if preference:
        meals = meals.filter(preference_tags__icontains=preference)
    
    # Prepare meal recommendations with calculated portions
    recommendations = []
    for meal in meals[:10]:  # Limit to top 10 options
        shopping_list = recommend_package_sizes(supply_45_day, meal)
        
        # Calculate total cost
        total_cost = (
            shopping_list['dry_food']['quantity'] * float(meal.dry_food.price) +
            shopping_list['wet_food']['quantity'] * float(meal.wet_food.price) +
            shopping_list['treats']['quantity'] * float(meal.treats.price)
        )
        
        recommendations.append({
            'meal': meal,
            'shopping_list': shopping_list,
            'total_cost': round(total_cost, 2),
            'cost_per_day': round(total_cost / 45, 2),
        })
    
    # Sort by cost (budget-friendly first)
    recommendations.sort(key=lambda x: x['total_cost'])
    
    context = {
        'weight': weight,
        'life_stage': life_stage,
        'activity_level': activity_level,
        'portions': portions,
        'recommendations': recommendations,
    }
    
    return render(request, 'meals/meal_results.html', context)


def meal_detail(request, meal_id):
    """Detailed view of a specific meal"""
    meal = get_object_or_404(Meal, id=meal_id, is_active=True)
    
    # Get weight from query params or use default
    weight = int(request.GET.get('weight', 30))
    activity_level = request.GET.get('activity_level', 'moderate')
    life_stage = meal.life_stage
    
    # Calculate portions
    portions = calculate_portions(weight, activity_level, life_stage)
    supply_45_day = calculate_45_day_supply(weight, activity_level, life_stage)
    shopping_list = recommend_package_sizes(supply_45_day, meal)
    
    context = {
        'meal': meal,
        'portions': portions,
        'shopping_list': shopping_list,
        'weight': weight,
        'activity_level': activity_level,
    }
    
    return render(request, 'meals/meal_detail.html', context)


@login_required
def save_meal(request, meal_id):
    """Save a meal to user's profile"""
    if request.method == 'POST':
        meal = get_object_or_404(Meal, id=meal_id)
        pet_id = request.POST.get('pet_id')
        
        if pet_id:
            pet = get_object_or_404(PetProfile, id=pet_id, user=request.user)
            
            # Calculate portions for this pet
            portions = calculate_portions(pet.weight, pet.activity_level, pet.life_stage)
            
            # Create saved meal
            SavedMeal.objects.create(
                user=request.user,
                pet=pet,
                meal=meal,
                daily_calories=portions['daily_calories'],
                dry_food_oz=portions['dry_food_oz'],
                wet_food_oz=portions['wet_food_oz'],
                treat_calories=portions['treat_calories'],
            )
            
            messages.success(request, f'Meal saved for {pet.name}!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Please select a pet.')
            return redirect('meal_detail', meal_id=meal_id)
    
    return redirect('meal_finder')