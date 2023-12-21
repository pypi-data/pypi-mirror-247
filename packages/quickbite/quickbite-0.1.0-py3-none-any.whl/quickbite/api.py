# api.py

import requests
from .config import SPOONACULAR_HOST, EDAMAM_HOST, headers

def search_recipes_by_ingredients(ingredients):
    """
    Search for recipes based on a list of ingredients.

    Parameters:
    ingredients (list of str): A list of ingredient names.

    Returns:
    list: A list of dictionaries, each dictionary representing a recipe.
    """
    # Function implementation
    url = f"https://{SPOONACULAR_HOST}/recipes/findByIngredients"
    params = {
        'ingredients': ','.join(ingredients),
        'number': '5',  # Adjust the number of results as needed
        'ignorePantry': 'true'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def search_recipes_excluding_ingredients(ingredients, exclusions):
    """
    Search for recipes based on ingredients while excluding certain ingredients.

    Parameters:
    ingredients (list of str): Ingredients to include.
    exclusions (list of str): Ingredients to exclude.

    Returns:
    list: A list of recipes that include specified ingredients and exclude others.
    """
    # Function implementation
    # First, fetch recipes that include the desired ingredients
    recipes = search_recipes_by_ingredients(ingredients)
    
    # Now, filter out any recipes that contain the excluded ingredients
    filtered_recipes = []
    for recipe in recipes:
        # Assuming each recipe has a field that lists its ingredients, which might not be the case
        recipe_ingredients = [ingredient['name'] for ingredient in recipe['usedIngredients']]
        if not any(excluded in recipe_ingredients for excluded in exclusions):
            filtered_recipes.append(recipe)
    
    return filtered_recipes

def get_nutritional_data(ingredient):
    """
    Retrieve nutritional information for a given ingredient.

    Parameters:
    ingredient (str): The ingredient to get nutritional data for.

    Returns:
    dict: Nutritional data for the given ingredient.
    """
    # Function implementation
    # Update the headers for Edamam API
    edamam_headers = headers.copy()
    edamam_headers['x-rapidapi-host'] = EDAMAM_HOST
    
    # The URL for the Edamam API endpoint
    url = f'https://{EDAMAM_HOST}/api/nutrition-data'
    
    # The parameters for the request
    params = {
        'ingr': ingredient,
        'nutrition-type': 'cooking'
    }
    
    try:
        # Send the GET request
        response = requests.get(url, headers=edamam_headers, params=params)
        response.raise_for_status()  # Will raise an HTTPError for unsuccessful status codes
        
        # If the request was successful, return the response data
        return response.json()
        
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An Error Occurred: {err}")
        return None  # Return None or raise an exception as needed

def get_recipe_details(recipe_id):
    """
    Fetch detailed information about a specific recipe.

    Parameters:
    recipe_id (int): The unique identifier for a recipe.

    Returns:
    dict: Detailed information about the recipe.
    """
    # Function implementation
    url = f"https://{SPOONACULAR_HOST}/recipes/{recipe_id}/information"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()  # Returns detailed recipe data including ingredients list


def get_ingredients_for_recipe(recipe_id):
    url = f"https://{SPOONACULAR_HOST}/recipes/{recipe_id}/information"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    recipe_details = response.json()
    
    # Extract the ingredients list from the details
    ingredients_list = recipe_details.get('extendedIngredients', [])
    
    # Format the ingredients list to be more readable
    formatted_ingredients = [
        f"{ingredient.get('amount', 'N/A')} {ingredient.get('unit', '')} {ingredient.get('name', '')}"
        for ingredient in ingredients_list
    ]
    
    return formatted_ingredients


