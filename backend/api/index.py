"""
Vercel serverless function for FastAPI application
This file serves as the entry point for Vercel's Python runtime
"""

import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def handler(event, context):
    """
    Vercel serverless function handler

    Args:
        event: The event data passed by Vercel/AWS
        context: The context object passed by Vercel/AWS

    Returns:
        The response from the FastAPI application
    """
    # Import inside the function to avoid import-time issues
    from mangum import Mangum
    from src.main import create_app

    # Create the app instance when the handler is called
    app = create_app()

    # Create and return the response using Mangum
    mangum_handler = Mangum(app)
    return mangum_handler(event, context)


# Make sure the handler is available at the module level
try:
    # This ensures Vercel can detect the handler function
    handler  # Reference to ensure it exists
except NameError:
    pass