"""
Meal calculation engine based on your formulas
"""

# Activity level multipliers
ACTIVITY_MULTIPLIERS = {
    'low': 0.85,
    'moderate': 1.0,
    'high': 1.15,
}

# Base calorie requirements by weight (from your data)
CALORIE_CHART = {
    5: (185, 200),
    10: (300, 350),
    15: (415, 475),
    20: (515, 585),
    25: (625, 695),  # Estimated
    30: (700, 800),
    40: (875, 1000),
    50: (1050, 1200),
    60: (1200, 1350),
    70: (1350, 1500),
    80: (1500, 1650),
    90: (1600, 1800),
    100: (1750, 2000),
}

# Ratio constants (from your formulas)
WET_FOOD_RATIO = 0.25  # 25% of calories from wet food
DRY_FOOD_RATIO = 0.75  # 75% of calories from dry food
TREAT_RATIO = 0.10      # ~10% for treats

# Calorie densities
WET_FOOD_CAL_PER_OZ = 25
DRY_FOOD_CAL_PER_OZ = 95
TREAT_CAL_PER_OZ = 87.5  # ~1400 cal per 16oz


def get_daily_calories(weight, activity_level='moderate'):
    """
    Calculate daily calorie needs based on weight and activity level
    """
    # Find closest weight in chart
    if weight <= 5:
        base_calories = CALORIE_CHART[5]
    elif weight >= 100:
        # For dogs over 100 lbs, add 40-50 calories per 10 lbs
        extra_weight = weight - 100
        extra_tens = extra_weight // 10
        base_min, base_max = CALORIE_CHART[100]
        base_calories = (base_min + (extra_tens * 40), base_max + (extra_tens * 50))
    else:
        # Find nearest weight bracket
        weights = sorted(CALORIE_CHART.keys())
        for i, w in enumerate(weights):
            if weight <= w:
                base_calories = CALORIE_CHART[w]
                break
    
    # Calculate average and apply activity multiplier
    avg_calories = (base_calories[0] + base_calories[1]) / 2
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.0)
    
    return int(avg_calories * multiplier)


def calculate_portions(weight, activity_level='moderate', life_stage='adult'):
    """
    Calculate daily portions of wet food, dry food, and treats
    Returns dict with portions in ounces
    """
    daily_calories = get_daily_calories(weight, activity_level)
    
    # Adjust for life stage (seniors typically need slightly less)
    if life_stage == 'senior':
        daily_calories = int(daily_calories * 0.90)
    elif life_stage == 'puppy':
        daily_calories = int(daily_calories * 1.10)
    
    # Calculate calories from each component
    wet_calories = daily_calories * WET_FOOD_RATIO
    dry_calories = daily_calories * DRY_FOOD_RATIO
    treat_calories = daily_calories * TREAT_RATIO
    
    # Convert to ounces
    wet_oz = wet_calories / WET_FOOD_CAL_PER_OZ
    dry_oz = dry_calories / DRY_FOOD_CAL_PER_OZ
    treat_oz = treat_calories / TREAT_CAL_PER_OZ
    
    # Also convert dry food to cups (4 oz = 1 cup)
    dry_cups = dry_oz / 4
    
    return {
        'daily_calories': daily_calories,
        'wet_food_oz': round(wet_oz, 1),
        'dry_food_oz': round(dry_oz, 1),
        'dry_food_cups': round(dry_cups, 2),
        'treat_oz': round(treat_oz, 1),
        'treat_calories': int(treat_calories),
    }


def calculate_45_day_supply(weight, activity_level='moderate', life_stage='adult'):
    """
    Calculate product quantities needed for a 45-day supply
    """
    daily = calculate_portions(weight, activity_level, life_stage)
    
    # 45-day totals
    wet_total_oz = daily['wet_food_oz'] * 45
    dry_total_oz = daily['dry_food_oz'] * 45
    treat_total_oz = daily['treat_oz'] * 45
    
    # Convert to pounds
    wet_lbs = wet_total_oz / 16
    dry_lbs = dry_total_oz / 16
    treat_lbs = treat_total_oz / 16
    
    return {
        'daily_portions': daily,
        'wet_food_lbs': round(wet_lbs, 1),
        'wet_food_oz': round(wet_total_oz, 1),
        'dry_food_lbs': round(dry_lbs, 1),
        'treat_lbs': round(treat_lbs, 1),
    }


def recommend_package_sizes(portions_45_day, meal):
    """
    Recommend specific package quantities based on meal products
    Returns shopping list
    """
    # Get product package sizes
    dry_pkg_size = float(meal.dry_food.package_size)
    wet_pkg_size = float(meal.wet_food.package_size)
    treat_pkg_size = float(meal.treats.package_size)
    
    # Calculate packages needed
    dry_bags = int(portions_45_day['dry_food_lbs'] / dry_pkg_size) + 1
    wet_packages = int(portions_45_day['wet_food_lbs'] / wet_pkg_size) + 1
    treat_bags = int(portions_45_day['treat_lbs'] / treat_pkg_size) + 1
    
    return {
        'dry_food': {
            'product': meal.dry_food,
            'quantity': dry_bags,
            'total_lbs': dry_bags * dry_pkg_size,
        },
        'wet_food': {
            'product': meal.wet_food,
            'quantity': wet_packages,
            'total_lbs': wet_packages * wet_pkg_size,
        },
        'treats': {
            'product': meal.treats,
            'quantity': treat_bags,
            'total_lbs': treat_bags * treat_pkg_size,
        },
    }