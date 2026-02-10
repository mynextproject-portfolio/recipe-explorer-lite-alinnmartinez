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
                "id": "test-recipe-001",
                "title": "Test Recipe",
                "description": "A simple test recipe",
                "ingredients": ["test ingredient 1", "test ingredient 2"],
                "instructions": ["Step 1: Test step", "Step 2: Another test step"],
                "cuisine": "International",
                "tags": ["test"],
                "difficulty": "Easy",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
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
