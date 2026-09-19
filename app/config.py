"""
1.Load the .env file.
2.Read the SECRET_KEY variable.
3.Make it available to the rest of the application.
4.Define the JWT algorithm.
"""

from dotenv import load_dotenv
import os

load_dotenv()

# Go to my environment variables, find SECRET_KEY, and put its value into the Python variable SECRET_KEY.
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
