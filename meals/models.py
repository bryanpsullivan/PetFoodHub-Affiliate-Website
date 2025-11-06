from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """Individual products (dry food, wet food, treats)"""
    
    PRODUCT_TYPES = [
        ('dry', 'Dry Food'),
        ('wet', 'Wet Food'),
        ('treat', 'Treats'),
    ]
    
    PREFERENCE_TAGS = [
        ('budget', 'Budget-Friendly'),
        ('premium', 'Premium'),
        ('grain_free', 'Grain-Free'),
        ('organic', 'Organic'),
        ('natural', 'Natural'),
        ('limited_ingredient', 'Limited Ingredient'),
    ]
    
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES)
    
    # Nutritional info
    calories_per_oz = models.DecimalField(max_digits=5, decimal_places=2)
    package_size = models.DecimalField(max_digits=6, decimal_places=2)  # in oz or lbs
    package_unit = models.CharField(max_length=10, default='oz')  # 'oz' or 'lbs'
    
    # Pricing
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Affiliate
    affiliate_link = models.URLField(max_length=500)
    
    # Preferences
    preferences = models.CharField(max_length=50, choices=PREFERENCE_TAGS, blank=True)
    
    # Metadata
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['brand', 'name']
    
    def __str__(self):
        return f"{self.brand} - {self.name} ({self.product_type})"


class Meal(models.Model):
    """Pre-curated meal combinations with reference portions"""
    
    SIZE_CATEGORIES = [
        ('small', 'Small (5-25 lbs)'),
        ('medium', 'Medium (30-60 lbs)'),
        ('large', 'Large (70-100+ lbs)'),
    ]
    
    LIFE_STAGES = [
        ('puppy', 'Puppy (4-12 months)'),
        ('adult', 'Adult (1-8 years)'),
        ('senior', 'Senior (8+ years)'),
    ]
    
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    
    # Products in this meal
    dry_food = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='meals_as_dry')
    wet_food = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='meals_as_wet')
    treats = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='meals_as_treat')
    
    # Target specifications (ONLY DEFINED ONCE)
    size_category = models.CharField(max_length=10, choices=SIZE_CATEGORIES)
    life_stage = models.CharField(max_length=10, choices=LIFE_STAGES)
    
    # Reference portions (calculated manually based on package sizes)
    reference_weight = models.IntegerField(
        default=30,
        help_text="Reference dog weight this meal was calculated for (e.g., 30 lbs)"
    )
    reference_daily_calories = models.IntegerField(
        help_text="Daily calorie needs for reference dog"
    )
    reference_dry_oz = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Daily dry food in ounces for reference dog"
    )
    reference_wet_oz = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Daily wet food in ounces for reference dog"
    )
    reference_treat_oz = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Daily treats in ounces for reference dog"
    )
    
    # Preferences
    preference_tags = models.CharField(max_length=100, blank=True)
    
    # Metadata
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', 'brand']
    
    def __str__(self):
        return f"{self.brand} - {self.name}"


class PetProfile(models.Model):
    """User's pet information"""
    
    ACTIVITY_LEVELS = [
        ('low', 'Low (Senior/Inactive)'),
        ('moderate', 'Moderate (Average)'),
        ('high', 'High (Very Active)'),
    ]
    
    LIFE_STAGES = [
        ('puppy', 'Puppy (4-12 months)'),
        ('adult', 'Adult (1-8 years)'),
        ('senior', 'Senior (8+ years)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    weight = models.IntegerField()  # in pounds
    age_months = models.IntegerField()  # Age in months
    life_stage = models.CharField(max_length=10, choices=LIFE_STAGES)
    activity_level = models.CharField(max_length=10, choices=ACTIVITY_LEVELS, default='moderate')
    
    # Optional details
    breed = models.CharField(max_length=100, blank=True)
    special_needs = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.weight} lbs)"


class SavedMeal(models.Model):
    """User's saved meal plans"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_meals')
    pet = models.ForeignKey(PetProfile, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    
    # Calculated portions (stored for reference)
    daily_calories = models.IntegerField()
    dry_food_oz = models.DecimalField(max_digits=5, decimal_places=2)
    wet_food_oz = models.DecimalField(max_digits=5, decimal_places=2)
    treat_oz = models.DecimalField(max_digits=5, decimal_places=2)  # CHANGED from treat_calories
    
    notes = models.TextField(blank=True)
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.meal.brand} for {self.pet.name}"