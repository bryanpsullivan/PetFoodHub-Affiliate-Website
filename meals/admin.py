from django.contrib import admin
from .models import Product, Meal, PetProfile, SavedMeal
from django.utils.html import format_html


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name', 'product_type', 'package_size', 'package_unit', 'price', 'image_preview', 'is_active']  # Added image_preview
    list_filter = ['product_type', 'brand', 'is_active', 'preferences']
    search_fields = ['brand', 'name']
    list_editable = ['price', 'is_active']

    # Add image preview in the list
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Image'
    
    readonly_fields = ['image_preview']
    
    # Organize fields to match your Chewy workflow
    fieldsets = (
        ('Product Info (from Chewy)', {
            'fields': ('brand', 'name', 'product_type'),
            'description': 'Copy brand and product name from Chewy'
        }),
        ('Product Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload product image or drag & drop'
        }),
        ('Package Details (from Chewy listing)', {
            'fields': ('package_size', 'package_unit', 'price'),
            'description': 'Example: 5 lbs, or 12 oz, etc.'
        }),
        ('Chewy Link', {
            'fields': ('affiliate_link',),
            'description': 'Paste the full Chewy URL here'
        }),
        ('Nutritional Info (Standard Values)', {
            'fields': ('calories_per_oz',),
            'description': 'Dry: 95 cal/oz | Wet: 25 cal/oz | Treats: 87.5 cal/oz'
        }),
        ('Optional', {
            'fields': ('preferences', 'description'),  # REMOVED image_url
            'classes': ('collapse',),
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        return initial


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = [
        'brand', 'name', 'size_category', 'life_stage', 
        'reference_weight', 'is_featured', 'is_active'
    ]
    list_filter = ['size_category', 'life_stage', 'is_featured', 'is_active', 'brand']
    search_fields = ['brand', 'name']
    list_editable = ['is_featured', 'is_active']
    
    fieldsets = (
        ('Meal Name', {
            'fields': ('name', 'brand'),
            'description': 'Example: "Blue Buffalo Senior Small Breed Complete Meal"'
        }),
        ('Select Products (must create products first!)', {
            'fields': ('dry_food', 'wet_food', 'treats'),
        }),
        ('Target Dog', {
            'fields': ('size_category', 'life_stage', 'preference_tags'),
        }),
        ('📊 Reference Portions (Your Manual Calculations)', {
            'fields': (
                'reference_weight',
                'reference_daily_calories',
                'reference_dry_oz',
                'reference_wet_oz',
                'reference_treat_oz',
            ),
            'description': '''
            Calculate these so all 3 products finish in ~45 days.
            Example for 10lb senior:
            - Reference weight: 10
            - Daily calories: ~250
            - Dry food: 1.3 oz/day (⅓ cup)
            - Wet food: 1.0 oz/day
            - Treats: 0.3 oz/day (~10 calories)
            '''
        }),
        ('Optional', {
            'fields': ('description', 'is_featured'),
            'classes': ('collapse',),
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(PetProfile)
class PetProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'weight', 'life_stage', 'activity_level']
    list_filter = ['life_stage', 'activity_level']
    search_fields = ['name', 'user__username']


@admin.register(SavedMeal)
class SavedMealAdmin(admin.ModelAdmin):
    list_display = ['user', 'pet', 'meal', 'daily_calories', 'is_current', 'created_at']
    list_filter = ['is_current', 'created_at']
    search_fields = ['user__username', 'pet__name', 'meal__brand']
    readonly_fields = ['daily_calories', 'dry_food_oz', 'wet_food_oz', 'treat_oz', 'created_at']