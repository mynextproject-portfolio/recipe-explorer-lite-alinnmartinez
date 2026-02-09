from pydantic import BaseModel, Field, ConfigDict  # Add Field to imports
import uuid
from datetime import datetime
from typing import List, Optional
from enum import Enum

# Constants
MAX_TITLE_LENGTH = 200
MAX_INGREDIENTS = 50

class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium" 
    HARD = "Hard"

class Recipe(BaseModel):
    model_config = ConfigDict(
        # Remove or fix the json_encoders if they exist
        # json_encoders should be a dict mapping types to functions, like:
        # json_encoders = {datetime: str}
    )
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str 
    description: str
    ingredients: List[str]
    instructions: str
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class RecipeCreate(BaseModel):
    title: str
    description: str
    ingredients: List[str]
    instructions: str
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel


class RecipeUpdate(BaseModel):
    title: str
    description: str
    ingredients: List[str]
    instructions: str
    tags: List[str]
    difficulty: DifficultyLevel
