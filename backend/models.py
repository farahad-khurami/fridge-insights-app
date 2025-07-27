from pydantic import BaseModel
from typing import List


class Food(BaseModel):
    name: str
    confidence: float
    bounding_box: List[int]


class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    instructions: str


class FoodAnalysisResult(BaseModel):
    foods: List[Food]
    recipes: List[Recipe]
