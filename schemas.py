"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Fitness app schemas

class Exercise(BaseModel):
    name: str = Field(..., description="Exercise name, e.g., Push Ups")
    sets: int = Field(..., ge=1, le=20, description="Number of sets")
    reps: int = Field(..., ge=1, le=200, description="Reps per set")

class Workout(BaseModel):
    """
    Workouts collection schema
    Collection name: "workout"
    """
    title: str = Field(..., description="Workout title, e.g., Upper Body Blast")
    difficulty: Optional[str] = Field("Beginner", description="Difficulty level")
    exercises: List[Exercise] = Field(default_factory=list, description="List of exercises")

class Log(BaseModel):
    """
    Logs collection schema
    Collection name: "log"
    """
    date: str = Field(..., description="ISO date string for the workout session")
    workout_title: str = Field(..., description="What workout was completed")
    notes: Optional[str] = Field(None, description="Any notes about the session")
    duration_minutes: Optional[int] = Field(None, ge=1, le=1000, description="Duration in minutes")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
