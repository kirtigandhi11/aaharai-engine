from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class UserProfile:
    age: int
    gender: str  # 'male', 'female'
    weight_kg: float
    height_cm: float
    activity_level: str  # 'sedentary', 'light', 'moderate', 'active', 'very_active'
    goal: str  # 'fat_loss', 'muscle_gain', 'maintenance'
    region: str  # 'north', 'south', 'west', 'east', 'general'
    budget: str  # 'low', 'medium', 'high'
    diet_type: str  # 'veg', 'non-veg', 'vegan'
    health_conditions: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    workout_type: str = 'none'  # 'strength', 'cardio', 'yoga', 'none'
    workout_frequency: int = 0
    workout_timing: str = 'morning'  # 'morning', 'afternoon', 'evening'
    
    # Progress tracking fields
    previous_calories: Optional[int] = None
    weight_change_kg: Optional[float] = None
    energy_level: str = 'moderate'  # 'low', 'moderate', 'high'
    hunger_level: str = 'moderate'  # 'low', 'moderate', 'high'
    adherence: str = 'good'  # 'poor', 'fair', 'good', 'excellent'

@dataclass
class DoshaResult:
    primary: str
    secondary: Optional[str]
    reasoning: str
    diet_principles: List[str]
    foods_to_avoid: List[str]

@dataclass
class NutritionTargets:
    bmr: float
    tdee: float
    target_calories: int
    protein_g: int
    carbs_g: int
    fat_g: int

@dataclass
class FoodStrategy:
    allowed_foods: Dict[str, List[str]]
    limited_foods: Dict[str, List[str]]
    avoid_foods: List[str]
    cooking_style: str
    regional_specialties: List[str]

@dataclass
class WorkoutNutrition:
    workout_type: str
    pre_workout_meal: str
    post_workout_meal: str
    protein_adjustment: int  # grams to add/subtract
    carb_timing_advice: str

@dataclass
class MealItem:
    name: str
    quantity: str
    calories: int
    protein: int
    carbs: int
    fat: int

@dataclass
class DailyMealPlan:
    breakfast: MealItem
    lunch: MealItem
    dinner: MealItem
    snacks: List[MealItem]
    total_calories: int
    total_protein: int
    total_carbs: int
    total_fat: int

@dataclass
class FlexibleOptions:
    meal_type: str
    original: MealItem
    alternatives: List[MealItem]
    substitutions: Dict[str, str]  # e.g., {"cow_milk": "almond_milk"}

@dataclass
class GroceryList:
    vegetables: Dict[str, float]  # item: quantity_kg
    grains: Dict[str, float]
    proteins: Dict[str, float]
    dairy_alternatives: Dict[str, float]
    spices_misc: Dict[str, float]
    weekly_scaling_factor: float = 7.0

@dataclass
class AdaptationResult:
    analysis: str
    calorie_adjustment: int
    macro_adjustments: Dict[str, int]
    recommendations: List[str]

@dataclass
class RealTimeAdjustment:
    eaten_item: str
    estimated_calories: int
    remaining_plan: DailyMealPlan
    suggestions: List[str]

@dataclass
class FullSystemOutput:
    user_summary: Dict[str, Any]
    dosha: DoshaResult
    nutrition: NutritionTargets
    strategy: FoodStrategy
    workout_nutrition: WorkoutNutrition
    meal_plan: DailyMealPlan
    flexibility: List[FlexibleOptions]
    grocery: GroceryList
    adaptation: Optional[AdaptationResult]
    real_time: Optional[RealTimeAdjustment]
