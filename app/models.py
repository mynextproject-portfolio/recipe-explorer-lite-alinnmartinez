from pydantic import BaseModel, Field, ConfigDict
import uuid  # Add this import
from datetime import datetime
from typing import List, Optional

# adding a temp comment to push commit in order to test checks

class Recipe(BaseModel):
    model_config = ConfigDict()
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    ingredients: List[str]
    instructions: List[str]  # Changed from str to List[str]
    cuisine: str  # New field for cuisine/region
    tags: List[str]
    difficulty: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class RecipeCreate(BaseModel):
    title: str
    description: str
    ingredients: List[str]
    instructions: List[str]  # Changed from str to List[str]
    cuisine: str  # New field for cuisine/region
    tags: List[str]
    difficulty: str

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[List[str]] = None  # Changed from str to List[str]
    cuisine: Optional[str] = None  # New field for cuisine/region
    tags: Optional[List[str]] = None
    difficulty: Optional[str] = None
