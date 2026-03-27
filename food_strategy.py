from models import UserProfile, DoshaResult, FoodStrategy

class FoodStrategyGenerator:
    """Step 4: Create food strategy based on region, budget, dosha, and health conditions"""
    
    # Regional food databases
    REGIONAL_FOODS = {
        'north': {
            'grains': ['wheat', 'basmati_rice', 'bajra', 'jowar'],
            'proteins': ['paneer', 'dal_tadka', 'chole', 'rajma', 'chicken_curry'],
            'vegetables': ['sarson', 'baingan', 'tinda', 'lauki', 'gobi'],
            'specialties': ['roti', 'paratha', 'naan', 'dal_makhani', 'butter_chicken']
        },
        'south': {
            'grains': ['rice', 'ragi', 'samai'],
            'proteins': ['sambar', 'rasam', 'curd_rice', 'fish_curry', 'egg_dosa'],
            'vegetables': ['drumstick', 'plantain', 'ivy_gourd', 'bitter_gourd'],
            'specialties': ['dosa', 'idli', 'uttapam', 'hyderabadi_biryani']
        },
        'west': {
            'grains': ['rice', 'wheat', 'nachni'],
            'proteins': ['dal_koli', 'fish_curry', 'prawns', 'paneer_bhurji'],
            'vegetables': ['surati_colocasia', 'cluster_beans', 'snake_gourd'],
            'specialties': ['dhokla', 'thepla', 'vada_pav', 'goan_fish_curry']
        },
        'east': {
            'grains': ['rice', 'millet'],
            'proteins': ['fish_curry', 'dal', 'egg_curry', 'prawns'],
            'vegetables': ['potol', 'karela', 'pumpkin', 'spinach'],
            'specialties': ['machher_jhol', 'shukto', 'chingri_malai_curry']
        },
        'general': {
            'grains': ['rice', 'wheat', 'oats', 'quinoa'],
            'proteins': ['dal', 'paneer', 'chicken', 'eggs', 'tofu'],
            'vegetables': ['spinach', 'carrots', 'beans', 'capsicum', 'tomatoes'],
            'specialties': ['khichdi', 'dal_rice', 'roti_sabzi']
        }
    }
    
    BUDGET_TIERS = {
        'low': ['dal', 'rice', 'seasonal_vegetables', 'eggs', 'roti'],
        'medium': ['paneer', 'chicken', 'mixed_vegetables', 'curd', 'fruits'],
        'high': ['fish', 'dry_fruits', 'organic_vegetables', 'quinoa', 'avocado']
    }
    
    DOSHA_BALANCING = {
        'Vata': {
            'favor': ['warm_cooked_foods', 'ghee', 'sesame_oil', 'sweet_fruits', 'root_vegetables'],
            'avoid': ['cold_foods', 'raw_salads', 'beans', 'cabbage', 'caffeine']
        },
        'Pitta': {
            'favor': ['cooling_foods', 'cucumber', 'coconut', 'sweet_fruits', 'ghee'],
            'avoid': ['spicy_foods', 'fermented_items', 'excessive_salt', 'alcohol']
        },
        'Kapha': {
            'favor': ['light_foods', 'vegetables', 'legumes', 'honey', 'ginger'],
            'avoid': ['dairy', 'sweet_foods', 'heavy_grains', 'excessive_oil']
        }
    }
    
    HEALTH_RESTRICTIONS = {
        'diabetes': ['white_rice', 'sugar', 'sweetened_beverages', 'maida'],
        'hypertension': ['excessive_salt', 'pickles', 'processed_foods', 'namkeen'],
        'heart_disease': ['fried_foods', 'red_meat', 'butter', 'cream'],
        'kidney_issues': ['excessive_protein', 'spinach', 'tomatoes', 'coconut_water'],
        'thyroid': ['raw_cruciferous_vegetables', 'soy', 'millets']
    }
    
    def generate(self, profile: UserProfile, dosha: DoshaResult) -> FoodStrategy:
        regional_data = self.REGIONAL_FOODS.get(profile.region, self.REGIONAL_FOODS['general'])
        
        # Build allowed foods list
        allowed_foods = self._build_allowed_foods(profile, dosha, regional_data)
        
        # Build limited foods list
        limited_foods = self._build_limited_foods(profile, dosha)
        
        # Build avoid list
        avoid_foods = self._build_avoid_list(profile, dosha)
        
        # Determine cooking style
        cooking_style = self._determine_cooking_style(dosha.primary, profile.region)
        
        # Get regional specialties
        specialties = regional_data.get('specialties', [])
        
        return FoodStrategy(
            allowed_foods=allowed_foods,
            limited_foods=limited_foods,
            avoid_foods=avoid_foods,
            cooking_style=cooking_style,
            regional_specialties=specialties
        )
    
    def _build_allowed_foods(self, profile: UserProfile, dosha: DoshaResult, 
                            regional_data: dict) -> dict:
        allowed = {
            'grains': regional_data['grains'].copy(),
            'proteins': [],
            'vegetables': regional_data['vegetables'].copy()
        }
        
        # Filter proteins based on diet type
        if profile.diet_type == 'veg':
            allowed['proteins'] = [p for p in regional_data['proteins'] 
                                  if 'chicken' not in p and 'fish' not in p 
                                  and 'egg' not in p and 'prawn' not in p]
        elif profile.diet_type == 'vegan':
            allowed['proteins'] = [p for p in regional_data['proteins'] 
                                  if 'paneer' not in p and 'curd' not in p
                                  and 'chicken' not in p and 'fish' not in p
                                  and 'egg' not in p and 'prawn' not in p]
            allowed['proteins'].extend(['tofu', 'tempeh', 'lentils'])
        else:  # non-veg
            allowed['proteins'] = regional_data['proteins'].copy()
            
        # Add budget-appropriate options
        budget_foods = self.BUDGET_TIERS.get(profile.budget, [])
        for food in budget_foods:
            if food not in allowed['proteins'] and food not in allowed['grains']:
                if any(veg in food for veg in ['vegetable', 'dal', 'rice', 'roti']):
                    if food not in allowed['vegetables'] and food not in allowed['grains']:
                        if 'vegetable' in food:
                            allowed['vegetables'].append(food)
                        elif food in ['dal', 'rice', 'roti']:
                            allowed['grains'].append(food)
                elif food not in allowed['proteins']:
                    allowed['proteins'].append(food)
                    
        return allowed
    
    def _build_limited_foods(self, profile: UserProfile, dosha: DoshaResult) -> dict:
        limited = {}
        dosha_avoid = self.DOSHA_BALANCING.get(dosha.primary, {}).get('avoid', [])
        
        limited['dosha_sensitive'] = dosha_avoid
        
        # Limit based on health conditions
        health_limited = []
        for condition in profile.health_conditions:
            if condition in self.HEALTH_RESTRICTIONS:
                health_limited.extend(self.HEALTH_RESTRICTIONS[condition][:2])  # Limit top 2
                
        limited['health_related'] = list(set(health_limited))
        
        return limited
    
    def _build_avoid_list(self, profile: UserProfile, dosha: DoshaResult) -> list:
        avoid = []
        
        # Add allergies
        avoid.extend(profile.allergies)
        
        # Add dosha-specific avoids
        dosha_avoid = self.DOSHA_BALANCING.get(dosha.primary, {}).get('avoid', [])
        avoid.extend(dosha_avoid)
        
        # Add health condition restrictions
        for condition in profile.health_conditions:
            if condition in self.HEALTH_RESTRICTIONS:
                avoid.extend(self.HEALTH_RESTRICTIONS[condition])
                
        # Remove duplicates
        return list(set(avoid))
    
    def _determine_cooking_style(self, dosha: str, region: str) -> str:
        styles = {
            'Vata': 'Warm, moist cooking with ghee/oil. Prefer stewing and slow-cooking.',
            'Pitta': 'Cooling methods. Steaming, light sautéing. Avoid excessive frying.',
            'Kapha': 'Light cooking. Grilling, baking, steaming. Minimal oil usage.'
        }
        
        base_style = styles.get(dosha, 'Balanced cooking methods')
        
        region_additions = {
            'north': ' Use traditional tandoor andtawa techniques.',
            'south': ' Incorporate coconut-based tempering and fermentation.',
            'west': ' Include steaming (dhokla) and dry roasting methods.',
            'east': ' Use mustard oil tempering and light fish curries.',
            'general': ' Focus on balanced Indian home-cooking methods.'
        }
        
        return base_style + region_additions.get(region, '')
