"""
Ayurvedic Indian Diet Planning System
Complete 9-Step Pipeline
"""

import json
from typing import Dict, Any, Optional

from models import (
    UserProfile, FullSystemOutput, DoshaResult, NutritionTargets,
    FoodStrategy, WorkoutNutrition, DailyMealPlan, FlexibleOptions,
    GroceryList, AdaptationResult
)
from dosha_analyzer import DoshaAnalyzer
from nutrition_calculator import NutritionCalculator
from food_strategy import FoodStrategyGenerator
from workout_nutrition import WorkoutNutritionPlanner
from meal_planner import MealPlanner
from flexibility_engine import FlexibilityEngine
from grocery_generator import GroceryGenerator
from adaptation_engine import AdaptationEngine


class AyurvedicDietSystem:
    """Main orchestrator for the 9-step diet planning pipeline"""
    
    def __init__(self):
        self.dosha_analyzer = DoshaAnalyzer()
        self.nutrition_calculator = NutritionCalculator()
        self.food_strategy_gen = FoodStrategyGenerator()
        self.workout_planner = WorkoutNutritionPlanner()
        self.meal_planner = MealPlanner()
        self.flexibility_engine = FlexibilityEngine()
        self.grocery_generator = GroceryGenerator()
        self.adaptation_engine = AdaptationEngine()
    
    def run_full_pipeline(self, user_data: Dict[str, Any]) -> FullSystemOutput:
        """Execute all 9 steps of the diet planning pipeline"""
        
        # Step 1: Create User Profile (Analysis)
        profile = self._create_user_profile(user_data)
        user_summary = self._generate_user_summary(profile)
        
        # Step 2: Determine Dosha
        dosha = self.dosha_analyzer.analyze(profile)
        
        # Step 3: Calculate Calories and Macros
        nutrition = self.nutrition_calculator.calculate(profile)
        
        # Step 4: Generate Food Strategy
        strategy = self.food_strategy_gen.generate(profile, dosha)
        
        # Step 5: Plan Workout Nutrition
        workout_nutrition = self.workout_planner.generate(profile)
        
        # Step 6: Create Full Day Meal Plan
        meal_plan = self.meal_planner.generate(
            profile, dosha, nutrition, strategy, workout_nutrition
        )
        
        # Step 7: Generate Flexible Alternatives
        flexibility = self.flexibility_engine.generate(
            meal_plan, profile.diet_type, profile.budget
        )
        
        # Step 8: Create Grocery List
        grocery = self.grocery_generator.generate(meal_plan, days=1)
        
        # Step 9: Weekly AI Adaptation (if progress data available)
        adaptation = None
        if profile.previous_calories is not None or profile.weight_change_kg is not None:
            adaptation = self.adaptation_engine.analyze_and_adjust(profile, nutrition)
        
        return FullSystemOutput(
            user_summary=user_summary,
            dosha=dosha,
            nutrition=nutrition,
            strategy=strategy,
            workout_nutrition=workout_nutrition,
            meal_plan=meal_plan,
            flexibility=flexibility,
            grocery=grocery,
            adaptation=adaptation,
            real_time=None
        )
    
    def _create_user_profile(self, data: Dict[str, Any]) -> UserProfile:
        """Create UserProfile from input dictionary"""
        return UserProfile(
            age=data.get('age', 30),
            gender=data.get('gender', 'male'),
            weight_kg=data.get('weight_kg', 70.0),
            height_cm=data.get('height_cm', 170.0),
            activity_level=data.get('activity_level', 'moderate'),
            goal=data.get('goal', 'maintenance'),
            region=data.get('region', 'general'),
            budget=data.get('budget', 'medium'),
            diet_type=data.get('diet_type', 'veg'),
            health_conditions=data.get('health_conditions', []),
            allergies=data.get('allergies', []),
            workout_type=data.get('workout_type', 'none'),
            workout_frequency=data.get('workout_frequency', 0),
            workout_timing=data.get('workout_timing', 'morning'),
            previous_calories=data.get('previous_calories'),
            weight_change_kg=data.get('weight_change_kg'),
            energy_level=data.get('energy_level', 'moderate'),
            hunger_level=data.get('hunger_level', 'moderate'),
            adherence=data.get('adherence', 'good')
        )
    
    def _generate_user_summary(self, profile: UserProfile) -> Dict[str, Any]:
        """Generate user summary for output"""
        bmi = profile.weight_kg / ((profile.height_cm / 100) ** 2)
        
        # Determine body condition
        if bmi < 18.5:
            body_condition = 'underweight'
        elif bmi < 25:
            body_condition = 'normal'
        else:
            body_condition = 'overweight'
        
        return {
            'age': profile.age,
            'gender': profile.gender,
            'bmi': round(bmi, 1),
            'body_condition': body_condition,
            'goal': profile.goal,
            'activity_level': profile.activity_level,
            'region': profile.region,
            'diet_type': profile.diet_type,
            'health_conditions': profile.health_conditions,
            'allergies': profile.allergies,
            'workout_type': profile.workout_type
        }
    
    def run_real_time_adjustment(self, user_message: str, 
                                current_plan: DailyMealPlan) -> Dict[str, Any]:
        """Handle real-time diet adjustments based on user input"""
        # Simple keyword-based estimation (can be enhanced with NLP)
        message_lower = user_message.lower()
        
        # Estimate calories from common foods
        calorie_estimates = {
            'pizza': 300, 'burger': 400, 'rice': 200, 'roti': 120,
            'dal': 180, 'chicken': 250, 'paneer': 280, 'fruit': 80,
            'banana': 100, 'apple': 80, 'milk': 150, 'curd': 100,
            'sandwich': 250, 'salad': 50, 'nuts': 170
        }
        
        estimated_calories = 0
        eaten_items = []
        
        for food, cals in calorie_estimates.items():
            if food in message_lower:
                estimated_calories += cals
                eaten_items.append(food)
        
        # Default estimate if no food found
        if estimated_calories == 0:
            estimated_calories = 300  # Average snack/meal
        
        # Generate suggestions
        suggestions = []
        if estimated_calories > 500:
            suggestions.append("Consider a lighter dinner to balance today's intake")
        if 'fruit' not in message_lower and 'salad' not in message_lower:
            suggestions.append("Add vegetables or fruits to your next meal")
        if 'protein' in message_lower or any(p in message_lower for p in ['chicken', 'paneer', 'dal']):
            suggestions.append("Good protein choice! Stay hydrated")
        
        return {
            'eaten_items': eaten_items if eaten_items else ['unspecified'],
            'estimated_calories': estimated_calories,
            'remaining_calories': max(0, 1800 - estimated_calories),  # Example target
            'suggestions': suggestions if suggestions else ["Continue with planned meals"]
        }


