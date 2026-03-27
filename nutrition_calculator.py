from models import UserProfile, NutritionTargets

class NutritionCalculator:
    """Step 3: Calculate BMR, TDEE, and macro targets using Mifflin-St Jeor equation"""
    
    ACTIVITY_MULTIPLIERS = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    def calculate(self, profile: UserProfile) -> NutritionTargets:
        # Step 1: Calculate BMR using Mifflin-St Jeor equation
        bmr = self._calculate_bmr(profile)
        
        # Step 2: Calculate TDEE
        tdee = bmr * self.ACTIVITY_MULTIPLIERS.get(profile.activity_level, 1.2)
        
        # Step 3: Apply goal adjustment
        target_calories = self._apply_goal_adjustment(tdee, profile.goal)
        
        # Step 4: Calculate macros
        protein_g, fat_g, carbs_g = self._calculate_macros(profile, target_calories)
        
        return NutritionTargets(
            bmr=round(bmr, 2),
            tdee=round(tdee, 2),
            target_calories=target_calories,
            protein_g=protein_g,
            carbs_g=carbs_g,
            fat_g=fat_g
        )
    
    def _calculate_bmr(self, profile: UserProfile) -> float:
        """Mifflin-St Jeor Equation"""
        if profile.gender == 'male':
            bmr = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * profile.age) + 5
        else:  # female
            bmr = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * profile.age) - 161
        return bmr
    
    def _apply_goal_adjustment(self, tdee: float, goal: str) -> int:
        """Apply calorie adjustment based on goal"""
        if goal == 'fat_loss':
            # 15% deficit (middle of 10-20% range)
            return int(tdee * 0.85)
        elif goal == 'muscle_gain':
            # 10% surplus (middle of 5-15% range)
            return int(tdee * 1.10)
        else:  # maintenance
            return int(tdee)
    
    def _calculate_macros(self, profile: UserProfile, calories: int) -> tuple:
        """Calculate protein, fat, and carbs based on goal"""
        weight = profile.weight_kg
        
        # Protein calculation based on goal
        if profile.goal == 'muscle_gain':
            protein_per_kg = 1.8  # Higher for muscle gain
        elif profile.goal == 'fat_loss':
            protein_per_kg = 2.0  # Higher for satiety during fat loss
        else:
            protein_per_kg = 1.2  # Maintenance
            
        protein_g = int(weight * protein_per_kg)
        protein_calories = protein_g * 4
        
        # Fat: 25% of total calories (middle of 20-30%)
        fat_calories = calories * 0.25
        fat_g = int(fat_calories / 9)
        
        # Carbs: remaining calories
        remaining_calories = calories - protein_calories - fat_calories
        carbs_g = int(remaining_calories / 4)
        
        # Ensure non-negative values
        carbs_g = max(0, carbs_g)
        
        return protein_g, fat_g, carbs_g
