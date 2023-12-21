import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.environ.get('API_KEY')

# Print a message if the API key was found, or an error if not
if api_key:
    print("API key found:", api_key)  # For security reasons, you may want to avoid printing the actual key
else:
    print("API key not found. Make sure your .env file is in the same directory as this script.")

