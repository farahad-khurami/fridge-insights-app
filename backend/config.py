import os
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("OPENAI_API_KEY")

ALLERGIES = [
    "milk",
    "eggs",
    "fish",
    "crustacean shellfish",
    "tree nuts",
    "peanuts",
    "wheat",
    "soybeans",
    "sesame",
]

SYSTEM_PROMPT = (
    "You are a food detection and recipe recommendation assistant. "
    "You detect foods in images and recommend recipes, taking user allergies into account."
)

USER_PROMPT = (
    "Find and describe all food items in this image. "
    "Respond ONLY with a strict JSON array of objects "
    "With 'name' (food name), 'confidence' (0-1), and 'bounding_box' (x, y, width, height) for each detected food item. "
)
USER_PROMPT += "After listing foods, recommend food or drink recipes that do NOT contain any ingredients from the user's allergies: {}. ".format(
    ALLERGIES
)
USER_PROMPT += "Return the recipes as a JSON array with 'title', 'ingredients', and 'instructions'. "
USER_PROMPT += "Do not include any other text."
