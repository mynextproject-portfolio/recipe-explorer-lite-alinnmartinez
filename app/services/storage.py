from typing import Dict, List, Optional
from datetime import datetime
import json  # TODO: Remove this - not used anymore
from app.models import Recipe, RecipeCreate, RecipeUpdate

# Global counter for analytics (can be used for analytics)
recipe_view_count = {}

class RecipeStorage:
    def __init__(self):
        self.recipes: Dict[str, Recipe] = {}
        # Load seed data on startup
        self._load_seed_data()
    
    def _load_seed_data(self):
        """Load initial seed data for testing"""
        seed_recipes = [
            {
                "id": "poutine-canada-001",
                "title": "Classic Quebec Poutine",
                "description": "The original comfort food from Quebec - crispy fries topped with fresh cheese curds and rich brown gravy. A perfect combination of textures and flavors that has become Canada's national dish.",
                "ingredients": [
                    "4 large russet potatoes, cut into fries",
                    "2 cups fresh cheese curds, at room temperature",
                    "3 tablespoons butter",
                    "3 tablespoons all-purpose flour",
                    "2 cups beef stock",
                    "1 tablespoon Worcestershire sauce",
                    "Salt and pepper to taste",
                    "Vegetable oil for frying"
                ],
                "instructions": [
                    "Cut potatoes into thick fries, about 1/2 inch thick. Soak in cold water for 30 minutes to remove excess starch.",
                    "Heat oil to 325°F (165°C) for the first fry. Fry potatoes for 3-4 minutes. Remove and drain on paper towels.",
                    "Increase oil temperature to 375°F (190°C). Fry potatoes again for 2-3 minutes until golden brown and crispy.",
                    "For the gravy: melt butter in a saucepan over medium heat. Whisk in flour and cook for 2 minutes to make a roux.",
                    "Gradually add beef stock while whisking constantly to prevent lumps. Add Worcestershire sauce.",
                    "Simmer for 5-10 minutes until thickened. Season with salt and pepper.",
                    "Place hot fries in serving dish, top with cheese curds, then pour hot gravy over top.",
                    "Serve immediately while the cheese is melting and everything is hot."
                ],
                "cuisine": "Canadian",
                "tags": ["comfort food", "Canadian", "vegetarian-friendly"],
                "difficulty": "Easy",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            },
            {
                "id": "shuba-russia-002",
                "title": "Shuba (Herring Under a Fur Coat)",
                "description": "A beloved Russian layered salad that's essential at New Year celebrations. This colorful dish combines salted herring with layers of vegetables and mayonnaise, creating a rich and festive treat.",
                "ingredients": [
                    "4 salted herring fillets, finely chopped",
                    "3 medium potatoes, boiled and grated",
                    "3 large carrots, boiled and grated",
                    "4 hard-boiled eggs, whites and yolks separated and grated",
                    "3 medium beets, boiled and grated",
                    "1 large onion, finely chopped",
                    "1 1/2 cups mayonnaise",
                    "Salt to taste",
                    "Fresh dill for garnish"
                ],
                "instructions": [
                    "Boil potatoes, carrots, and beets separately until tender. Beets take the longest (45-60 minutes). Let cool completely.",
                    "Hard-boil eggs for 10 minutes, then cool in ice water. Separate whites from yolks and grate separately.",
                    "Peel and grate all vegetables using a coarse grader. Keep each ingredient in separate bowls.",
                    "In a clear glass dish, start layering: first spread chopped herring evenly on the bottom.",
                    "Layer chopped onion over herring, then spread a thin layer of mayonnaise.",
                    "Add layer of grated potatoes, then mayonnaise. Season lightly with salt.",
                    "Continue with grated carrots and mayonnaise, then grated egg whites and mayonnaise.",
                    "Finally, top with grated beets and a final layer of mayonnaise to cover completely.",
                    "Garnish with grated egg yolks and fresh dill. Refrigerate for at least 4 hours or overnight.",
                    "Cut into squares to serve, showing off the beautiful layers."
                ],
                "cuisine": "Russian",
                "tags": ["Russian", "layered salad", "New Year", "festive", "make-ahead"],
                "difficulty": "Medium",
                "created_at": "2024-01-20T14:45:00",
                "updated_at": "2024-01-20T14:45:00"
            },
            {
                "id": "guo-bao-rou-china-003",
                "title": "Guo Bao Rou (Sweet and Sour Crispy Pork)",
                "description": "A signature dish from Northeast China with perfectly crispy pork pieces coated in a glossy sweet and sour sauce. The key is achieving the right balance of crispy texture and tangy-sweet flavor.",
                "ingredients": [
                    "1 lb pork tenderloin, cut into 2-inch strips",
                    "1/2 cup cornstarch",
                    "1/4 cup all-purpose flour",
                    "1 egg white",
                    "1 teaspoon salt",
                    "2 tablespoons Shaoxing wine or dry sherry",
                    "4 tablespoons sugar",
                    "3 tablespoons rice vinegar",
                    "2 tablespoons light soy sauce",
                    "1 tablespoon tomato paste",
                    "2 cloves garlic, minced",
                    "1 tablespoon fresh ginger, minced",
                    "2 green onions, chopped",
                    "Vegetable oil for deep frying"
                ],
                "instructions": [
                    "Cut pork tenderloin into strips about 2 inches long and 1/2 inch thick. Season with salt and Shaoxing wine.",
                    "Make batter by mixing cornstarch, flour, egg white, and 2-3 tablespoons water until smooth. Coat pork pieces.",
                    "Heat oil to 350°F (175°C). Deep fry pork pieces until golden and crispy, about 4-5 minutes. Remove and drain.",
                    "Let oil temperature rise to 375°F (190°C) and fry pork again for 1-2 minutes for extra crispiness.",
                    "For sauce: mix sugar, rice vinegar, soy sauce, and tomato paste in a small bowl until sugar dissolves.",
                    "Heat 2 tablespoons oil in a wok over high heat. Add garlic and ginger, stir-fry for 30 seconds.",
                    "Pour in sauce mixture and bring to a boil. The sauce should be glossy and slightly thickened.",
                    "Add crispy pork pieces to the wok and quickly toss to coat with sauce.",
                    "Garnish with chopped green onions and serve immediately while the pork is still crispy.",
                    "Serve with steamed rice and enjoy the contrast of crispy pork and tangy sauce."
                ],
                "cuisine": "Chinese",
                "tags": ["Chinese", "sweet and sour", "crispy", "Northeast Chinese", "stir-fry"],
                "difficulty": "Hard",
                "created_at": "2024-01-25T09:15:00",
                "updated_at": "2024-01-25T09:15:00"
            }
        ]
        
        for recipe_dict in seed_recipes:
            try:
                recipe = Recipe(**recipe_dict)
                self.recipes[recipe.id] = recipe
            except Exception as e:
                print(f"Failed to load seed recipe: {e}")
    
    def get_all_recipes(self) -> List[Recipe]:
        print(f"DEBUG: get_all_recipes called, storage has {len(self.recipes)} recipes")
        result = list(self.recipes.values())
        print(f"DEBUG: Converting to list returned {len(result)} recipes")
        return result
    
    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        return self.recipes.get(recipe_id)
    
    def search_recipes(self, query: str) -> List[Recipe]:
        if not query:
            return self.get_all_recipes()
        
        # Case-insensitive title search
        query_lower = query.lower()
        results = []
        for recipe in self.recipes.values():
            if query_lower in recipe.title.lower():
                results.append(recipe)
        return results
    
    def create_recipe(self, recipe_data: RecipeCreate) -> Recipe:
        recipe = Recipe(**recipe_data.model_dump())
        self.recipes[recipe.id] = recipe
        return recipe
    
    def update_recipe(self, recipe_id: str, recipe_data: RecipeUpdate) -> Optional[Recipe]:
        if recipe_id not in self.recipes:
            return None
        
        recipe = self.recipes[recipe_id]
        updated_data = recipe_data.model_dump()
        for key, value in updated_data.items():
            setattr(recipe, key, value)
        recipe.updated_at = datetime.now()
        
        self.recipes[recipe_id] = recipe
        return recipe
    
    def delete_recipe(self, recipe_id: str) -> bool:
        if recipe_id in self.recipes:
            del self.recipes[recipe_id]
            return True
        return False
    
    def import_recipes(self, recipes_data: List[dict]) -> int:
        # Replace all existing recipes
        self.recipes.clear()
        count = 0
        
        for recipe_dict in recipes_data:
            try:
                # Handle datetime strings if they exist
                if 'created_at' in recipe_dict:
                    recipe_dict['created_at'] = datetime.fromisoformat(recipe_dict['created_at'])
                if 'updated_at' in recipe_dict:
                    recipe_dict['updated_at'] = datetime.fromisoformat(recipe_dict['updated_at'])
                
                recipe = Recipe(**recipe_dict)
                self.recipes[recipe.id] = recipe
                count += 1
            except Exception:
                # Skip invalid recipes
                continue
        
        return count


# Global storage instance (intentionally simple for refactoring)
recipe_storage = RecipeStorage()
