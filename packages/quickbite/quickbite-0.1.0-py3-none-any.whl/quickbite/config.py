# config.py

import os

# Replace 'YOUR_API_KEY' with the actual API key or fetch from environment variable
API_KEY = os.getenv('API_KEY', 'YOUR_API_KEY')

# Hosts for Spoonacular and Edamam APIs via RapidAPI
SPOONACULAR_HOST = 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com'
EDAMAM_HOST = 'edamam-edamam-nutrition-analysis.p.rapidapi.com'

# Common headers for RapidAPI
headers = {
    'x-rapidapi-key': API_KEY
}
