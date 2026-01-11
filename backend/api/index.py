"""Vercel serverless function for FastAPI"""

import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Define the handler function
def handler(event, context):
    """Handle incoming requests."""
    # Import inside the function to avoid import-time issues
    from mangum import Mangum
    from src.main import create_app

    # Create the app and handler
    app = create_app()
    mangum_handler = Mangum(app)

    # Handle the request
    return mangum_handler(event, context)