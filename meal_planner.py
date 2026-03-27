from models import UserProfile, DoshaResult, NutritionTargets, FoodStrategy, WorkoutNutrition, DailyMealPlan, MealItem

class MealPlanner:
    """Step 6: Generate full-day Indian diet plan"""
    
    # Indian food database with nutritional info (per standard serving)
    FOOD_DATABASE = {
        # Breakfast options
        'poha': {'calories': 250, 'protein': 6, 'carbs': 45, 'fat': 5, 'serving': '1.5 cups'},
        'upma': {'calories': 280, 'protein': 7, 'carbs': 42, 'fat': 8, 'serving': '1.5 cups'},
        'oats_porridge': {'calories': 220, 'protein': 8, 'carbs': 38, 'fat': 4, 'serving': '1 bowl'},
        'dosa': {'calories': 180, 'protein': 4, 'carbs': 32, 'fat': 4, 'serving': '2 medium'},
        'idli': {'calories': 160, 'protein': 5, 'carbs': 30, 'fat': 2, 'serving': '4 pieces'},
        'paratha': {'calories': 300, 'protein': 8, 'carbs': 40, 'fat': 12, 'serving': '2 medium'},
        'besan_chilla': {'calories': 240, 'protein': 12, 'carbs': 28, 'fat': 9, 'serving': '2 medium'},
        
        # Lunch/Dinner proteins
        'dal_tadka': {'calories': 180, 'protein': 12, 'carbs': 24, 'fat': 5, 'serving': '1 cup'},
        'rajma': {'calories': 220, 'protein': 14, 'carbs': 30, 'fat': 6, 'serving': '1 cup'},
        'chole': {'calories': 240, 'protein': 13, 'carbs': 32, 'fat': 7, 'serving': '1 cup'},
        'paneer_bhurji': {'calories': 280, 'protein': 18, 'carbs': 8, 'fat': 20, 'serving': '1 cup'},
        'chicken_curry': {'calories': 320, 'protein': 28, 'carbs': 10, 'fat': 18, 'serving': '1 cup'},
        'fish_curry': {'calories': 280, 'protein': 26, 'carbs': 8, 'fat': 15, 'serving': '1 cup'},
        'egg_curry': {'calories': 260, 'protein': 16, 'carbs': 10, 'fat': 18, 'serving': '2 eggs + gravy'},
        'tofu_stir_fry': {'calories': 200, 'protein': 16, 'carbs': 12, 'fat': 10, 'serving': '1 cup'},
        
        # Grains
        'rice': {'calories': 200, 'protein': 4, 'carbs': 45, 'fat': 0, 'serving': '1 cup cooked'},
        'roti': {'calories': 120, 'protein': 4, 'carbs': 22, 'fat': 2, 'serving': '2 medium'},
        'quinoa': {'calories': 220, 'protein': 8, 'carbs': 40, 'fat': 3, 'serving': '1 cup cooked'},
        'khichdi': {'calories': 250, 'protein': 8, 'carbs': 42, 'fat': 6, 'serving': '1.5 cups'},
        
        # Vegetables
        'mixed_veg': {'calories': 120, 'protein': 4, 'carbs': 18, 'fat': 4, 'serving': '1 cup'},
        'palak': {'calories': 80, 'protein': 5, 'carbs': 10, 'fat': 3, 'serving': '1 cup'},
        'bhindi': {'calories': 100, 'protein': 3, 'carbs': 14, 'fat': 4, 'serving': '1 cup'},
        'baingan': {'calories': 110, 'protein': 3, 'carbs': 12, 'fat': 6, 'serving': '1 cup'},
        'lauki': {'calories': 70, 'protein': 2, 'carbs': 12, 'fat': 2, 'serving': '1 cup'},
        
        # Snacks
        'fruit': {'calories': 80, 'protein': 1, 'carbs': 20, 'fat': 0, 'serving': '1 medium'},
        'nuts': {'calories': 170, 'protein': 6, 'carbs': 6, 'fat': 15, 'serving': '30g'},
        'curd': {'calories': 100, 'protein': 8, 'carbs': 6, 'fat': 4, 'serving': '1 cup'},
        'sprouts': {'calories': 130, 'protein': 10, 'carbs': 18, 'fat': 2, 'serving': '1 cup'},
        'buttermilk': {'calories': 50, 'protein': 3, 'carbs': 6, 'fat': 1, 'serving': '1 glass'},
    }
    
    def generate(self, profile: UserProfile, dosha: DoshaResult, 
                 targets: NutritionTargets, strategy: FoodStrategy,
                 workout: WorkoutNutrition) -> DailyMealPlan:
        
        # Adjust protein target based on workout
        adjusted_protein = targets.protein_g + workout.protein_adjustment
        
        # Generate meals
        breakfast = self._create_breakfast(profile, dosha, strategy, targets)
        lunch = self._create_lunch(profile, dosha, strategy, targets, adjusted_protein)
        dinner = self._create_dinner(profile, dosha, strategy, targets, adjusted_protein)
        snacks = self._create_snacks(profile, dosha, strategy, targets)
        
        # Calculate totals
        total_calories = breakfast.calories + lunch.calories + dinner.calories + sum(s.calories for s in snacks)
        total_protein = breakfast.protein + lunch.protein + dinner.protein + sum(s.protein for s in snacks)
        total_carbs = breakfast.carbs + lunch.carbs + dinner.carbs + sum(s.carbs for s in snacks)
        total_fat = breakfast.fat + lunch.fat + dinner.fat + sum(s.fat for s in snacks)
        
        return DailyMealPlan(
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            snacks=snacks,
            total_calories=total_calories,
            total_protein=total_protein,
            total_carbs=total_carbs,
            total_fat=total_fat
        )
    
    def _create_breakfast(self, profile: UserProfile, dosha: DoshaResult,
                         strategy: FoodStrategy, targets: NutritionTargets) -> MealItem:
        # Select based on region and dosha
        if profile.region == 'south':
            if dosha.primary == 'Kapha':
                return self._make_meal('idli', 3, 'pieces')  # Lighter option
            else:
                return self._make_meal('dosa', 2, 'medium + sambar')
        elif profile.region == 'north':
            if dosha.primary == 'Vata':
                return self._make_meal('paratha', 1, 'medium with curd')  # Warming
            else:
                return self._make_meal('poha', 1.5, 'cups')
        else:
            return self._make_meal('oats_porridge', 1, 'bowl with nuts')
    
    def _create_lunch(self, profile: UserProfile, dosha: DoshaResult,
                     strategy: FoodStrategy, targets: NutritionTargets,
                     protein_target: int) -> MealItem:
        # Build balanced lunch
        if profile.diet_type == 'veg':
            main = 'dal_tadka'
            sides = ['rice', 'mixed_veg', 'roti']
        elif profile.diet_type == 'vegan':
            main = 'chole'
            sides = ['rice', 'mixed_veg']
        else:
            main = 'chicken_curry' if profile.region != 'east' else 'fish_curry'
            sides = ['rice', 'mixed_veg', 'roti']
        
        # Calculate combined nutrition
        base = self.FOOD_DATABASE[main]
        total_cal = base['calories']
        total_pro = base['protein']
        total_carb = base['carbs']
        total_fat = base['fat']
        
        for side in sides[:2]:  # Add 2 sides
            side_data = self.FOOD_DATABASE.get(side, {'calories': 100, 'protein': 3, 'carbs': 20, 'fat': 2})
            total_cal += side_data['calories']
            total_pro += side_data['protein']
            total_carb += side_data['carbs']
            total_fat += side_data['fat']
        
        quantity = f"1 cup {main.replace('_', ' ')}, 1 cup rice, 1 roti, 1 cup veg"
        
        return MealItem(
            name=f"{main.replace('_', ' ').title()} Meal",
            quantity=quantity,
            calories=int(total_cal),
            protein=int(total_pro),
            carbs=int(total_carb),
            fat=int(total_fat)
        )
    
    def _create_dinner(self, profile: UserProfile, dosha: DoshaResult,
                      strategy: FoodStrategy, targets: NutritionTargets,
                      protein_target: int) -> MealItem:
        # Lighter dinner
        if dosha.primary == 'Kapha':
            # Very light dinner
            return self._make_meal('khichdi', 1.5, 'cups with vegetables')
        elif dosha.primary == 'Vata':
            # Warm, grounding dinner
            return self._make_meal('dal_tadka', 1, 'cup with roti and lauki')
        else:
            # Balanced dinner
            if profile.diet_type == 'veg':
                return self._make_meal('paneer_bhurji', 1, 'cup with roti')
            else:
                return self._make_meal('fish_curry' if profile.region == 'coastal' else 'egg_curry', 
                                      1, 'serving with rice')
    
    def _create_snacks(self, profile: UserProfile, dosha: DoshaResult,
                      strategy: FoodStrategy, targets: NutritionTargets) -> list:
        snacks = []
        
        # Morning snack
        if dosha.primary == 'Pitta':
            snacks.append(self._make_meal('fruit', 1, 'medium (sweet fruit)'))
        else:
            snacks.append(self._make_meal('nuts', 30, 'grams'))
        
        # Evening snack
        if profile.diet_type != 'vegan':
            snacks.append(self._make_meal('curd', 1, 'cup'))
        else:
            snacks.append(self._make_meal('sprouts', 1, 'cup'))
        
        # Post-workout snack if applicable
        if profile.workout_frequency > 0:
            snacks.append(self._make_meal('buttermilk', 1, 'glass'))
        
        return snacks
    
    def _make_meal(self, food_key: str, quantity: float, unit: str) -> MealItem:
        db_entry = self.FOOD_DATABASE.get(food_key, {'calories': 200, 'protein': 10, 'carbs': 30, 'fat': 5})
        
        # Scale nutrition by quantity (simplified)
        scale_factor = quantity if quantity <= 2 else 1.5
        
        return MealItem(
            name=food_key.replace('_', ' ').title(),
            quantity=f"{quantity} {unit}",
            calories=int(db_entry['calories'] * scale_factor),
            protein=int(db_entry['protein'] * scale_factor),
            carbs=int(db_entry['carbs'] * scale_factor),
            fat=int(db_entry['fat'] * scale_factor)
        )
