import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = "You are a food detection assistant."

USER_PROMPT = "Find and describe all food items in this image. Respond ONLY with a strict JSON array of objects, each with 'name' (food name), 'confidence' (0-1), and 'bounding_box' (x, y, width, height) for each detected food item. Do not include any other text."