from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List, Optional
import json
from app.models import Recipe, RecipeCreate, RecipeUpdate
from app.services.storage import recipe_storage

router = APIRouter(prefix="/api")


@router.get("/recipes")
def get_recipes(search: Optional[str] = None):
    """Get all recipes or search by title, ingredients, and cuisine"""
    # TODO: Add pagination when we have more than 100 recipes
    print(f"DEBUG: get_recipes called with search='{search}'")
    print(f"DEBUG: Storage has {len(recipe_storage.recipes)} recipes in storage")
    
    recipes = recipe_storage.get_all_recipes()
    print(f"DEBUG: get_all_recipes() returned {len(recipes)} recipes")
    
    if search:
        print(f"DEBUG: Applying search filter for '{search}'")
        # Use the same search logic as /recipes/search
        terms = search.lower().strip().split()
        filtered = []

        for recipe in recipes:
            # Include cuisine in search haystack
            haystack = " ".join(
                [recipe.title, recipe.cuisine] + recipe.ingredients
            ).lower()

            if all(term in haystack for term in terms):
                filtered.append(recipe)

        recipes = filtered
        print(f"DEBUG: After search filter: {len(recipes)} recipes")
    
    # Log for debugging (remove in production)
    print(f"DEBUG: Returning {len(recipes)} recipes")
    
    return {"recipes": recipes}


@router.get("/recipes/search")
def search_recipes(query: Optional[str] = None):  # Changed from 'search' to 'query'
    """Search recipes by query parameter"""
    recipes = recipe_storage.get_all_recipes()

    if query:  # Changed from 'search' to 'query'
        terms = query.lower().strip().split()
        filtered = []

        for recipe in recipes:
            # Include cuisine in search haystack
            haystack = " ".join(
                [recipe.title, recipe.cuisine] + recipe.ingredients
            ).lower()

            if all(term in haystack for term in terms):
                filtered.append(recipe)

        recipes = filtered

    print(f"Returning {len(recipes)} recipes")
    return {"recipes": recipes}


@router.get("/recipes/export")
def export_recipes():
    """Export all recipes as JSON"""
    recipes = recipe_storage.get_all_recipes()
    # Convert to dict for JSON serialization
    recipes_dict = [recipe.model_dump() for recipe in recipes]  # Changed from .dict() to .model_dump()
    return JSONResponse(content=recipes_dict)


@router.post("/recipes/import")
async def import_recipes(file: UploadFile = File(...)):
    """Import recipes from JSON file"""
    try:
        content = await file.read()
        recipes_data = json.loads(content)
        
        print(f"DEBUG: Importing {len(recipes_data)} recipes from {file.filename}")
        
        # Use the storage service's import method instead of direct assignment
        count = recipe_storage.import_recipes(recipes_data)
        
        print(f"DEBUG: Successfully imported {count} recipes")
        print(f"DEBUG: Total recipes in storage: {len(recipe_storage.recipes)}")
        
        return {"message": f"Successfully imported {count} recipes", "count": count}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        print(f"DEBUG: Import failed with error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")


@router.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: str):
    """Get a specific recipe by ID"""
    recipe = recipe_storage.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/recipes")
def create_recipe(recipe: RecipeCreate):
    """Create a new recipe"""
    new_recipe = recipe_storage.create_recipe(recipe)
    return new_recipe


@router.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: str, recipe: RecipeUpdate):
    """Update an existing recipe"""
    updated_recipe = recipe_storage.update_recipe(recipe_id, recipe)
    if not updated_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe


@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: str):
    """Delete a recipe"""
    success = recipe_storage.delete_recipe(recipe_id)
    if not success:
        return {"error": "Recipe not found", "status": "failed"}
    return {"message": "Recipe deleted successfully", "status": "success"}  # Added status field inconsistently
