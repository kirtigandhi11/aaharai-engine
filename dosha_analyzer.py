from models import UserProfile, DoshaResult
from typing import Optional, List

class DoshaAnalyzer:
    """Step 2: Determine Ayurvedic Dosha based on user profile"""
    
    def analyze(self, profile: UserProfile) -> DoshaResult:
        vata_score = 0
        pitta_score = 0
        kapha_score = 0
        
        # Body build analysis
        bmi = profile.weight_kg / ((profile.height_cm / 100) ** 2)
        
        if bmi < 18.5:
            vata_score += 3
        elif bmi < 22:
            pitta_score += 2
        else:
            kapha_score += 3
            
        # Weight tendency
        if profile.goal == 'muscle_gain' and bmi < 20:
            vata_score += 2
        elif profile.goal == 'fat_loss' and bmi > 25:
            kapha_score += 2
            
        # Appetite and metabolism indicators
        if profile.activity_level in ['sedentary', 'light']:
            kapha_score += 1
        elif profile.activity_level == 'very_active':
            vata_score += 1
            
        # Regional climate influence (simplified)
        if profile.region in ['north', 'west']:  # Drier climates
            vata_score += 1
        elif profile.region in ['south', 'east']:  # Hotter/humid climates
            pitta_score += 1
            
        # Determine primary and secondary doshas
        scores = {'Vata': vata_score, 'Pitta': pitta_score, 'Kapha': kapha_score}
        sorted_doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        primary = sorted_doshas[0][0]
        secondary = sorted_doshas[1][0] if sorted_doshas[1][1] > 0 else None
        
        reasoning = self._generate_reasoning(profile, primary, secondary, scores)
        diet_principles = self._get_diet_principles(primary)
        foods_to_avoid = self._get_foods_to_avoid(primary)
        
        return DoshaResult(
            primary=primary,
            secondary=secondary,
            reasoning=reasoning,
            diet_principles=diet_principles,
            foods_to_avoid=foods_to_avoid
        )
    
    def _generate_reasoning(self, profile: UserProfile, primary: str, 
                          secondary: Optional[str], scores: dict) -> str:
        bmi = profile.weight_kg / ((profile.height_cm / 100) ** 2)
        
        reasons = []
        
        if primary == 'Vata':
            reasons.append(f"Your BMI of {bmi:.1f} suggests a lighter build typical of Vata.")
            reasons.append("You may have irregular eating habits or variable appetite.")
        elif primary == 'Pitta':
            reasons.append(f"Your BMI of {bmi:.1f} indicates a medium build characteristic of Pitta.")
            reasons.append("You likely have a strong appetite and good digestion.")
        else:  # Kapha
            reasons.append(f"Your BMI of {bmi:.1f} suggests a heavier build common in Kapha.")
            reasons.append("You may experience slower metabolism and tendency to gain weight.")
            
        if secondary:
            reasons.append(f"Secondary {secondary} influences add complexity to your constitution.")
            
        return " ".join(reasons)
    
    def _get_diet_principles(self, dosha: str) -> List[str]:
        principles = {
            'Vata': [
                "Eat warm, moist, and grounding foods",
                "Prefer sweet, sour, and salty tastes",
                "Maintain regular meal times",
                "Include healthy fats like ghee and sesame oil",
                "Avoid cold, dry, and raw foods"
            ],
            'Pitta': [
                "Eat cooling and hydrating foods",
                "Prefer sweet, bitter, and astringent tastes",
                "Avoid excessive spicy, sour, and salty foods",
                "Include fresh fruits and vegetables",
                "Eat at regular intervals, don't skip meals"
            ],
            'Kapha': [
                "Eat light, warm, and dry foods",
                "Prefer pungent, bitter, and astringent tastes",
                "Reduce heavy, oily, and sweet foods",
                "Include plenty of vegetables and legumes",
                "Avoid dairy and excessive carbohydrates"
            ]
        }
        return principles.get(dosha, [])
    
    def _get_foods_to_avoid(self, dosha: str) -> List[str]:
        avoid = {
            'Vata': ['Cold drinks', 'Raw salads', 'Beans', 'Cabbage', 'Excessive caffeine'],
            'Pitta': ['Spicy chilies', 'Fermented foods', 'Excessive salt', 'Alcohol', 'Fried foods'],
            'Kapha': ['Dairy products', 'Sweet desserts', 'Red meat', 'Excessive oils', 'White rice']
        }
        return avoid.get(dosha, [])
