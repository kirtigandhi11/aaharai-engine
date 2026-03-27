from models import UserProfile, WorkoutNutrition

class WorkoutNutritionPlanner:
    """Step 5: Adjust diet based on workout routine"""
    
    WORKOUT_PROTEIN_ADJUSTMENTS = {
        'strength': 20,      # Extra 20g protein for strength training
        'cardio': 10,        # Extra 10g for cardio
        'yoga': 5,           # Extra 5g for yoga
        'none': 0            # No adjustment
    }
    
    PRE_WORKOUT_MEALS = {
        'strength': {
            'morning': 'Banana with peanut butter toast + black coffee',
            'afternoon': 'Oats with dates and almonds',
            'evening': 'Fruit smoothie with protein powder'
        },
        'cardio': {
            'morning': 'Light fruit (apple/banana) + water',
            'afternoon': 'Energy bar or dates (2-3 pieces)',
            'evening': 'Small bowl of poha or upma'
        },
        'yoga': {
            'morning': 'Warm lemon water + 2 soaked almonds',
            'afternoon': 'Light herbal tea + fruit',
            'evening': 'Coconut water + small fruit'
        },
        'none': {
            'morning': 'Regular breakfast',
            'afternoon': 'Regular lunch',
            'evening': 'Regular dinner'
        }
    }
    
    POST_WORKOUT_MEALS = {
        'strength': {
            'morning': 'Protein shake + banana OR Paneer bhurji with roti',
            'afternoon': 'Chicken breast/Paneer with quinoa/rice',
            'evening': 'Dal + rice + curd OR Egg whites with toast'
        },
        'cardio': {
            'morning': 'Fruit smoothie + handful of nuts',
            'afternoon': 'Khichdi with vegetables',
            'evening': 'Light dal soup + roti'
        },
        'yoga': {
            'morning': 'Fresh fruit + warm milk',
            'afternoon': 'Vegetable khichdi',
            'evening': 'Light vegetable soup'
        },
        'none': {
            'morning': 'Regular lunch',
            'afternoon': 'Regular snacks',
            'evening': 'Regular dinner'
        }
    }
    
    CARB_TIMING_ADVICE = {
        'strength': 'Focus carbs around workout: 40% of daily carbs in pre/post workout meals',
        'cardio': 'Moderate carbs throughout day, slightly higher before cardio sessions',
        'yoga': 'Balanced carb distribution, avoid heavy carbs immediately before practice',
        'none': 'Even carb distribution across meals, focus on complex carbohydrates'
    }
    
    def generate(self, profile: UserProfile) -> WorkoutNutrition:
        workout_type = profile.workout_type if profile.workout_frequency > 0 else 'none'
        
        pre_workout = self._get_pre_workout_meal(workout_type, profile.workout_timing)
        post_workout = self._get_post_workout_meal(workout_type, profile.workout_timing)
        
        protein_adjustment = self.WORKOUT_PROTEIN_ADJUSTMENTS.get(workout_type, 0)
        carb_advice = self.CARB_TIMING_ADVICE.get(workout_type, '')
        
        return WorkoutNutrition(
            workout_type=workout_type,
            pre_workout_meal=pre_workout,
            post_workout_meal=post_workout,
            protein_adjustment=protein_adjustment,
            carb_timing_advice=carb_advice
        )
    
    def _get_pre_workout_meal(self, workout_type: str, timing: str) -> str:
        meals = self.PRE_WORKOUT_MEALS.get(workout_type, self.PRE_WORKOUT_MEALS['none'])
        return meals.get(timing, meals['morning'])
    
    def _get_post_workout_meal(self, workout_type: str, timing: str) -> str:
        meals = self.POST_WORKOUT_MEALS.get(workout_type, self.POST_WORKOUT_MEALS['none'])
        return meals.get(timing, meals['morning'])
