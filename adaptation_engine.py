from models import UserProfile, AdaptationResult, NutritionTargets

class AdaptationEngine:
    """Step 9: Adjust diet based on progress tracking"""
    
    def analyze_and_adjust(self, profile: UserProfile, 
                          previous_targets: NutritionTargets) -> AdaptationResult:
        """Analyze progress and recommend adjustments"""
        
        analysis = self._analyze_progress(profile)
        calorie_adjustment = self._calculate_calorie_adjustment(profile, previous_targets)
        macro_adjustments = self._calculate_macro_adjustments(profile, previous_targets)
        recommendations = self._generate_recommendations(profile)
        
        return AdaptationResult(
            analysis=analysis,
            calorie_adjustment=calorie_adjustment,
            macro_adjustments=macro_adjustments,
            recommendations=recommendations
        )
    
    def _analyze_progress(self, profile: UserProfile) -> str:
        """Analyze user progress based on metrics"""
        parts = []
        
        # Weight change analysis
        if profile.weight_change_kg is not None:
            if profile.weight_change_kg < -0.5:
                parts.append(f"Good weight loss of {abs(profile.weight_change_kg):.1f} kg detected.")
            elif profile.weight_change_kg > 0.5:
                if profile.goal == 'fat_loss':
                    parts.append(f"Weight gain of {profile.weight_change_kg:.1f} kg - plan needs adjustment.")
                else:
                    parts.append(f"Weight gain of {profile.weight_change_kg:.1f} kg - on track for muscle gain.")
            else:
                parts.append("Weight stable - may need to adjust calories for progress.")
        
        # Energy level analysis
        if profile.energy_level == 'low':
            parts.append("Low energy reported - may need more carbs or calories.")
        elif profile.energy_level == 'high':
            parts.append("Energy levels optimal - current plan working well.")
        
        # Hunger analysis
        if profile.hunger_level == 'high':
            parts.append("High hunger reported - increase protein and fiber.")
        elif profile.hunger_level == 'low':
            parts.append("Appetite controlled - good satiety from current plan.")
        
        # Adherence analysis
        adherence_scores = {'poor': 0.3, 'fair': 0.6, 'good': 0.85, 'excellent': 1.0}
        score = adherence_scores.get(profile.adherence, 0.7)
        if score < 0.6:
            parts.append("Adherence challenges - simplify meal plan or add flexibility.")
        elif score >= 0.85:
            parts.append("Excellent adherence - continue current approach.")
        
        return " ".join(parts) if parts else "Insufficient data for analysis."
    
    def _calculate_calorie_adjustment(self, profile: UserProfile,
                                     previous: NutritionTargets) -> int:
        """Calculate recommended calorie adjustment"""
        adjustment = 0
        
        # Rule: No progress → reduce calories (for fat loss)
        if profile.weight_change_kg is not None:
            if abs(profile.weight_change_kg) < 0.3:  # No significant change
                if profile.goal == 'fat_loss':
                    adjustment = -150  # Reduce by 150 calories
                elif profile.goal == 'muscle_gain':
                    adjustment = +100  # Increase slightly
            elif profile.weight_change_kg > 1.0 and profile.goal == 'fat_loss':
                adjustment = -200  # Significant reduction needed
        
        # Rule: Low energy → increase carbs (which means increase calories)
        if profile.energy_level == 'low':
            adjustment = max(adjustment, +100)
        
        # Rule: High hunger with no weight loss → maintain but adjust macros
        if profile.hunger_level == 'high' and profile.weight_change_kg is not None:
            if abs(profile.weight_change_kg) < 0.3:
                adjustment = -50  # Slight reduction, but focus on macros
        
        return adjustment
    
    def _calculate_macro_adjustments(self, profile: UserProfile,
                                    previous: NutritionTargets) -> dict:
        """Calculate macro adjustments based on rules"""
        adjustments = {'protein': 0, 'carbs': 0, 'fat': 0}
        
        # Rule: Low energy → increase carbs
        if profile.energy_level == 'low':
            adjustments['carbs'] = +30  # Add 30g carbs (120 calories)
        
        # Rule: High hunger → increase protein/fiber
        if profile.hunger_level == 'high':
            adjustments['protein'] = +20  # Add 20g protein (80 calories)
            # Fiber comes from food choices, not direct macro
        
        # Muscle gain goal → ensure adequate protein
        if profile.goal == 'muscle_gain' and profile.adherence in ['good', 'excellent']:
            if adjustments['protein'] < 10:
                adjustments['protein'] = +10
        
        # Fat loss with good adherence → maintain protein, adjust carbs
        if profile.goal == 'fat_loss' and profile.adherence == 'excellent':
            if profile.weight_change_kg is not None and profile.weight_change_kg < -0.5:
                adjustments['carbs'] = -20  # Can reduce carbs slightly
        
        return adjustments
    
    def _generate_recommendations(self, profile: UserProfile) -> list:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on energy level
        if profile.energy_level == 'low':
            recommendations.extend([
                "Increase carbohydrate intake around workout times",
                "Ensure adequate sleep (7-8 hours)",
                "Consider adding a pre-workout snack"
            ])
        
        # Based on hunger
        if profile.hunger_level == 'high':
            recommendations.extend([
                "Increase protein at each meal",
                "Add more fiber-rich vegetables",
                "Drink water before meals",
                "Include healthy fats for satiety"
            ])
        
        # Based on adherence
        if profile.adherence in ['poor', 'fair']:
            recommendations.extend([
                "Simplify meal prep with batch cooking",
                "Keep healthy snacks readily available",
                "Set reminders for meal times",
                "Allow one flexible meal per week"
            ])
        
        # Based on weight change
        if profile.weight_change_kg is not None:
            if profile.weight_change_kg > 0.5 and profile.goal == 'fat_loss':
                recommendations.append("Review portion sizes and reduce high-calorie snacks")
            elif profile.weight_change_kg < -1.0 and profile.goal == 'fat_loss':
                recommendations.append("Consider a diet break or slight calorie increase")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Continue current plan - showing good results")
            recommendations.append("Track progress weekly and adjust as needed")
        
        return recommendations[:5]  # Limit to top 5 recommendations