def main():
    """Example usage of the system"""
    system = AyurvedicDietSystem()
    
    # Example user data
    user_data = {
        'age': 28,
        'gender': 'female',
        'weight_kg': 65.0,
        'height_cm': 162.0,
        'activity_level': 'moderate',
        'goal': 'fat_loss',
        'region': 'north',
        'budget': 'medium',
        'diet_type': 'veg',
        'health_conditions': [],
        'allergies': ['peanuts'],
        'workout_type': 'yoga',
        'workout_frequency': 4,
        'workout_timing': 'morning'
    }
    
    # Run full pipeline
    result = system.run_full_pipeline(user_data)
    
    # Print results
    print("=" * 60)
    print("AYURVEDIC INDIAN DIET PLANNING SYSTEM - FULL REPORT")
    print("=" * 60)
    
    print("\n📊 USER SUMMARY")
    print(f"  Age: {result.user_summary['age']} | Gender: {result.user_summary['gender']}")
    print(f"  BMI: {result.user_summary['bmi']} ({result.user_summary['body_condition']})")
    print(f"  Goal: {result.user_summary['goal']} | Activity: {result.user_summary['activity_level']}")
    
    print("\n☯️  DOSHA ANALYSIS")
    print(f"  Primary Dosha: {result.dosha.primary}")
    print(f"  Secondary Dosha: {result.dosha.secondary or 'None'}")
    print(f"  Reasoning: {result.dosha.reasoning}")
    
    print("\n🔢 NUTRITION TARGETS")
    print(f"  BMR: {result.nutrition.bmr:.0f} kcal")
    print(f"  TDEE: {result.nutrition.tdee:.0f} kcal")
    print(f"  Target Calories: {result.nutrition.target_calories} kcal")
    print(f"  Macros: P={result.nutrition.protein_g}g | C={result.nutrition.carbs_g}g | F={result.nutrition.fat_g}g")
    
    print("\n🍽️  MEAL PLAN")
    print(f"  Breakfast: {result.meal_plan.breakfast.name} ({result.meal_plan.breakfast.calories} kcal)")
    print(f"  Lunch: {result.meal_plan.lunch.name} ({result.meal_plan.lunch.calories} kcal)")
    print(f"  Dinner: {result.meal_plan.dinner.name} ({result.meal_plan.dinner.calories} kcal)")
    print(f"  Snacks: {len(result.meal_plan.snacks)} items")
    print(f"  Total: {result.meal_plan.total_calories} kcal")
    
    print("\n🛒 GROCERY LIST (1 Day)")
    print(f"  Vegetables: {len(result.grocery.vegetables)} items")
    print(f"  Grains: {len(result.grocery.grains)} items")
    print(f"  Proteins: {len(result.grocery.proteins)} items")
    
    if result.adaptation:
        print("\n🔄 ADAPTATION RECOMMENDATIONS")
        print(f"  Analysis: {result.adaptation.analysis}")
        print(f"  Calorie Adjustment: {result.adaptation.calorie_adjustment:+d} kcal")
    
    print("\n" + "=" * 60)
    print("Pipeline completed successfully!")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    main()
