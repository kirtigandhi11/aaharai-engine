from models import DailyMealPlan, MealItem, FlexibleOptions

class FlexibilityEngine:
    """Step 7: Provide meal alternatives and substitutions"""
    
    MEAL_ALTERNATIVES = {
        'breakfast': [
            {'name': 'Poha', 'calories': 250, 'protein': 6, 'carbs': 45, 'fat': 5, 'serving': '1.5 cups'},
            {'name': 'Upma', 'calories': 280, 'protein': 7, 'carbs': 42, 'fat': 8, 'serving': '1.5 cups'},
            {'name': 'Besan Chilla', 'calories': 240, 'protein': 12, 'carbs': 28, 'fat': 9, 'serving': '2 pieces'}
        ],
        'lunch': [
            {'name': 'Rajma Rice', 'calories': 420, 'protein': 18, 'carbs': 75, 'fat': 6, 'serving': '1 cup + rice'},
            {'name': 'Chole Roti', 'calories': 400, 'protein': 17, 'carbs': 60, 'fat': 9, 'serving': '1 cup + 2 roti'},
            {'name': 'Kadhi Rice', 'calories': 380, 'protein': 12, 'carbs': 65, 'fat': 8, 'serving': '1 cup + rice'}
        ],
        'dinner': [
            {'name': 'Khichdi', 'calories': 300, 'protein': 10, 'carbs': 50, 'fat': 6, 'serving': '1.5 cups'},
            {'name': 'Dal Roti Veg', 'calories': 320, 'protein': 14, 'carbs': 45, 'fat': 8, 'serving': '1 cup + 2 roti'},
            {'name': 'Vegetable Khichdi', 'calories': 280, 'protein': 9, 'carbs': 48, 'fat': 5, 'serving': '1.5 cups'}
        ],
        'snacks': [
            {'name': 'Fruit + Nuts', 'calories': 250, 'protein': 7, 'carbs': 26, 'fat': 15, 'serving': '1 fruit + 30g'},
            {'name': 'Sprouts Salad', 'calories': 130, 'protein': 10, 'carbs': 18, 'fat': 2, 'serving': '1 cup'},
            {'name': 'Curd with Seeds', 'calories': 150, 'protein': 10, 'carbs': 8, 'fat': 8, 'serving': '1 cup'}
        ]
    }
    
    SUBSTITUTIONS = {
        'veg_to_vegan': {
            'paneer': 'tofu',
            'curd': 'coconut_curd',
            'milk': 'almond_milk',
            'ghee': 'coconut_oil',
            'honey': 'maple_syrup'
        },
        'vegan_to_veg': {
            'tofu': 'paneer',
            'coconut_curd': 'curd',
            'almond_milk': 'milk',
            'coconut_oil': 'ghee',
            'maple_syrup': 'honey'
        },
        'budget_to_premium': {
            'dal': 'quinoa',
            'rice': 'brown_rice',
            'seasonal_veg': 'organic_veg',
            'chicken': 'fish',
            'eggs': 'free_range_eggs'
        },
        'premium_to_budget': {
            'quinoa': 'dal',
            'brown_rice': 'rice',
            'organic_veg': 'seasonal_veg',
            'fish': 'chicken',
            'free_range_eggs': 'eggs'
        }
    }
    
    def generate(self, meal_plan: DailyMealPlan, diet_type: str, budget: str) -> list:
        alternatives = []
        
        # Generate alternatives for each meal
        for meal_type in ['breakfast', 'lunch', 'dinner']:
            original = getattr(meal_plan, meal_type)
            alt_options = self.MEAL_ALTERNATIVES.get(meal_type, [])
            
            alt_meals = [
                MealItem(
                    name=opt['name'],
                    quantity=opt['serving'],
                    calories=opt['calories'],
                    protein=opt['protein'],
                    carbs=opt['carbs'],
                    fat=opt['fat']
                )
                for opt in alt_options[:3]
            ]
            
            # Determine substitutions
            subs = {}
            if diet_type == 'veg':
                subs.update(self.SUBSTITUTIONS['veg_to_vegan'])
            elif diet_type == 'vegan':
                subs.update(self.SUBSTITUTIONS['vegan_to_veg'])
                
            if budget == 'low':
                subs.update(self.SUBSTITUTIONS['budget_to_premium'])
            elif budget == 'high':
                subs.update(self.SUBSTITUTIONS['premium_to_budget'])
            
            alternatives.append(FlexibleOptions(
                meal_type=meal_type,
                original=original,
                alternatives=alt_meals,
                substitutions=subs
            ))
        
        # Add snacks alternatives
        snack_alts = [
            MealItem(
                name=opt['name'],
                quantity=opt['serving'],
                calories=opt['calories'],
                protein=opt['protein'],
                carbs=opt['carbs'],
                fat=opt['fat']
            )
            for opt in self.MEAL_ALTERNATIVES['snacks'][:3]
        ]
        
        if meal_plan.snacks:
            alternatives.append(FlexibleOptions(
                meal_type='snacks',
                original=meal_plan.snacks[0],
                alternatives=snack_alts,
                substitutions={}
            ))
        
        return alternatives
