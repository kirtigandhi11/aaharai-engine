from models import DailyMealPlan, GroceryList

class GroceryGenerator:
    """Step 8: Generate grocery list from meal plan"""
    
    INGREDIENT_MAPPING = {
        # Grains
        'rice': {'category': 'grains', 'unit': 'kg', 'per_serving': 0.08},
        'roti': {'category': 'grains', 'unit': 'kg', 'per_serving': 0.06},  # wheat flour
        'oats': {'category': 'grains', 'unit': 'kg', 'per_serving': 0.05},
        'poha': {'category': 'grains', 'unit': 'kg', 'per_serving': 0.07},
        'dosa': {'category': 'grains', 'unit': 'kg', 'per_serving': 0.06},  # rice+dal
        'idli': {'category': 'grains', 'unit': 'kg', 'per_serving': 0.06},
        'khichdi': {'category': 'grains', 'unit': 'kg', 'per_serving': 0.08},
        'quinoa': {'category': 'grains', 'unit': 'kg', 'per_serving': 0.06},
        
        # Proteins
        'dal': {'category': 'proteins', 'unit': 'kg', 'per_serving': 0.06},
        'paneer': {'category': 'proteins', 'unit': 'kg', 'per_serving': 0.10},
        'chicken': {'category': 'proteins', 'unit': 'kg', 'per_serving': 0.12},
        'fish': {'category': 'proteins', 'unit': 'kg', 'per_serving': 0.12},
        'eggs': {'category': 'proteins', 'unit': 'pieces', 'per_serving': 2},
        'tofu': {'category': 'proteins', 'unit': 'kg', 'per_serving': 0.10},
        'sprouts': {'category': 'proteins', 'unit': 'kg', 'per_serving': 0.08},
        'rajma': {'category': 'proteins', 'unit': 'kg', 'per_serving': 0.06},
        'chole': {'category': 'proteins', 'unit': 'kg', 'per_serving': 0.06},
        
        # Vegetables
        'mixed_veg': {'category': 'vegetables', 'unit': 'kg', 'per_serving': 0.15},
        'palak': {'category': 'vegetables', 'unit': 'kg', 'per_serving': 0.10},
        'bhindi': {'category': 'vegetables', 'unit': 'kg', 'per_serving': 0.12},
        'baingan': {'category': 'vegetables', 'unit': 'kg', 'per_serving': 0.12},
        'lauki': {'category': 'vegetables', 'unit': 'kg', 'per_serving': 0.15},
        'tomatoes': {'category': 'vegetables', 'unit': 'kg', 'per_serving': 0.08},
        'onions': {'category': 'vegetables', 'unit': 'kg', 'per_serving': 0.06},
        
        # Dairy/Alternatives
        'curd': {'category': 'dairy_alternatives', 'unit': 'liters', 'per_serving': 0.2},
        'milk': {'category': 'dairy_alternatives', 'unit': 'liters', 'per_serving': 0.2},
        'buttermilk': {'category': 'dairy_alternatives', 'unit': 'liters', 'per_serving': 0.25},
        'coconut_curd': {'category': 'dairy_alternatives', 'unit': 'kg', 'per_serving': 0.15},
        'almond_milk': {'category': 'dairy_alternatives', 'unit': 'liters', 'per_serving': 0.25},
        
        # Snacks/Misc
        'nuts': {'category': 'spices_misc', 'unit': 'kg', 'per_serving': 0.03},
        'fruit': {'category': 'vegetables', 'unit': 'kg', 'per_serving': 0.15},
        'spices': {'category': 'spices_misc', 'unit': 'pack', 'per_serving': 0.01},
        'oil': {'category': 'spices_misc', 'unit': 'liters', 'per_serving': 0.015},
        'ghee': {'category': 'spices_misc', 'unit': 'kg', 'per_serving': 0.01}
    }
    
    def generate(self, meal_plan: DailyMealPlan, days: int = 1) -> GroceryList:
        groceries = {
            'vegetables': {},
            'grains': {},
            'proteins': {},
            'dairy_alternatives': {},
            'spices_misc': {}
        }
        
        # Extract ingredients from all meals
        all_meals = [
            meal_plan.breakfast,
            meal_plan.lunch,
            meal_plan.dinner
        ] + meal_plan.snacks
        
        for meal in all_meals:
            ingredients = self._extract_ingredients(meal.name)
            for ingredient in ingredients:
                self._add_to_grocery(groceries, ingredient, days)
        
        # Add staples
        self._add_staples(groceries, days)
        
        return GroceryList(
            vegetables=groceries['vegetables'],
            grains=groceries['grains'],
            proteins=groceries['proteins'],
            dairy_alternatives=groceries['dairy_alternatives'],
            spices_misc=groceries['spices_misc'],
            weekly_scaling_factor=float(days)
        )
    
    def _extract_ingredients(self, meal_name: str) -> list:
        """Extract key ingredients from meal name"""
        meal_lower = meal_name.lower()
        ingredients = []
        
        for key in self.INGREDIENT_MAPPING.keys():
            if key in meal_lower:
                ingredients.append(key)
        
        # Add common base ingredients if not found
        if not ingredients:
            if 'curry' in meal_lower or 'sabzi' in meal_lower:
                ingredients.extend(['mixed_veg', 'onions', 'tomatoes'])
            elif 'rice' in meal_lower:
                ingredients.append('rice')
            elif 'roti' in meal_lower or 'bread' in meal_lower:
                ingredients.append('roti')
        
        return ingredients if ingredients else ['mixed_veg', 'rice']
    
    def _add_to_grocery(self, groceries: dict, ingredient: str, days: int):
        """Add ingredient to appropriate category"""
        mapping = self.INGREDIENT_MAPPING.get(ingredient, {
            'category': 'spices_misc', 'unit': 'kg', 'per_serving': 0.1
        })
        
        category = mapping['category']
        quantity = mapping['per_serving'] * days
        
        if ingredient in groceries[category]:
            groceries[category][ingredient] += quantity
        else:
            groceries[category][ingredient] = quantity
    
    def _add_staples(self, groceries: dict, days: int):
        """Add essential staples"""
        # Spices and cooking essentials
        staples = {
            'salt': 0.01 * days,
            'turmeric': 0.005 * days,
            'cumin': 0.005 * days,
            'coriander': 0.005 * days,
            'ginger_garlic': 0.02 * days,
            'green_chilies': 0.01 * days
        }
        
        for staple, qty in staples.items():
            if staple in groceries['spices_misc']:
                groceries['spices_misc'][staple] += qty
            else:
                groceries['spices_misc'][staple] = qty
