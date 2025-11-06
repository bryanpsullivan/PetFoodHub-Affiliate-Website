from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from meals.models import PetProfile, SavedMeal


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('user_dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """User login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


@login_required
def user_dashboard(request):
    """User dashboard showing pets and saved meals"""
    pets = PetProfile.objects.filter(user=request.user)
    saved_meals = SavedMeal.objects.filter(user=request.user, is_current=True)
    
    context = {
        'pets': pets,
        'saved_meals': saved_meals,
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def add_pet(request):
    """Add a new pet profile"""
    if request.method == 'POST':
        name = request.POST.get('name')
        weight = int(request.POST.get('weight'))
        age_months = int(request.POST.get('age_months'))
        activity_level = request.POST.get('activity_level')
        
        # Determine life stage from age
        if age_months < 12:
            life_stage = 'puppy'
        elif age_months < 96:  # 8 years
            life_stage = 'adult'
        else:
            life_stage = 'senior'
        
        PetProfile.objects.create(
            user=request.user,
            name=name,
            weight=weight,
            age_months=age_months,
            life_stage=life_stage,
            activity_level=activity_level,
        )
        
        messages.success(request, f'{name} added successfully!')
        return redirect('user_dashboard')
    
    return render(request, 'accounts/add_pet.html')


@login_required
def edit_pet(request, pet_id):
    """Edit pet profile"""
    pet = get_object_or_404(PetProfile, id=pet_id, user=request.user)
    
    if request.method == 'POST':
        pet.name = request.POST.get('name')
        pet.weight = int(request.POST.get('weight'))
        pet.age_months = int(request.POST.get('age_months'))
        pet.activity_level = request.POST.get('activity_level')
        
        # Update life stage
        if pet.age_months < 12:
            pet.life_stage = 'puppy'
        elif pet.age_months < 96:
            pet.life_stage = 'adult'
        else:
            pet.life_stage = 'senior'
        
        pet.save()
        messages.success(request, f'{pet.name} updated successfully!')
        return redirect('user_dashboard')
    
    return render(request, 'accounts/edit_pet.html', {'pet': pet})