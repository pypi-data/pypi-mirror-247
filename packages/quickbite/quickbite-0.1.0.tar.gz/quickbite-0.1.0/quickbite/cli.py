# cli.py

def get_user_ingredients():
    """
    Prompt the user to enter ingredients they have at hand, separated by commas.

    This function reads user input from the command line. The user should enter
    ingredients separated by commas. The function processes and returns these
    ingredients as a list of strings.

    Returns:
    list of str: A list containing the ingredients entered by the user.
    """
    # Function implementation
    ingredients = input("Enter ingredients you have, separated by commas (e.g., eggs, flour, sugar): ")
    return [ingredient.strip() for ingredient in ingredients.split(',')]

def get_user_exclusions():
    """
    Prompt the user to enter ingredients they wish to exclude from the recipes, separated by commas.

    This function reads user input from the command line. The user should enter
    ingredients to exclude separated by commas. The function processes and returns
    these ingredients as a list of strings.

    Returns:
    list of str: A list containing the ingredients to exclude, as entered by the user.
    """
    # Function implementation
    exclusions = input("Enter ingredients you want to exclude, separated by commas (e.g., nuts, dairy): ")
    return [exclusion.strip() for exclusion in exclusions.split(',')]

def display_recipes(recipes):
    """
    Display a list of recipes to the user.

    This function takes a list of recipes and prints each recipe's title along with
    a numeric index to the console.

    Parameters:
    recipes (list of dict): A list of dictionaries where each dictionary contains
                            information about a recipe, including its title.

    Returns:
    None: This function does not return a value; it outputs to the console.
    """
    # Function implementation
    if recipes:
        print("\nAvailable recipes:")
        for index, recipe in enumerate(recipes, start=1):
            print(f"{index}. {recipe['title']}")
    else:
        print("\nNo recipes found with the given criteria.")
        
def print_nutritional_info(nutritional_info):
    print("\nNutritional Information:")
    for key, value in nutritional_info.items():
        print(f"{key}: {value}")

def print_ingredients_list(ingredients_list):
     """
    Print out a formatted list of ingredients.

    This function takes a list of ingredient descriptions and prints each one to the console.
    Each ingredient description is expected to be a string.

    Parameters:
    ingredients_list (list of str): A list of strings, each describing an ingredient.

    Returns:
    None: This function does not return a value; it outputs to the console.
    """
    # Function implementation
    if not ingredients_list:
        print("No ingredients found.")
        return

    print("\nIngredients List:")
    for ingredient_str in ingredients_list:
        print(ingredient_str)

def format_nutritional_data(data):
     """
    Takes nutritional data in JSON format and prints it in a readable format.

    This function processes a dictionary containing nutritional data and prints
    various nutritional information such as calories, fat, protein, etc., to the console.
    The data is expected to be in the format returned by the Edamam API.

    Parameters:
    data (dict): A dictionary containing nutritional information for a given ingredient or recipe.

    Returns:
    None: This function does not return a value; it outputs to the console.
    """
    # Function implementation
    if not data:
        print("No data to display.")
        return

    # Print the title of the recipe or ingredient
    title = data.get('uri', '').split('#recipe_')[-1].replace('_', ' ').title()
    print(f"Nutritional Information for: {title}\n")
    
    # Extract total nutrients
    total_nutrients = data.get('totalNutrients', {})
    
    # Go through each nutrient and print out its label, quantity, and unit
    for nutrient_id, nutrient_info in total_nutrients.items():
        label = nutrient_info.get('label', '')
        quantity = nutrient_info.get('quantity', 0)
        unit = nutrient_info.get('unit', '')
        print(f"{label}: {quantity:.2f} {unit}")
    
    # Print diet labels if present
    diet_labels = data.get('dietLabels', [])
    if diet_labels:
        print("\nDiet Labels:")
        for label in diet_labels:
            print(f"- {label}")
    
    # Print health labels if present
    health_labels = data.get('healthLabels', [])
    if health_labels:
        print("\nHealth Labels:")
        for label in health_labels:
            print(f"- {label}")
